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
from src.engine.config import settings
from src.engine.counter import Counter
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
        # Tracking History UI
        self.track_history = defaultdict(lambda: [])
        self.rect_width = 1
        self.font = 0.4
        self.text_width = 1
        self.padding = 6
        self.margin = 6
        self.circle_thickness = 3
        self.polyline_thickness = 1

    def _capture_loop(self):
        """Continuously drain the buffer to ensure we always have the absolute latest frame."""
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.latest_frame = cv2.flip(frame, 1)
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
            self.counter.cleanup_lost_tracks()

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
                        self.counter.process_detection(track_id, class_id, box)
                        new_boxes.append((box, track_id, class_id))
            
            with self.box_lock:
                self.latest_boxes = new_boxes

    def draw_bbox(self, frame, box, track_id, class_id):
        """Draw modern sci-fi bounding box with corner brackets and translucent fill."""
        x1, y1, x2, y2 = map(int, box)
        color = colors(int(class_id), True)

        # 1. Semi-transparent fill
        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
        cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)

        # 2. Corner brackets
        length = 15
        thickness = 2
        # Top-left
        cv2.line(frame, (x1, y1), (x1 + length, y1), color, thickness)
        cv2.line(frame, (x1, y1), (x1, y1 + length), color, thickness)
        # Top-right
        cv2.line(frame, (x2, y1), (x2 - length, y1), color, thickness)
        cv2.line(frame, (x2, y1), (x2, y1 + length), color, thickness)
        # Bottom-left
        cv2.line(frame, (x1, y2), (x1 + length, y2), color, thickness)
        cv2.line(frame, (x1, y2), (x1, y2 - length), color, thickness)
        # Bottom-right
        cv2.line(frame, (x2, y2), (x2 - length, y2), color, thickness)
        cv2.line(frame, (x2, y2), (x2, y2 - length), color, thickness)

        # 3. Label with modern translucent background
        class_name = "Adult" if class_id == settings.ADULT_CLASS_ID else "Child"
        label = f"{class_name} [{track_id}]"
        
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        
        # Text background overlay
        text_overlay = frame.copy()
        cv2.rectangle(text_overlay, (x1, y1 - th - 8), (x1 + tw + 8, y1), color, -1)
        cv2.addWeighted(text_overlay, 0.6, frame, 0.4, 0, frame)
        
        cv2.putText(frame, label, (x1 + 4, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    def draw_trail(self, frame, box, track_id, class_id):
        """Draw fading tracking trail with a sci-fi centroid dot."""
        x1, y1, x2, y2 = map(int, box)
        track = self.track_history[track_id]
        
        cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
        track.append((cx, cy))
        
        if len(track) > 30:  # Shorter, cleaner trail
            track.pop(0)

        color = colors(int(class_id), True)
        
        # Draw fading trail
        if len(track) > 1:
            for i in range(1, len(track)):
                thickness = int(np.sqrt(float(i)) * 0.8) + 1
                cv2.line(frame, track[i - 1], track[i], color, thickness)
                
        # Draw current centroid (double ring effect)
        cv2.circle(frame, (cx, cy), 3, (255, 255, 255), -1)
        cv2.circle(frame, (cx, cy), 6, color, 1)

    def get_latest_jpeg_bytes(self) -> bytes:
        """
        Returns a single MJPEG encoded frame with bounding boxes. Runs independently of YOLO.
        """
        if self.latest_frame is None:
            return None
        
        frame = self.latest_frame.copy()
        
        with self.box_lock:
            current_boxes = list(self.latest_boxes)
            
        for box, track_id, class_id in current_boxes:
            self.draw_bbox(frame, box, track_id, class_id)
            self.draw_trail(frame, box, track_id, class_id)
        


        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
        if not ret:
            return None
        
        return buffer.tobytes()

    def release(self):
        self.running = False
        if hasattr(self, 'capture_thread') and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=1.0)
        if hasattr(self, 'yolo_thread') and self.yolo_thread.is_alive():
            self.yolo_thread.join(timeout=1.0)
        if self.cap.isOpened():
            self.cap.release()
