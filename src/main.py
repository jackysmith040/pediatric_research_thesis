from nicegui import app, ui, run
import asyncio


from src.state.telemetry import TelemetryState
from src.engine.tracker_manager import TrackerManager
from src.engine.counter import Counter
from src.engine.detector import Detector
from src.engine.config import settings
from fastapi import Response
from fastapi.responses import StreamingResponse

from src.ui.dashboard import register_dashboard
from src.ui.landing import register_landing
from src.ui.evaluation import register_evaluation

# Global State & Engine
telemetry_state = TelemetryState()
tracker_manager = TrackerManager(expiry_seconds=settings.ID_EXPIRY_SECONDS)
counter = Counter(tracker_manager=tracker_manager, state=telemetry_state)
detector = None

@app.on_startup
def start_engine():
    global detector
    detector = Detector(counter=counter)

@app.on_shutdown
def stop_engine():
    if detector:
        detector.release()

from fastapi.responses import StreamingResponse

@app.get('/camera/stream')
async def camera_stream():
    async def generate_frames():
        while True:
            if detector is None:
                await asyncio.sleep(0.1)
                continue
            
            frame_bytes = await run.io_bound(detector.get_latest_jpeg_bytes)
            if frame_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                await asyncio.sleep(0.033)
            else:
                await asyncio.sleep(0.033)

    return StreamingResponse(
        generate_frames(), 
        media_type='multipart/x-mixed-replace; boundary=frame',
        headers={
            "Cache-Control": "no-cache, private",
            "Pragma": "no-cache"
        }
    )

# Register UI Pages
register_landing()
register_dashboard(telemetry_state, lambda: detector)
register_evaluation(telemetry_state, lambda: detector)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Pediatric Clinical Command Center")
