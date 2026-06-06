# 📡 CV Engine: `telemetry.py`

## What does `telemetry.py` do?
This file contains the `TelemetryDispatcher`. Its entire purpose is to take the math data from `counter.py` and push it over the internet to the Laravel Dashboard.

### Asynchronous Magic (Asyncio)
If the Python engine paused to wait for the Laravel server to respond every time it sent data, the video would freeze. To prevent this, `telemetry.py` uses Python's `asyncio` and `httpx`. It runs an asynchronous `start()` loop in the background. Every 3 seconds (defined in `config.py`), it grabs the numbers, sends a JSON package, and immediately goes back to sleep without blocking the main program.

### Fail-Safe Architecture
If the Laravel Dashboard is turned off or crashes, `telemetry.py` catches the error (using `try...except httpx.RequestError`). It simply prints an error to the console and tries again 3 seconds later. It will never crash the CV Engine just because the web server is down!

---

### 🧸 Explain Like I'm 5 (ELI5)
Imagine you are playing a video game on the couch, and your mom is in the kitchen. Every 3 minutes, you yell out your current high score. If she yells back "Great job!", awesome. If she is outside and doesn't hear you, you don't stop playing the video game—you just shrug and yell your score again 3 minutes later. The `TelemetryDispatcher` is the kid yelling the score, and Laravel is the mom in the kitchen.

---

### 👩‍💻 How to Contribute
If you want to send new types of data to the dashboard—for example, the current temperature of the waiting room, or the average wait time—you would add that data to the `payload` dictionary inside the `start()` method in this file (and update the Laravel API to accept it!).
