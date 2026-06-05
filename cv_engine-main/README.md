# Pediatric Patient Counting - CV Engine

This is the independent Python microservice responsible for real-time Computer Vision analysis using Ultralytics YOLO and FastAPI. It tracks pediatric vs adult patients, maintains an ID-based count, streams an MJPEG video feed, and dispatches telemetry to the central dashboard.

## Requirements

- Python 3.11+
- A compatible webcam or video source

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or venv\Scripts\activate on Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

You can configure the application via a `.env` file or environment variables. By default, it expects:
- `VIDEO_SOURCE=0` (Default webcam)
- `MODEL_PATH=models/best.pt` (Will fallback to downloading `yolov8n.pt` if missing)

## Running the Application

Start the FastAPI server via Uvicorn on port 5000:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

## Features
- **Video Feed**: Access the live MJPEG stream at `http://127.0.0.1:5000/video_feed`.
- **Telemetry**: It automatically sends an HTTP POST with patient counts to the configured Laravel Restify endpoint (`http://127.0.0.1:8000/api/restify/traffic-logs`) every 3 seconds.
# cv_engine
