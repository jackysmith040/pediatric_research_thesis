import asyncio
import logging
from datetime import datetime
from app.config import settings
from app.counter import Counter

logger = logging.getLogger(__name__)

class TelemetryDispatcher:
    def __init__(self, counter: Counter):
        self.counter = counter
        self.is_running = False

    async def start(self):
        """Starts the background telemetry loop (logging to terminal)."""
        self.is_running = True
        logger.info("Starting telemetry dispatcher (logging to terminal)")
        
        while self.is_running:
            payload = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "camera_id": settings.CAMERA_ID,
                "current_adults": self.counter.current_adults,
                "current_children": self.counter.current_children,
                "total_daily_adults": self.counter.total_daily_adults,
                "total_daily_children": self.counter.total_daily_children,
                "overcrowding_alert": self.counter.is_overcrowded()
            }
            
            logger.info(
                f"[TELEMETRY] {payload['timestamp']} | "
                f"Camera: {payload['camera_id']} | "
                f"Adults: {payload['current_adults']} (total: {payload['total_daily_adults']}) | "
                f"Children: {payload['current_children']} (total: {payload['total_daily_children']}) | "
                f"Alert: {'YES' if payload['overcrowding_alert'] else 'no'}"
            )
            
            await asyncio.sleep(settings.TELEMETRY_INTERVAL_SECONDS)

    def stop(self):
        """Stops the telemetry loop."""
        self.is_running = False
        logger.info("Stopping telemetry dispatcher.")
