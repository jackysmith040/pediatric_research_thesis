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
The primary challenge of the CV Engine was avoiding video stream stutter caused by blocking inference calls.
- **Error Encountered:** OpenCV's `VideoCapture` would buffer 3 to 5 frames, so processing an older frame meant the UI video feed looked like a slow-motion slideshow.
- **The Fix:** We implemented a two-thread decouple: The Capture Thread continuously drains `cv2` via a `CAP_PROP_BUFFERSIZE = 1` property so it only holds the most recent frame, while the Inference Thread pulls only the latest frame, processes it, and updates bounding box coordinates. This successfully created a zero-latency feel on the stream.

## Phase 3: The Architecture Pivot (NiceGUI Monolith)
The project initially decoupled the logic entirely (Laravel for the UI Dashboard, and FastAPI for the CV engine).
- **The Problem:** The Laravel Reverb architecture introduced massive overhead. It required a separate server, constant network requests across localhost, and bloated the tech stack.
- **The Pivot:** We transitioned the entire UI over to **NiceGUI**, effectively uniting the front-end dashboard and the YOLO backend into a **Single Python Monolith**.
- **The Refactor:** The CV Engine was integrated into a unified `src/` directory package (`src/ui`, `src/engine`, `src/state`). The complex WebSocket telemetry bridge was replaced with a simple Pydantic `TelemetryState` model acting as a shared in-memory dictionary.
- **The Result:** Massive performance gains, instant reactivity, and a much cleaner developer experience.

## Phase 4: Senior Stable Delivery & Impeccable Design
- Instead of using a simple generic landing page, an Impeccable design system was applied across the board (`slate-950` dark themes with `indigo-600` accents).
- The system is now 100% Python, robust, clinical, and completely stable.
