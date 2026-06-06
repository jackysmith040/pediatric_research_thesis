# Architecture Decisions & Methodology

This document outlines the core architecture and development methodology for **The Invisible Child** project, derived from the original `project-plan` and iterative refinements.

## The Dual-Stack Architecture

To balance clinical-grade computer vision performance with an accessible web-based administrative dashboard, the system is split into two specialized stacks:

### 1. CV Engine (Python / FastAPI)
- **Why Python?** Python is the industry standard for neural network execution. We utilize `YOLOv26` (via the Ultralytics library) for high-accuracy pediatric vs. adult classification and bounding-box tracking.
- **Threading Strategy (Zero-Latency):** A standard synchronous OpenCV loop blocks the video feed every time YOLOv26 runs inference, causing significant stutter on IP Cameras. We implemented a decoupled thread pattern where the *camera capture thread* continuously drains the buffer (`CAP_PROP_BUFFERSIZE = 1`) to ensure the absolute most recent frame is captured. The *inference thread* runs in parallel, overlaying the latest available data onto the stream. This provides a flawless 30 FPS video feed regardless of inference speeds.
- **REST Telemetry:** The Python engine acts as an HTTP client, posting counting metrics to the Laravel API every 3 seconds.

### 2. Command Center (Laravel 13)
- **Why Laravel?** Laravel provides rock-solid data ingestion, scheduled tasks (for daily PDF reporting), and seamless real-time WebSocket capabilities.
- **Livewire & Islands Architecture:** The UI is built with Livewire 4. To prevent the real-time telemetry updates from freezing the video feed or interfering with user inputs, the `TelemetryDashboard` is wrapped in the `#[Isolate]` attribute. This encapsulates its state and XHR requests strictly to its own DOM node.
- **Laravel Reverb:** Instead of relying on expensive third-party Pusher clusters, we run our own first-party WebSocket server via Laravel Reverb. The `TelemetryController` receives API pushes from the CV engine and instantly broadcasts `TelemetryReceived` events to connected frontend clients.
- **Graceful Degradation:** Both the CV Engine stream and the Reverb WebSocket use robust Alpine.js logic to gracefully handle disconnects. The UI seamlessly swaps between a Live Feed and an "Offline State" card without crashing or showing broken image icons.

## The "Impeccable" UI/UX Methodology

Based on the `impeccable` design specifications in the `project-plan`:
- **Editorial Aesthetic:** The UI utilizes deep cinematic backgrounds (`#1c1c1e`), precise typography (Inter/Manrope), and very deliberate use of "Space Gray" and "Electric Blue" as highlight colors.
- **Story-Driven Landing Page:** Instead of a simple login wall, the landing page walks stakeholders through the clinical impact of the tool using `aos.js` scroll animations, ensuring the project resonates emotionally with laymen.

## Senior Stable Delivery

The development followed the strict `senior-stable-delivery` lifecycle:
- **No Feature Creep:** Enhancements were strictly triaged. Core functionality was prioritized over novelty.
- **Fail-Closed API:** The Laravel backend catches broadcast exceptions gracefully. If Reverb goes down, the API still returns a `200 OK` to the CV engine and logs the failure to SQLite, rather than crashing the data ingestion loop.
- **Pest & Pint:** The pipeline is continuously verified with Laravel Pint code formatting and Pest feature tests to guarantee CI/CD stability.
