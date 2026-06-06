# 🧮 CV Engine: `counter.py`

## What does `counter.py` do?
The `counter.py` file contains the `Counter` class. This class is the "accountant" of the CV Engine. While other parts of the system are busy looking at the video and drawing boxes, the `Counter` is purely focused on the math.

### Key Responsibilities:
1. **Keeping Score:** It holds the integers for `current_adults`, `current_children`, `total_daily_adults`, and `total_daily_children`.
2. **Processing Detections:** The `process_detection()` method is called every time the AI spots someone. It checks with the `tracker_manager.py` to see if this person is *new* or if we've already counted them. If they are new, it increments the daily total!
3. **Overcrowding Logic:** The `is_overcrowded()` method checks if the current number of children in the room exceeds the `WAITING_ROOM_CAPACITY` limit defined in `config.py`.

### How it works with others:
The `Counter` needs a `TrackerManager` to work. You pass the `TrackerManager` into the `Counter` when you create it. Then, whenever the `Counter` needs to know exactly how many people are in the room *right now*, it just asks the `TrackerManager` via the `update_current_counts()` method.

---

### 🧸 Explain Like I'm 5 (ELI5)
Imagine you are standing at the door of a party with a clicker in each hand. The AI (the bouncer) points to someone and says "Hey, I see a child!" 
You (the Counter) look at your notebook to see if you've counted that exact child before. If they just arrived, you click your counter +1. If they were already here and just walked past you again, you ignore them. You also keep an eye on the maximum capacity of the room; if too many people enter, you press the big red "OVERCROWDED" alarm button!

---

### 👩‍💻 How to Contribute
If you want to add new logic—for example, sending a warning if there are zero adults but many children (unsupervised minors)—you would write that logic right here in `counter.py`. Add a new method like `is_unsupervised()` and have it return `True` if `current_adults == 0` and `current_children > 0`.
