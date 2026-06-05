import logging
from app.tracker_manager import TrackerManager
from app.config import settings

logger = logging.getLogger(__name__)

class Counter:
    def __init__(self, tracker_manager: TrackerManager):
        self.tracker_manager = tracker_manager
        
        # State
        self.total_daily_adults = 0
        self.total_daily_children = 0
        
    @property
    def current_adults(self) -> int:
        """Dynamically compute the current adults based on active tracker memory."""
        active_ids = self.tracker_manager.get_active_ids()
        return sum(1 for class_id in active_ids.values() if class_id == settings.ADULT_CLASS_ID)

    @property
    def current_children(self) -> int:
        """Dynamically compute the current children based on active tracker memory."""
        active_ids = self.tracker_manager.get_active_ids()
        return sum(1 for class_id in active_ids.values() if class_id == settings.CHILD_CLASS_ID)

    def process_detection(self, track_id: int, class_id: int):
        """
        Process a single detection track.
        """
        is_new = self.tracker_manager.update_id(track_id, class_id)
        
        if is_new:
            if class_id == settings.ADULT_CLASS_ID:
                self.total_daily_adults += 1
            elif class_id == settings.CHILD_CLASS_ID:
                self.total_daily_children += 1

    def is_overcrowded(self) -> bool:
        """
        Check if pediatric alert threshold is reached.
        """
        if settings.WAITING_ROOM_CAPACITY <= 0:
            return False
        
        child_percentage = (self.current_children / settings.WAITING_ROOM_CAPACITY) * 100
        return child_percentage >= settings.PEDIATRIC_ALERT_THRESHOLD_PERCENT
