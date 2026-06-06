# 🧠 CV Engine: `tracker_manager.py`

## What does `tracker_manager.py` do?
This file contains the `TrackerManager` class, which handles the short-term memory of the system. 

When YOLO (the AI) detects a person, it assigns them a random ID (e.g., Person #42). As long as Person #42 stays in the camera frame, YOLO keeps reporting "I see Person #42!". 
But what happens when Person #42 walks out the door? YOLO stops reporting them, but unless we explicitly delete them from our memory, our "current people in room" count will never go down.

### Key Mechanisms
1. **`update_id()`:** When the AI spots someone, we update their `last_seen` timestamp in our memory dictionary. We also check if this is the very first time we've seen them (returning `True` if they are new, which tells the `Counter` to add +1 to the daily total).
2. **`clean_expired_ids()`:** This method loops through everyone in memory. If someone hasn't been seen for `expiry_seconds` (usually 30 seconds), it deletes them. This ensures the "current adults/children" metric drops back down when people leave the waiting room.

---

### 🧸 Explain Like I'm 5 (ELI5)
Imagine you are playing hide-and-seek. You have a list of all your friends. Every time you spot a friend, you write the current time next to their name. 
Every few seconds, you look at your list. If you haven't seen Jimmy for 30 whole seconds, you assume Jimmy went home, so you cross his name off the list. The `TrackerManager` is that list!

---

### 👩‍💻 How to Contribute
If you wanted to implement a system that detects "loitering" (e.g., someone who has been standing in the exact same spot for 4 hours), you could add a `first_seen` timestamp to the memory dictionary in `tracker_manager.py`, and write a method to calculate how long `current_time - first_seen` is!
