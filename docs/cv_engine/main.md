# 🚀 CV Engine: `main.py`

## What does `main.py` do?
This is the entry point of the entire Computer Vision Engine. When you run `uvicorn app.main:app`, this is the file that executes.

It serves two main purposes:
1. **Wiring everything together:** It creates the `TrackerManager`, hands it to the `Counter`, hands the `Counter` to the `Detector`, and hands the `Counter` to the `TelemetryDispatcher`. It's the grand architect that makes sure all the separate puzzle pieces are connected.
2. **Running the FastAPI Server:** It defines the web server (`app = FastAPI()`) and maps out the URL routes. 

### The Lifespan Event
In modern FastAPI, background tasks (like our Telemetry sender) should be managed via a `lifespan` context manager. When the server boots up, the lifespan event starts the `TelemetryDispatcher`. When you press `Ctrl+C` to kill the server, the lifespan event politely shuts down the telemetry loop and the camera threads so they don't crash or get stuck in memory.

---

### 🧸 Explain Like I'm 5 (ELI5)
Think of `main.py` as the Manager of a restaurant. 
The Manager doesn't cook the food (that's `detector.py`), and the Manager doesn't deliver the food (that's `telemetry.py`). But in the morning, the Manager is the one who unlocks the doors, tells the Chef to go to the kitchen, tells the Waiter to go to the tables, and flips the sign on the door to "OPEN". At night, the Manager tells everyone to stop working and locks the doors.

---

### 👩‍💻 How to Contribute
If you want to add a brand new API route to the Python engine (for example, `/api/status` to check if the camera is healthy), you would add it right here in `main.py`. Just write a function with `@app.get("/api/status")` above it!
