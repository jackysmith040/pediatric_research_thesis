# 🛠️ CV Engine: `config.py`

Welcome to the **Computer Vision (CV) Engine**! If you're new here, don't worry—we've structured everything so it's easy to read. 

## What does `config.py` do?
This file acts as the "brain's instruction manual". In any application, you have things that might change depending on where the app is running (like passwords, camera URLs, or server ports). Instead of hardcoding these directly into the code, we put them in a `.env` file. `config.py` reads that `.env` file and makes those variables safely accessible to the rest of the Python code.

It uses a library called `pydantic_settings`. This is awesome because it automatically validates the data. If a setting is supposed to be a number (like `WAITING_ROOM_CAPACITY`), Pydantic ensures it's actually an integer.

### Key Sections:
- **Model Configuration:** Tells the app where the YOLO neural network file is located (`MODEL_PATH`) and how confident the AI needs to be before it counts a person (`CONFIDENCE_THRESHOLD`).
- **Tracking Configuration:** Decides how long the system should remember someone after they walk off-camera (`ID_EXPIRY_SECONDS`).
- **Video Feed:** The URL or ID of the camera we are watching (`VIDEO_SOURCE`).
- **Telemetry:** Where and how often we send our data to the Laravel Dashboard (`TELEMETRY_ENDPOINT`).

---

### 🧸 Explain Like I'm 5 (ELI5)
Imagine you're building a Lego spaceship. `config.py` is the instruction booklet. It doesn't actually fly the spaceship (that's the rest of the code), but it tells you exactly what color bricks to use, how many thrusters it has, and who the pilot is. If you want to change the pilot from "Bob" to "Alice", you just change it in the instructions, and the whole spaceship knows what to do!

---

### 👩‍💻 How to Contribute
If you ever need to add a new environment variable (for example, `ENABLE_NIGHT_VISION`), you would:
1. Add it to the `.env` file.
2. Open `config.py` and add it to the `Settings` class: `ENABLE_NIGHT_VISION: bool = bool(os.getenv("ENABLE_NIGHT_VISION", "False"))`.
3. Now any other Python file can use `settings.ENABLE_NIGHT_VISION`!
