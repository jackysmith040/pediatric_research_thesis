import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.config import settings
from app.tracker_manager import TrackerManager
from app.counter import Counter
from app.detector import Detector
from app.streamer import mjpeg_generator
from app.telemetry import TelemetryDispatcher

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Core Application State
tracker_manager = TrackerManager(expiry_seconds=settings.ID_EXPIRY_SECONDS)
counter = Counter(tracker_manager=tracker_manager)
detector = Detector(counter=counter)
telemetry = TelemetryDispatcher(counter=counter)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting CV Engine...")
    asyncio.create_task(telemetry.start())
    yield
    # Shutdown
    logger.info("Shutting down CV Engine...")
    telemetry.stop()
    detector.release()

app = FastAPI(title="Pediatric Patient CV Engine", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "CV Engine is running. Access /video_feed for the MJPEG stream."}

@app.get("/video_feed")
def video_feed():
    """
    MJPEG streaming endpoint for the live video feed.
    This bypasses JSON serialization and returns a continuous multipart byte stream.
    """
    return StreamingResponse(
        mjpeg_generator(detector),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
