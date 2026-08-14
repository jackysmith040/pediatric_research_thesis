import cv2
import os
import logging
import numpy as np
import torch
import threading
import time
import math
import ultralytics.nn.tasks
from collections import defaultdict
from ultralytics import YOLO
from ultralytics.utils.plotting import colors
from src.engine.config import settings, PRESET_MODELS

from src.engine.counter import Counter
from typing import Generator

# Security override for PyTorch 2.6+ loading YOLO weights
_original_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = _patched_load

logger = logging.getLogger(__name__)


import supervision as sv
from src.engine.stream_resolver import StreamResolver
from src.engine.tracker_engine import MultiTrackerEngine


class Detector:
    @staticmethod
    def apply_clahe(frame: np.ndarray, clip_limit: float = 2.0, tile_grid_size: int = 8) -> np.ndarray:
        """
        Applies Contrast Limited Adaptive Histogram Equalization (CLAHE) in the LAB color space.
        Enhances contrast in low-light clinical triage environments without shifting color balance.
        """
        if frame is None or frame.size == 0:
            return frame
        try:
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l_channel, a_channel, b_channel = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=float(clip_limit), tileGridSize=(int(tile_grid_size), int(tile_grid_size)))
            cl = clahe.apply(l_channel)
            limg = cv2.merge((cl, a_channel, b_channel))
            return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        except Exception as e:
            logger.error(f"Error applying CLAHE preprocessing: {e}")
            return frame
    def __init__(self, counter: Counter):
        self.counter = counter
        self.model_lock = threading.Lock()
        
        # Initialize YOLO Model dynamically with fallback cascade
        self._init_model(settings.MODEL_PATH)

        # Initialize Roboflow Supervision Multi-Tracker Engine & Annotators
        self.tracker_engine = MultiTrackerEngine(initial_mode=settings.DEFAULT_TRACKER_MODE)
        self.current_tracker_status_label = "ByteTrack [Auto]"
        
        self.box_annotator = sv.BoundingBoxAnnotator(thickness=2)
        self.label_annotator = sv.LabelAnnotator(text_scale=0.5, text_thickness=1)
        self.trace_annotator = sv.TraceAnnotator(trace_length=30, thickness=2)



        # Dynamic Video Source & Lock

        self.source_lock = threading.Lock()
        self.current_source_input = settings.VIDEO_SOURCE
        self.current_source_label = "Webcam 0"
        self.current_source_type = "webcam"
        self.last_error = None
        self.is_webcam = True
        self.cap = None

        # Initialize video source
        self._init_capture(settings.VIDEO_SOURCE)

        # Threading for Decoupled Architecture
        self.latest_frame = None
        self.latest_boxes = []
        self.latest_jpeg_bytes = None
        self.box_lock = threading.Lock()
        self.running = True
        self._synthetic_id_counter = 10000
        
        # Thread 1: Camera Capture
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()

        # Thread 2: YOLO Inference
        self.yolo_thread = threading.Thread(target=self._yolo_loop, daemon=True)
        self.yolo_thread.start()

        # Store model class names
        self.names = self.model.names
        self.uses_coco_person = len(self.names) == 1 and 'person' in str(self.names.get(0, '')).lower()
        if self.uses_coco_person:
            logger.info("Generic COCO person model detected. Height heuristics active for pediatric detection.")

        # Tracking History UI
        self.track_history = defaultdict(lambda: [])
        self.rect_width = 1
        self.font = 0.4
        self.text_width = 1
        self.padding = 6
        self.margin = 6
        self.circle_thickness = 3
        self.polyline_thickness = 1

    def _resolve_track_id(self, box, track_id: int, class_id: int, claimed_ids: set) -> int:
        """
        Resolves missing/unassigned track IDs (-1) by matching against existing active centroids
        (excluding IDs already claimed in the current frame) or assigning a stable synthetic ID.
        """
        if track_id != -1 and track_id not in claimed_ids:
            return track_id

        cx = (box[0] + box[2]) / 2.0
        cy = (box[1] + box[3]) / 2.0

        best_match_id = None
        min_dist = settings.UNTRACKED_SPATIAL_MATCH_RADIUS

        for active_id, (acx, acy, aclass_id) in self.counter.active_centroids.items():
            if aclass_id == class_id and active_id not in claimed_ids:
                dist = math.hypot(cx - acx, cy - acy)
                if dist < min_dist:
                    min_dist = dist
                    best_match_id = active_id

        if best_match_id is not None:
            return best_match_id

        self._synthetic_id_counter += 1
        return self._synthetic_id_counter

    def _init_capture(self, source_input: str) -> tuple[bool, str]:
        """Resolves and opens a video capture source thread-safely."""
        cap, label, err = StreamResolver.resolve_stream_source(source_input)
        if err or cap is None:
            err_msg = err or f"Failed to open video source: {label}"
            self.last_error = err_msg
            logger.error(f"Stream resolution error for '{source_input}': {err_msg}")
            return False, err_msg

        with self.source_lock:
            if hasattr(self, 'cap') and self.cap is not None and self.cap.isOpened():
                self.cap.release()
            
            self.cap = cap
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            source_str = str(source_input).strip()
            self.is_webcam = source_str == "" or source_str.isdigit()
            
            if self.is_webcam:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

            self.current_source_input = source_input
            self.current_source_label = label
            self.last_error = None
            logger.info(f"Successfully opened stream source: {label}")
            return True, label

    def change_source(self, source_input: str) -> tuple[bool, str]:
        """Dynamic runtime method to switch video input sources."""
        return self._init_capture(source_input)

    def _init_model(self, model_path: str) -> tuple[bool, str]:
        """Loads a YOLO model with dynamic fallback cascade and class mapping resolution."""
        target_path = str(model_path).strip()
        selected_path = None
        
        if os.path.exists(target_path):
            selected_path = target_path
        else:
            # Fallback cascade
            fallbacks = [
                settings.MODEL_PATH,
                "models/fine_tuned/pediatric-model.pt",
                "models/fine_tuned/pediatric-smaller-dataset-trained.pt",
                "models/fine_tuned/pediatric-kids-only.pt",
                "models/base_model/yolo26s.pt",
                "models/yolov8n.pt",
                "yolov8n.pt"
            ]
            for fb in fallbacks:
                if os.path.exists(fb):
                    selected_path = fb
                    break
        
        if not selected_path:
            selected_path = "yolov8n.pt"

        try:
            logger.info(f"Loading YOLO model weights from {selected_path}")
            model_instance = YOLO(selected_path)
            
            with getattr(self, 'model_lock', threading.Lock()):
                self.model = model_instance
                self.current_model_path = selected_path
                self.names = self.model.names
                
                # Dynamic class resolution
                self.child_class_id = settings.CHILD_CLASS_ID
                self.adult_class_id = settings.ADULT_CLASS_ID
                
                for idx, name in self.names.items():
                    n = str(name).lower()
                    if 'child' in n or 'kid' in n or 'pediatric' in n:
                        self.child_class_id = idx
                    elif 'adult' in n:
                        self.adult_class_id = idx
                
                self.uses_coco_person = len(self.names) == 1 and 'person' in str(self.names.get(0, '')).lower()
                if 'person' in str(self.names.get(0, '')).lower() and len(self.names) > 10:
                    self.uses_coco_person = True

                filename = os.path.basename(selected_path)
                self.current_model_label = filename
                
            logger.info(f"Successfully initialized model '{filename}' (Child Class ID: {self.child_class_id}, Adult Class ID: {self.adult_class_id})")
            return True, f"Loaded model: {filename}"
        except Exception as e:
            err_msg = f"Failed to load model from {target_path}: {e}"
            logger.error(err_msg)
            return False, err_msg

    def change_model(self, model_path: str) -> tuple[bool, str]:
        """Dynamic runtime method to switch YOLO model weights."""
        return self._init_model(model_path)

    def change_tracker_mode(self, mode: str) -> tuple[bool, str]:
        """Dynamic runtime method to switch tracking algorithms or auto mode."""
        success, msg = self.tracker_engine.set_mode(mode)
        if success:
            self.current_tracker_status_label = self.tracker_engine.get_info()["status_label"]
        return success, msg



    def _capture_loop(self):
        """Continuously drain buffer and stream frames. Auto-loops finite video files/streams."""
        while self.running:
            with self.source_lock:
                if self.cap is None or not self.cap.isOpened():
                    time.sleep(0.05)
                    continue

                ret, frame = self.cap.read()

            if ret:
                # Downscale high-resolution video frames (e.g. 1080p/4K) to MAX_FRAME_WIDTH for smooth 30 FPS
                h, w = frame.shape[:2]
                if w > settings.MAX_FRAME_WIDTH:
                    new_h = int(h * (settings.MAX_FRAME_WIDTH / float(w)))
                    frame = cv2.resize(frame, (settings.MAX_FRAME_WIDTH, new_h), interpolation=cv2.INTER_AREA)

                # Mirror flip for live webcam, original orientation for streams & video files
                self.latest_frame = cv2.flip(frame, 1) if self.is_webcam else frame
                if not self.is_webcam:
                    time.sleep(0.015)  # Pace local file reads smoothly
            else:
                # EOF reached on video stream/file -> rewind to frame 0 for continuous looping test
                with self.source_lock:
                    if self.cap is not None and not self.is_webcam:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                time.sleep(0.01)

    def _yolo_loop(self):
        """Continuously run CLAHE preprocessing, YOLO inference, and Supervision ByteTrack multi-object tracking."""
        while self.running:
            if self.latest_frame is None:
                time.sleep(0.01)
                continue
                
            frame = self.latest_frame.copy()
            frame_h = float(frame.shape[0])
            
            # Apply CLAHE Preprocessing in LAB color space if enabled
            proc_frame = self.apply_clahe(frame, settings.CLAHE_CLIP_LIMIT, settings.CLAHE_TILE_GRID_SIZE) if settings.ENABLE_CLAHE else frame
            
            # Clean expired IDs from memory
            self.counter.tracker_manager.clean_expired_ids()
            self.counter.cleanup_lost_tracks()

            # Run YOLO prediction
            results = self.model.predict(
                proc_frame, 
                conf=settings.PEDIATRIC_CONF_THRESHOLD,
                iou=settings.IOU_THRESHOLD,
                imgsz=480,
                verbose=False
            )

            new_boxes = []
            if results and len(results) > 0 and len(results[0].boxes) > 0:
                # Convert Ultralytics results to Supervision Detections
                detections = sv.Detections.from_ultralytics(results[0])
                
                # Update Multi-Tracker Engine with detections and frame for scene analysis
                detections, status_label = self.tracker_engine.update_with_detections(detections, frame)
                self.current_tracker_status_label = status_label

                boxes = detections.xyxy

                raw_track_ids = detections.tracker_id
                if raw_track_ids is None:
                    track_ids = [-1] * len(boxes)
                else:
                    track_ids = [int(tid) if tid is not None else -1 for tid in raw_track_ids]
                
                class_ids = detections.class_id.astype(int).tolist() if detections.class_id is not None else [0] * len(boxes)

                claimed_ids = set()
                for raw_id in track_ids:
                    if raw_id != -1:
                        claimed_ids.add(raw_id)
                
                for box, raw_track_id, raw_class_id in zip(boxes, track_ids, class_ids):
                    target_class_id = raw_class_id

                    child_cls = getattr(self, 'child_class_id', settings.CHILD_CLASS_ID)
                    adult_cls = getattr(self, 'adult_class_id', settings.ADULT_CLASS_ID)

                    # For single-class person models (e.g. COCO 0='person'), apply scale height heuristic
                    if self.uses_coco_person and raw_class_id == 0:
                        box_h = float(box[3] - box[1])
                        # If person bounding box is under 40% of frame height, classify as Child (pediatric)
                        if box_h / max(1.0, frame_h) < 0.40:
                            target_class_id = child_cls
                        else:
                            target_class_id = adult_cls

                    if target_class_id in [child_cls, adult_cls]:
                        resolved_id = self._resolve_track_id(box, raw_track_id, target_class_id, claimed_ids)
                        claimed_ids.add(resolved_id)
                        self.counter.process_detection(resolved_id, target_class_id, box)
                        new_boxes.append((box, resolved_id, target_class_id))
            
            with self.box_lock:
                self.latest_boxes = new_boxes


    def draw_bbox(self, frame, box, track_id, class_id, class_index=None):
        """Draw modern sci-fi bounding box with corner brackets, translucent fill, and sequential count label."""
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
        child_cls = getattr(self, 'child_class_id', settings.CHILD_CLASS_ID)
        class_name = "Child" if class_id == child_cls else "Adult"

        if class_index is not None:
            label = f"{class_name} #{class_index} [{track_id}]"
        else:
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
        Returns a single MJPEG encoded frame with synchronized bounding boxes.
        Runs independently of YOLO to guarantee smooth 30 FPS playback.
        """
        if self.latest_frame is None:
            return None
            
        frame = self.latest_frame.copy()
        
        with self.box_lock:
            current_boxes = list(self.latest_boxes)
            
        # Compute 1-based sequential indices per class sorted left-to-right (x1 coordinate)
        sorted_boxes = sorted(current_boxes, key=lambda b: float(b[0][0]))
        class_counters = defaultdict(int)
        box_indices = {}
        for box, track_id, class_id in sorted_boxes:
            class_counters[class_id] += 1
            box_indices[id(box)] = class_counters[class_id]

        for box, track_id, class_id in current_boxes:
            idx = box_indices.get(id(box))
            self.draw_bbox(frame, box, track_id, class_id, class_index=idx)
            if track_id != -1:
                self.draw_trail(frame, box, track_id, class_id)

        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 75])
        return buffer.tobytes() if ret else None

    def release(self):
        self.running = False
        if hasattr(self, 'capture_thread') and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=1.0)
        if hasattr(self, 'yolo_thread') and self.yolo_thread.is_alive():
            self.yolo_thread.join(timeout=1.0)
        if self.cap.isOpened():
            self.cap.release()
