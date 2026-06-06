import cv2
import os
import logging
import numpy as np
import torch
import threading
import time
import ultralytics.nn.tasks
from collections import defaultdict
from ultralytics import YOLO
from ultralytics.utils.plotting import colors
from app.config import settings
from app.counter import Counter
from typing import Generator

# Security override for PyTorch 2.6+ loading YOLO weights
_original_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = _patched_load

logger = logging.getLogger(__name__)


class Detector:
    def __init__(self, counter: Counter):
        self.counter = counter
        
        # Determine model path
        if os.path.exists(settings.MODEL_PATH):
            logger.info(f"Loading custom model from {settings.MODEL_PATH}")
            self.model = YOLO(settings.MODEL_PATH)
        else:
            logger.warning(f"Model not found at {settings.MODEL_PATH}. Falling back to yolov8n.pt")
            self.model = YOLO("yolov8n.pt")

        # Open video source (e.g. 0 for webcam, or RTSP URL)
        source = settings.VIDEO_SOURCE
        if source.isdigit():
            source = int(source)
            
        self.cap = cv2.VideoCapture(source)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) # Prevent 3-5 frame latency buildup
        
        if not self.cap.isOpened():
            logger.error(f"Failed to open video source: {source}")

        # Threading for Decoupled Architecture
        self.latest_frame = None
        self.latest_boxes = []
        self.box_lock = threading.Lock()
        self.running = True
        
        # Thread 1: Camera Capture
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()

        # Thread 2: YOLO Inference
        self.yolo_thread = threading.Thread(target=self._yolo_loop, daemon=True)
        self.yolo_thread.start()

        # Store model class names for display
        self.names = self.model.names

        # Tracking History UI (matching object-tracking.py style)
        self.track_history = defaultdict(lambda: [])
        self.rect_width = 2
        self.font = 1.0
        self.text_width = 2
        self.padding = 12
        self.margin = 10
        self.circle_thickness = 5
        self.polyline_thickness = 2

    def _capture_loop(self):
        """Continuously drain the buffer to ensure we always have the absolute latest frame."""
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.latest_frame = frame
            else:
                time.sleep(0.005)

    def _yolo_loop(self):
        """Continuously run YOLO inference on the latest frame without blocking the video stream."""
        while self.running:
            if self.latest_frame is None:
                time.sleep(0.01)
                continue
                
            frame = self.latest_frame.copy()
            
            # Clean expired IDs from memory
            self.counter.tracker_manager.clean_expired_ids()

            # Run YOLO tracking
            results = self.model.track(
                frame, 
                persist=True, 
                tracker=settings.TRACKER_CONFIG,
                conf=settings.CONFIDENCE_THRESHOLD,
                iou=settings.IOU_THRESHOLD,
                imgsz=480,
                verbose=False
            )

            new_boxes = []
            if results and results[0].boxes and results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()
                class_ids = results[0].boxes.cls.int().cpu().tolist()
                
                for box, track_id, class_id in zip(boxes, track_ids, class_ids):
                    if class_id in [settings.ADULT_CLASS_ID, settings.CHILD_CLASS_ID]:
                        self.counter.process_detection(track_id, class_id)
                        new_boxes.append((box, track_id, class_id))
            
            with self.box_lock:
                self.latest_boxes = new_boxes

    def draw_bbox(self, frame, box, track_id, class_id):
        """Draw bounding box with label at TOP-LEFT, TEXT CENTERED in its box."""
        x1, y1, x2, y2 = map(int, box)

        color = colors(int(class_id), True)

        # Draw main bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, self.rect_width)

        # Prepare label using configured logic instead of raw model names
        class_name = "Adult" if class_id == settings.ADULT_CLASS_ID else "Child"
        label = f"{class_name}:{int(track_id)}"

        # Get text size
        (tw, th), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, self.font, self.text_width
        )

        bg_x1 = x1  # left edge of bbox
        bg_x2 = bg_x1 + (tw + 2 * self.padding)

        bg_y2 = y1  # top of bbox
        bg_y1 = bg_y2 - (th + 2 * self.margin)

        # Draw filled background rectangle (top-left)
        cv2.rectangle(
            frame,
            (bg_x1, bg_y1),
            (bg_x2, bg_y2),
            color,
            -1,
        )

        # Center text in the background rectangle
        text_x = bg_x1 + ((bg_x2 - bg_x1) - tw) // 2
        text_y = bg_y1 + ((bg_y2 - bg_y1) + th) // 2 - 2  # small vertical tweak

        cv2.putText(
            frame,
            label,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.font,
            (255, 255, 255),
            self.text_width,
            cv2.LINE_AA,
        )

    def draw_trail(self, frame, box, track_id, class_id):
        """Draw tracking trail with centroid dot and polyline."""
        x1, y1, x2, y2 = map(int, box)
        track = self.track_history[track_id]
        
        # Append centroid
        track.append((float((x1 + x2) / 2), float((y1 + y2) / 2)))
        
        if len(track) > 50:  # retain 50 tracks
            track.pop(0)

        # Draw the tracking lines
        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
        color = colors(int(class_id), True)

        # Current centroid dot
        cv2.circle(
            frame,
            (int(track[-1][0]), int(track[-1][1])),
            5,
            color,
            -1
        )

        # Trail line
        cv2.polylines(
            frame,
            [points],
            isClosed=False,
            color=color,
            thickness=self.polyline_thickness
        )

    def get_frame_generator(self) -> Generator[bytes, None, None]:
        """
        Yields MJPEG encoded frames with bounding boxes. Runs at high FPS independently of YOLO.
        """
        while self.running:
            if self.latest_frame is None:
                time.sleep(0.01)
                continue
            
            frame = self.latest_frame.copy()
            
            with self.box_lock:
                current_boxes = list(self.latest_boxes)
                
            for box, track_id, class_id in current_boxes:
                self.draw_bbox(frame, box, track_id, class_id)
                self.draw_trail(frame, box, track_id, class_id)
            
            # Overlay Counting Logic
            cv2.putText(frame, f"Adults (Current): {self.counter.current_adults}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Children (Current): {self.counter.current_children}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, f"Total Adults: {self.counter.total_daily_adults}", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Total Children: {self.counter.total_daily_children}", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            if self.counter.is_overcrowded():
                cv2.putText(frame, "OVERCROWDING ALERT!", (10, 160),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
            if not ret:
                continue
            
            frame_bytes = buffer.tobytes()
            yield frame_bytes
            
            # Cap the stream itself to roughly 30 FPS to save bandwidth
            time.sleep(1 / 30)

    def release(self):
        self.running = False
        if hasattr(self, 'capture_thread') and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=1.0)
        if hasattr(self, 'yolo_thread') and self.yolo_thread.is_alive():
            self.yolo_thread.join(timeout=1.0)
        if self.cap.isOpened():
            self.cap.release()
