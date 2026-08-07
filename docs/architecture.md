# Architecture Decisions & Methodology

This document outlines the core architecture and development methodology for **The Invisible Child** project.

## The NiceGUI Monolith Pivot

Previously, the project operated on a decoupled Dual-Stack Architecture (FastAPI + Laravel). To dramatically simplify deployment and reduce latency, the system was refactored into a single **Python Monolith** using NiceGUI.

### 1. Unified Python Engine
- **CV Pipeline:** We utilize `YOLOv26` (via the Ultralytics library) for high-accuracy pediatric vs. adult classification and bounding-box tracking.
- **Zero-Latency Threading:** A standard synchronous OpenCV loop blocks the video feed every time YOLO runs inference, causing stutter. We use a decoupled thread pattern where the *camera capture thread* continuously drains the buffer (`CAP_PROP_BUFFERSIZE = 1`) to ensure the absolute most recent frame is captured. The *inference thread* runs in parallel, overlaying the latest available data onto the stream.
- **In-Memory State (Pydantic):** Instead of posting telemetry data to a REST API, the YOLO CV engine directly updates a shared `TelemetryState` Pydantic model. 

### 2. Clinical Command Center UI
- **Why NiceGUI?** NiceGUI runs on FastAPI, allowing us to serve the MJPEG video stream natively while providing a reactive, Python-driven frontend for the telemetry data.
- **Real-Time Data:** The `TelemetryState` is actively bound to the frontend components. A background `ui.timer` automatically reflects the absolute latest adult/child counts directly from the CV engine memory without WebSockets or XHR overhead.

## The "Impeccable" UI/UX Methodology

Based on the `impeccable` design specifications:
- **Clinical Editorial Aesthetic:** The UI utilizes deep cinematic backgrounds (`slate-950`), precise typography (Inter), and very deliberate use of `slate-900` cards and `indigo-600` accents.
- **Professional Landing Page:** The landing page communicates clinical impact through a strict, serious aesthetic, shedding "marketing" fluff in favor of hard technical data and transparency.

## Senior Stable Delivery

The development followed the strict `senior-stable-delivery` lifecycle:
- **No Feature Creep:** Enhancements were strictly triaged using Rabit Auditor.
- **Modular Packaging:** The monolith is cleanly separated into `src/ui`, `src/engine`, and `src/state` to ensure it can be adapted easily.
