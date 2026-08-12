import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Model Configuration
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/expbetter.pt")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.45"))
    IOU_THRESHOLD: float = float(os.getenv("IOU_THRESHOLD", "0.4"))
    
    # Tracking Configuration
    TRACKER_CONFIG: str = os.getenv("TRACKER_CONFIG", "bytetrack.yaml")
    ID_EXPIRY_SECONDS: int = int(os.getenv("ID_EXPIRY_SECONDS", "30"))
    UNTRACKED_SPATIAL_MATCH_RADIUS: float = float(os.getenv("UNTRACKED_SPATIAL_MATCH_RADIUS", "40.0"))

    # Video Feed Configuration
    # Defaults to local webcam (0)
    VIDEO_SOURCE: str = os.getenv("VIDEO_SOURCE", "0")

    CAMERA_ID: str = os.getenv("CAMERA_ID", "outpatient_waiting_cctv_01")
    # Overcrowding Logic
    WAITING_ROOM_CAPACITY: int = int(os.getenv("WAITING_ROOM_CAPACITY", "50"))
    PEDIATRIC_ALERT_THRESHOLD_PERCENT: float = float(os.getenv("PEDIATRIC_ALERT_THRESHOLD_PERCENT", "30.0"))

    # Detection & Performance Configuration
    PEDIATRIC_CONF_THRESHOLD: float = float(os.getenv("PEDIATRIC_CONF_THRESHOLD", "0.30"))
    MAX_FRAME_WIDTH: int = int(os.getenv("MAX_FRAME_WIDTH", "1280"))

    # Class mappings (expbetter.pt trained weights: 0=Adult, 1=Child)
    ADULT_CLASS_ID: int = int(os.getenv("ADULT_CLASS_ID", "0"))
    CHILD_CLASS_ID: int = int(os.getenv("CHILD_CLASS_ID", "1"))

    class Config:
        env_file = ".env"

settings = Settings()
