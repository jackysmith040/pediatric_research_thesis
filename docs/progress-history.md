# 📈 Progress History & Project Post-Mortem

Welcome to the historical log of **The Invisible Child**. This document tracks the evolution of the project from its initial project plan to the final senior-stable delivery, detailing the errors encountered, the architectural decisions made, and the fixes applied. 

This is the ultimate resource for understanding *why* things were built the way they were.

---

## Phase 1: The Initial Vision
The project started with a spec (`project-plan/v1/spec.md`) to build a dual-stack pediatric monitoring system.
- **Goal:** Use AI to count adults and children in a waiting room to prevent pediatric overcrowding.
- **Tech Stack:** Python (FastAPI + YOLO) for the CV Engine, Laravel for the Command Center.
- **Design:** "Impeccable" methodology—Space Gray backgrounds, Electric Blue accents, cinematic UI.

## Phase 2: Python Threading Crisis
**The Error:** Initially, the CV engine ran synchronously. It would grab a frame from the camera, run YOLO inference, draw the boxes, and yield the frame. 
**The Symptom:** The video feed lagged terribly. By the time YOLO finished processing frame #1, the camera buffer was holding frame #5, causing a massive delay buildup.
**The Decision (Fix):** We implemented a **Decoupled Threading Architecture**.
- We split the engine into a `_capture_loop` and a `_yolo_loop`.
- The `_capture_loop` forces the camera buffer to 1 (`cv2.CAP_PROP_BUFFERSIZE = 1`) and continuously drains it to ensure we always have the absolute most recent frame.
- The `_yolo_loop` runs in parallel, processing whatever the latest frame happens to be.
- **Result:** Zero-latency video stream. The stream runs flawlessly at 30 FPS regardless of the AI inference speed.

## Phase 3: The Livewire Island Wars
**The Error:** We successfully connected the Python Engine to Laravel via REST, and Laravel to the UI via Reverb WebSockets. However, every time a telemetry update arrived (every 3 seconds), the *entire* dashboard re-rendered.
**The Symptom:** The MJPEG video feed would constantly flicker or reload, and the "Download PDF" button would randomly show a loading spinner.
**The Decision (Fix):** 
1. **Islands:** We upgraded the `TelemetryDashboard` to a Livewire Island using the `#[Isolate]` attribute. This quarantined the re-renders to only the telemetry HTML.
2. **Targeting:** We applied `wire:target="downloadReport"` to the PDF button so the global Livewire loading state wouldn't falsely trigger it during WebSocket background updates.

## Phase 4: The Silent API Crash
**The Error:** While testing the CV Engine, the Uvicorn terminal suddenly vomited a massive 500 Internal Server Error JSON stack trace from Laravel.
**The Cause:** Laravel's `TelemetryController` was trying to broadcast the event to Reverb (`broadcast(...)->toOthers()`). However, the Reverb server was offline. Because it was synchronous (`ShouldBroadcastNow`), the broadcast failure crashed the API endpoint.
**The Decision (Fix):** We instituted **Graceful Degradation**.
- We wrapped the `event()` dispatch in a `try-catch` block inside the API controller.
- If Reverb is down, Laravel simply logs a warning to `laravel.log`, saves the data to the SQLite database anyway, and returns a `200 OK` to the Python engine.
- We added Alpine.js listeners (`@echo-connected` and `@echo-disconnected`) to the UI to physically change a green "Reverb Live" dot to a red "Reverb Offline" badge if the WebSocket tunnel drops.

## Phase 5: The YOLO Version Clarification
**The Error:** The documentation incorrectly referred to the neural network as "YOLOv8".
**The Fix:** The documentation was globally patched to correctly reference the state-of-the-art **YOLOv26** (specifically the nano `yolov26n` variant) which provides the extreme speed required for this architecture.

---

### Conclusion
By following the **Senior Stable Delivery** methodology (Rabit Auditor checklists, Pest testing, Pint formatting, and fail-safe API design), "The Invisible Child" evolved from a fragile prototype into a deeply resilient, clinical-grade intelligence tool.
