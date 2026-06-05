import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Model Configuration
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/expbetter.pt")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
    IOU_THRESHOLD: float = float(os.getenv("IOU_THRESHOLD", "0.4"))
    
    # Tracking Configuration
    TRACKER_CONFIG: str = os.getenv("TRACKER_CONFIG", "botsort.yaml")
    ID_EXPIRY_SECONDS: int = int(os.getenv("ID_EXPIRY_SECONDS", "5"))

    # Video Feed Configuration
    # Defaults to local webcam (0)
    VIDEO_SOURCE: str = os.getenv("VIDEO_SOURCE", "0")

    # Telemetry Configuration
    TELEMETRY_ENDPOINT: str = os.getenv("TELEMETRY_ENDPOINT", "http://127.0.0.1:8000/api/restify/traffic-logs")
    TELEMETRY_INTERVAL_SECONDS: int = int(os.getenv("TELEMETRY_INTERVAL_SECONDS", "3"))
    CAMERA_ID: str = os.getenv("CAMERA_ID", "outpatient_waiting_cctv_01")
    
    # Overcrowding Logic
    WAITING_ROOM_CAPACITY: int = int(os.getenv("WAITING_ROOM_CAPACITY", "50"))
    PEDIATRIC_ALERT_THRESHOLD_PERCENT: float = float(os.getenv("PEDIATRIC_ALERT_THRESHOLD_PERCENT", "30.0"))

    # Class mappings (Expected: 0 for Adult, 1 for Child)
    # Using defaults for yolov8n if expbetter.pt is not provided: 0='person'
    ADULT_CLASS_ID: int = int(os.getenv("ADULT_CLASS_ID", "0"))
    CHILD_CLASS_ID: int = int(os.getenv("CHILD_CLASS_ID", "1"))

    class Config:
        env_file = ".env"

settings = Settings()
