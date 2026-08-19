# The Invisible Child: Pediatric Patient Counting with Interactive Object Detection and Dynamic Multi-Tracking in Clinical Triage Environments

**Academic Context:** Final Year Research Thesis (February 2026)  
**Author:** Jacky Smith  
**Department:** Department of Mathematics, Faculty of Physical and Computational Sciences  
**Institution:** Kwame Nkrumah University of Science and Technology (KNUST), Kumasi, Ghana  
**Repository:** [https://github.com/jackysmith040/pediatric_research_thesis.git](https://github.com/jackysmith040/pediatric_research_thesis.git)  

---

## Abstract

In resource-constrained hospital emergency departments (EDs) and outpatient triage facilities, infant and pediatric mortality is heavily exacerbated by prolonged, unmonitored waiting room delays. In such high-stress clinical environments, manual triage logs and visual headcounts consistently fail to account for the **"Invisible Child" phenomenon**—infants wrapped in swaddling cloths, carried against caregivers' torsos, or occluded in crowded waiting areas. As a consequence, pediatric patient load is systematically underestimated, leading to severe nursing shortages, delayed critical interventions, and preventable pediatric decompensation.

To resolve this critical healthcare challenge, this research designs, develops, mathematically models, and validates a real-time, edge-deployed clinical computer vision system. The system integrates deep convolutional and attention-based object detection (**YOLO architectures**) with an adaptive **Multi-Tracker Suite** (incorporating **ByteTrack**, **BoT-SORT**, **OC-SORT**, and **FastTracker**) into a unified, zero-network-serialization Python monolith powered by NiceGUI.

Key mathematical and engineering contributions include:
1. **Asynchronous Decoupled Capture-Inference Architecture:** A multithreaded design utilizing a continuous OpenCV capture buffer draining thread (`CAP_PROP_BUFFERSIZE = 1`) coupled to a background asynchronous inference worker, eliminating video streaming latency and sustaining constant 30 FPS telemetry playback.
2. **Illumination-Invariant LAB CLAHE Pipeline:** A contrast enhancement framework operating in the LAB color space that boosts feature contrast in dim triage environments without shifting critical RGB chromatic signatures.
3. **Adaptive Scene Analysis with Hysteresis Stabilization:** A dynamic switching algorithm that continuously evaluates camera motion via optical flow frame difference ($\Delta I$) and crowd occlusion density via pairwise Intersection-over-Union ($\text{IoU}_{\text{pairwise}}$), automatically routing frames to optimal tracking routines across varying triage conditions with a 3.0-second anti-flapping hysteresis barrier.
4. **Centroid Spatial Fallback & Temporal Debouncing:** A spatial Euclidean re-identification mechanism ($r \le 40.0\text{ px}$) and a 5.0-second lost-track debouncing queue that prevents identity fragmentation and double-counting during physical occlusion.
5. **High-Speed ONNX Runtime Quantization:** Model optimization achieving a **2.1x CPU inference speedup** (reducing inference latency from 59.8 ms to 28.4 ms), allowing edge deployment on low-cost clinical workstations without expensive discrete GPUs.
6. **Automated Clinical Governance:** Continuous computation of pediatric load percentage ($C_{\text{child}}\%$), automated threshold alerting ($\ge 30\%$), and automated export of structured CSV telemetry logs and formatted PDF capacity audit reports.

Extensive empirical evaluations across benchmark video datasets and live clinical simulation feeds demonstrate an overall detection accuracy of **mAP@0.5 = 0.912** on pediatric targets, a Multiple Object Tracking Accuracy (**MOTA**) of **84.6%**, an **IDF1 score of 87.2%**, and zero video lag across multi-hour stress testing. The system establishes a robust, privacy-preserving, and computationally accessible paradigm for automated pediatric capacity surveillance in modern healthcare infrastructure.

---

## 1. Introduction & Clinical Context

### 1.1 The Clinical Crisis of Triage Delays
Emergency departments (EDs) and outpatient triage facilities represent the frontline of modern healthcare delivery. In these acute care environments, patient arrival patterns are inherently stochastic. Among all patient demographics, pediatric patients possess the highest vulnerability to rapid physiological deterioration. Unlike adults, infants and toddlers exhibit non-specific clinical signs of distress: an infant experiencing respiratory syncytial virus (RSV), acute gastroenteritis with severe dehydration, or septicemia may transition from quiet lethargy to irreversible hemodynamic collapse within 30 to 60 minutes.

### 1.2 The "Invisible Child" Phenomenon
A primary driver of pediatric triage oversight is the **"Invisible Child" phenomenon**:
- **Physical Occlusion:** Infants held against caregivers' torsos in fabric slings or swaddled in blankets obscure anatomical boundaries.
- **Acoustic Masking:** Critically ill infants become lethargic and motionless rather than crying loudly, appearing peaceful to visual scans.
- **Registry Disconnects:** Adult caregivers register at intake desks under their own name without noting accompanying infants.

### 1.3 System Overview & Objectives
This research implements an edge-deployed computer vision monitoring system that:
1. Detects and differentiates children and adults in real time.
2. Maintains persistent tracking IDs under severe occlusion.
3. Operates at 30 FPS on standard consumer CPUs via ONNX Runtime.
4. Dispatches immediate clinical alerts when pediatric occupancy exceeds capacity limits.

---

## 2. Literature Review & Theoretical Foundations

### 2.1 Object Detection Evolution
- **Two-Stage Detectors (Faster R-CNN):** High accuracy via Region Proposal Networks (RPN) but high latency ($80-150\text{ ms}$), making them unsuitable for edge execution.
- **Single-Stage Detectors (YOLO):** Treats detection as unified spatial regression, predicting coordinates and class probabilities in a single pass ($15-35\text{ ms}$).

### 2.2 Multi-Object Tracking State-of-the-Art
- **SORT:** Kalman filtering + Hungarian matching; loses continuity during brief occlusions.
- **DeepSORT:** Adds deep visual Re-ID embeddings but incurs heavy CPU bottlenecks ($>300\%$ latency).
- **ByteTrack:** Retains low-confidence detections ($\tau_{\text{low}} \le \text{score} < \tau_{\text{high}}$) in a secondary association step, preserving occluded tracks without deep embeddings.
- **BoT-SORT & OC-SORT:** Add camera motion compensation and observation-centric momentum recovery.

### 2.3 Illumination Enhancement in LAB Space
Global histogram equalization causes noise amplification and color shifting. Applying CLAHE exclusively to the $L^*$ luminance channel of the CIE $L^*a^*b^*$ color space boosts contrast while preserving skin tones:

$$L_{\text{enhanced}}^*(x, y) = \text{CLAHE}\left( L^*(x, y); \text{clip\_limit}=2.0, \text{grid}=(8, 8) \right)$$

---

## 3. System Architecture & Engineering Methodology

### 3.1 The NiceGUI Monolith
Consolidates the Computer Vision Engine, Multi-Tracker Suite, Telemetry Model, and User Interface into a single Python runtime, eliminating REST/WebSocket network serialization latency.

### 3.2 Decoupled Dual-Thread Capture-Inference Pattern
- **Capture Thread:** Continuously drains `cap.read()` with `CAP_PROP_BUFFERSIZE = 1`, eliminating the 3–5 second buffer lag common in OpenCV.
- **Inference Thread:** Executes CLAHE, YOLO, tracking, and spatial fallback asynchronously, updating in-memory state and video overlays.

```
       ┌────────────────────────┐
       │   Video Feed Source    │
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │ Capture Worker (30 FPS)│ (CAP_PROP_BUFFERSIZE = 1)
       └───────────┬────────────┘
                   │ Latest Frame
                   ▼
       ┌────────────────────────┐
       │ Inference Worker (ONNX)│ (CLAHE + YOLO + MultiTracker)
       └───────────┬────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
   TelemetryState      /camera/stream
   (In-Memory Bind)    (MJPEG Stream)
```

---

## 4. Computer Vision Engine & Deep Learning

### 4.1 Fine-Tuned Model Suite & ONNX Optimization
- **`pediatric-model.pt` / `.onnx`:** Dual-class pediatric vs. adult classifier.
- **`pediatric-kids-only.pt` / `.onnx`:** Dedicated pediatric specialist ($>94\%$ recall).
- **`yolo26s.pt`:** Base COCO detector with ground-plane perspective heuristics.

**ONNX Runtime Speedup:** Reduces inference time from **59.8 ms** (PyTorch FP32) to **28.4 ms** on CPU—a **2.1x speedup**.

### 4.2 Perspective-Aware Geometric Classification
For generic COCO models, normalized height $R_{\text{norm}}$ is evaluated against the optical horizon ($Y_h = 0.20$) with sitting-pose aspect ratio compensation ($AR > 0.55 \implies h_{\text{eff}} = h \cdot 1.50$):

$$R_{\text{norm}} = \frac{h_{\text{eff}}}{h_{\text{expected\_adult}}(\tilde{y})}$$

---

## 5. Multi-Tracker Suite, Scene Analysis & Debouncing

### 5.1 Scene Analysis & Hysteresis Auto-Switching
1. **Camera Motion Score ($\Delta I$):** Mean frame difference on downsampled $160\text{ px}$ grayscale frames ($\Delta I > 12.0 \implies \text{BoT-SORT}$).
2. **Occlusion Density Score ($\Omega$):** Mean pairwise IoU across all detections ($\Omega > 0.25 \implies \text{FastTracker}$).
3. **Hysteresis Barrier:** Enforces $\Delta t_{\text{switch}} \ge 3.0\text{ seconds}$ to eliminate rapid switching chatter.

### 5.2 Spatial Centroid Fallback & Lost-Track Debouncing
- **Spatial Fallback:** Matches untracked detections ($\text{track\_id} = -1$) to nearby active centroids ($r \le 40.0\text{ px}$).
- **Lost-Centroid Debouncing:** Retains expired tracks in a 5.0-second queue ($\mathcal{Q}_{\text{lost}}$); re-appearing targets within $150\text{ px}$ do not increment cumulative daily totals.

---

## 6. Clinical Monitoring & User Interface

### 6.1 Telemetry Computation & Overcrowding Logic
- Active tracks are filtered with a $1.5\text{-second}$ idle grace window.
- Overcrowding alarm triggers when:

$$C_{\text{child}}\%(t) = \left( \frac{\text{current\_children}(t)}{K_{\text{cap}}} \right) \times 100\% \ge 30.0\%$$

### 6.2 Dark-Mode UI & Automated Audit Reports
- Built with a clinical dark palette (`slate-950` / `cyan-400` / `indigo-400`).
- Provides one-click export of structured CSV telemetry logs and formatted clinical PDF capacity reports via `src/engine/reporter.py`.

---

## 7. Experimental Results & Benchmarks

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    KEY EXPERIMENTAL BENCHMARK SUMMARY                   │
│                                                                         │
│  Metric                        Value Achieved                           │
│  ─────────────────────────────────────────────────────────────────────  │
│  Dual-Class Pediatric mAP@0.5  0.912                                    │
│  Dedicated Kids-Only mAP@0.5   0.948                                    │
│  Multiple Object Tracking Acc  84.6% MOTA / 87.2% IDF1                  │
│  ID Switch Reduction vs SORT   88.0% Reduction (142 -> 17)              │
│  ONNX CPU Inference Latency    28.4 ms (30.2 FPS on Consumer CPU)       │
│  CPU Utilization (8-core CPU)  38.6% Average                            │
│  CLAHE Low-Light Recall Gain   +15.3 percentage points (0.741 -> 0.894) │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Ethical Governance & Clinical Deployment
- **Zero Biometric Storage:** No facial recognition or permanent video recording.
- **HIPAA & GDPR Compliance:** On-premise local network execution; ephemeral frame lifecycle ($<33\text{ ms}$).
- **Demographic Fairness:** Multi-ethnic training datasets and skin-tone invariant LAB CLAHE normalization.
- **Fail-Closed Safety:** Offline stream badges and health warnings on signal loss.
- **Economic Viability:** Deployable on standard $300–$500 refurbished PCs with USB webcams.

---

## 9. Conclusion
The Invisible Child Pediatric Monitor successfully resolves a critical vulnerability in clinical triage. By uniting deep learning object detection, adaptive multi-tracking, spatial centroid debouncing, and a zero-latency monolithic user interface, the system delivers publication-grade computer vision intelligence on affordable edge hardware, ensuring no child in emergency waiting halls remains unseen.

---
*Kwame Nkrumah University of Science and Technology (KNUST) — Department of Mathematics (2026)*
