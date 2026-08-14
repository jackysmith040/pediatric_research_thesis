# `src/engine/config.py`

## Purpose
`config.py` manages application configuration, model paths, detection thresholds, and clinical thresholds using `pydantic_settings`.

---

## Configuration Variables

| Property | Default Value | Description |
|---|---|---|
| `MODEL_PATH` | `"models/expbetter.pt"` | Path to trained YOLO object detection model weights |
| `CONFIDENCE_THRESHOLD` | `0.45` | Minimum confidence score to accept object detections |
| `IOU_THRESHOLD` | `0.40` | Intersection-over-Union threshold for Non-Maximum Suppression (NMS) |
| `TRACKER_CONFIG` | `"bytetrack.yaml"` | ByteTrack tracker configuration file |
| `ID_EXPIRY_SECONDS` | `30` | Time in seconds before unseen tracking IDs are purged from memory |
| `UNTRACKED_SPATIAL_MATCH_RADIUS` | `40.0` | Radius (pixels) for matching untracked bounding boxes (`track_id == -1`) to existing centroids |
| `VIDEO_SOURCE` | `"0"` | Video source input (Webcam index `"0"`, local file path, YouTube URL, or RTSP stream) |
| `WAITING_ROOM_CAPACITY` | `50` | Total patient capacity of monitored waiting area |
| `PEDIATRIC_ALERT_THRESHOLD_PERCENT` | `30.0` | Pediatric percentage threshold that triggers an overcrowding alert |
| `ADULT_CLASS_ID` | `0` | Model class index mapped to Adult |
| `CHILD_CLASS_ID` | `1` | Model class index mapped to Child |

---

## Environment Override (.env)

Configuration values can be overridden via `.env` file or environment variables:

```ini
MODEL_PATH=models/expbetter.pt
CONFIDENCE_THRESHOLD=0.45
WAITING_ROOM_CAPACITY=50
PEDIATRIC_ALERT_THRESHOLD_PERCENT=30.0
VIDEO_SOURCE=0
```
