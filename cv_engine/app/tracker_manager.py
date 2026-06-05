import time
from typing import Dict, Any

class TrackerManager:
    def __init__(self, expiry_seconds: int):
        self.expiry_seconds = expiry_seconds
        # Dictionary structure:
        # { id: {"last_seen": float, "class_id": int, "counted": bool} }
        self.tracked_ids: Dict[int, Dict[str, Any]] = {}

    def update_id(self, track_id: int, class_id: int) -> bool:
        """
        Updates the tracker memory with the given ID.
        Returns True if this ID is newly registered (i.e. not previously counted).
        """
        current_time = time.time()
        is_new = False
        
        if track_id not in self.tracked_ids:
            self.tracked_ids[track_id] = {
                "last_seen": current_time,
                "class_id": class_id,
                "counted": True
            }
            is_new = True
        else:
            self.tracked_ids[track_id]["last_seen"] = current_time
            # Ensure class_id doesn't flip flop by trusting the first strong detection
            # For a more advanced approach, a rolling mode over class_id can be used.
            
        return is_new

    def get_active_ids(self) -> Dict[int, int]:
        """
        Returns a dict of currently active {track_id: class_id}
        """
        return {tid: data["class_id"] for tid, data in self.tracked_ids.items()}

    def clean_expired_ids(self):
        """
        Removes IDs that have not been seen for 'expiry_seconds'.
        """
        current_time = time.time()
        expired_ids = [
            tid for tid, data in self.tracked_ids.items()
            if (current_time - data["last_seen"]) > self.expiry_seconds
        ]
        for tid in expired_ids:
            del self.tracked_ids[tid]
