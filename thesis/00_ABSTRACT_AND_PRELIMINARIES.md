# Preliminaries: Abstract, Acknowledgements & Academic Structure

**Thesis Title:**  
*The Invisible Child: Pediatric Patient Counting with Interactive Object Detection and Dynamic Multi-Tracking in Clinical Triage Environments*

**Candidate:**  
Jacky Smith

**Academic Supervisor & Faculty:**  
Department of Mathematics, Faculty of Physical and Computational Sciences  
Kwame Nkrumah University of Science and Technology (KNUST), Kumasi, Ghana  

**Degree:**  
Bachelor of Science (Honours) in Actuarial Science / Mathematics with Biomedical Data Science Specialization  

**Date of Submission:**  
February 2026  

---

## Dedication

*To the clinical nurses, triage officers, and healthcare workers in low-resource emergency departments who labor tirelessly under overwhelming patient volumes; and to every infant and pediatric patient whose timely care depends on vigilant, unsleeping intelligence.*

---

## Acknowledgements

I wish to express my deepest gratitude to my academic supervisor, whose profound insights into mathematical modeling, computer vision architectures, and rigorous stochastic evaluation shaped the trajectory of this research. Special appreciation is extended to the faculty and research staff at the Department of Mathematics, KNUST, for their relentless commitment to bridging applied mathematics and life-saving biomedical engineering.

I am profoundly thankful to the clinical triage teams and hospital administrators who offered invaluable practical perspectives on waiting room dynamics, occlusion patterns during infant nursing, and the ergonomic constraints of real-time clinical dashboards. 

Finally, I express my eternal gratitude to my family and colleagues whose unyielding encouragement, patience, and support provided the foundation upon which this thesis was built.

---

## Abstract

In resource-constrained hospital emergency departments (EDs) and outpatient triage facilities, infant and pediatric mortality is heavily exacerbated by prolonged, unmonitored waiting room delays. In such high-stress clinical environments, manual triage logs and visual headcounts consistently fail to account for the **"Invisible Child" phenomenon**—infants wrapped in swaddling cloths, carried against caregivers' torsos, or occluded in crowded waiting areas. As a consequence, pediatric patient load is systematically underestimated, leading to severe nursing shortages, delayed critical interventions, and preventable pediatric decompensation.

To resolve this critical healthcare challenge, this research designs, develops, mathematically models, and validates a real-time, edge-deployed clinical computer vision system. The system integrates deep convolutional and attention-based object detection (**YOLO architectures**) with an adaptive **Multi-Tracker Suite** (incorporating **ByteTrack**, **BoT-SORT**, **OC-SORT**, and **FastTracker**) into a unified, zero-network-serialization Python monolith powered by NiceGUI.

Key mathematical and engineering contributions include:
1. **Asynchronous Decoupled Capture-Inference Architecture:** A multithreaded design utilizing a continuous OpenCV capture buffer draining thread (`CAP_PROP_BUFFERSIZE = 1`) coupled to a background asynchronous inference worker, eliminating video streaming latency and sustaining constant 30 FPS telemetry playback.
2. **Illumination-Invariant LAB CLAHE Pipeline:** A contrast enhancement framework operating in the LAB color space that boosts feature contrast in dim triage environments without shifting critical RGB chromatic signatures.
3. **Adaptive Scene Analysis with Hysteresis Stabilization:** A dynamic switching algorithm that continuously evaluates camera motion via optical flow frame difference ($\Delta I$) and crowd occlusion density via pairwise Intersection-over-Union ($\text{IoU}_{\text{pairwise}}$), automatically routing frames to optimal tracking routines across varying triage conditions.
4. **Centroid Spatial Fallback & Temporal Debouncing:** A spatial Euclidean re-identification mechanism ($r \le 40.0\text{ px}$) and a 5.0-second lost-track debouncing queue that prevents identity fragmentation and double-counting during physical occlusion.
5. **High-Speed ONNX Runtime Quantization:** Model optimization achieving a **2.1x CPU inference speedup** (reducing inference latency from 59.8 ms to 28.4 ms), allowing edge deployment on low-cost clinical workstations without expensive discrete GPUs.
6. **Automated Clinical Governance:** Continuous computation of pediatric load percentage ($C_{\text{child}}\%$), automated threshold alerting ($\ge 30\%$), and automated export of structured CSV telemetry logs and formatted PDF capacity audit reports.

Extensive empirical evaluations across benchmark video datasets and live clinical simulation feeds demonstrate an overall detection accuracy of **mAP@0.5 = 0.912** on pediatric targets, a Multiple Object Tracking Accuracy (**MOTA**) of **84.6%**, an **IDF1 score of 87.2%**, and zero video lag across multi-hour stress testing. The system establishes a robust, privacy-preserving, and computationally accessible paradigm for automated pediatric capacity surveillance in modern healthcare infrastructure.

**Keywords:** Pediatric Patient Counting, Clinical Triage, Computer Vision, YOLO, Multi-Object Tracking, ByteTrack, BoT-SORT, CLAHE, Edge Computing, NiceGUI, Biomedical Informatics.

---

## Table of Contents

1. **Chapter 1: Introduction & Clinical Context**
   - 1.1 Background & The Clinical Crisis of Triage Delays
   - 1.2 The "Invisible Child" Phenomenon: Definition & Etiology
   - 1.3 Problem Statement
   - 1.4 Research Questions & Core Hypothesis
   - 1.5 Research Objectives
   - 1.6 Scientific & Engineering Contributions
   - 1.7 Thesis Organization

2. **Chapter 2: Literature Review & Theoretical Foundations**
   - 2.1 Overview of Object Detection in Clinical & Surveillance Domains
   - 2.2 Deep Learning Architectures: From Two-Stage R-CNN to Single-Stage YOLO
   - 2.3 Multi-Object Tracking (MOT) Paradigms & Mathematical Foundations
     - 2.3.1 Classical Kalman Filtering & Hungarian Matching
     - 2.3.2 DeepSORT & Visual Embedding Challenges
     - 2.3.3 ByteTrack: Association with Low-Score Detections
     - 2.3.4 BoT-SORT: Camera Motion Compensation & Re-ID
     - 2.3.5 OC-SORT: Observation-Centric Momentum Recovery
   - 2.4 Illumination Normalization & Contrast Enhancement in Computer Vision
   - 2.5 Perspective Geometry & Ground-Plane Scale Invariance
   - 2.6 Edge Computing vs. Cloud Streaming in Medical Informatics
   - 2.7 Summary & Identification of Research Gaps

3. **Chapter 3: System Architecture & Engineering Methodology**
   - 3.1 Monolithic Architecture vs. Distributed Microservices
   - 3.2 Decoupled Dual-Thread Capture-Inference Pattern
   - 3.3 Zero-Network-Serialization In-Memory State Model
   - 3.4 Hardware Abstraction & Dynamic Stream Resolution
   - 3.5 Operational Modes: Web Browser vs. Native Desktop App

4. **Chapter 4: Computer Vision & Deep Learning Engine**
   - 4.1 Dataset Curation & Pediatric Annotation Protocol
   - 4.2 Transfer Learning & Fine-Tuning YOLO Neural Networks
   - 4.3 Model Optimization: PyTorch to ONNX Runtime Quantization
   - 4.4 Dynamic Class Mapping & Architecture Auto-Resolution
   - 4.5 Illumination Normalization: LAB Color Space CLAHE Pipeline
   - 4.6 Perspective-Aware Classification Heuristics

5. **Chapter 5: Tracking Engine, Scene Analysis & Debouncing**
   - 5.1 The Multi-Tracker Suite Architecture
   - 5.2 Mathematical Formulation of Dynamic Tracking Algorithms
   - 5.3 Real-Time Scene Analyzer: Optical Flow & Occlusion Density
   - 5.4 Hysteresis Stabilization Logic
   - 5.5 Untracked Spatial Centroid Fallback Re-Identification
   - 5.6 Spatial Debouncing & Lost-Centroid Temporal Queues

6. **Chapter 6: Clinical Intelligence, Capacity Analytics & User Interface**
   - 6.1 Clinical Telemetry Metric Computation
   - 6.2 Pediatric Overcrowding Warning Logic & Alert Triggers
   - 6.3 Clinical Design System & Dark-Mode Ergonomics
   - 6.4 Real-Time Interactive Controls & Dynamic Dropdown Selectors
   - 6.5 Automated Audit Logging: CSV Telemetry & Formatted PDF Reports

7. **Chapter 7: Experimental Setup, Benchmarks & Results**
   - 7.1 Experimental Testbed & Video Dataset Characteristics
   - 7.2 Object Detection Evaluation Metrics (mAP, Precision, Recall, F1)
   - 7.3 Multi-Object Tracking Evaluation Metrics (MOTA, MOTP, IDF1, HOTA, IDSW)
   - 7.4 Latency, Throughput & Computational Resource Benchmarks
   - 7.5 Comprehensive Ablation Studies
     - 7.5.1 Impact of LAB CLAHE Preprocessing
     - 7.5.2 Impact of Spatial Centroid Fallback
     - 7.5.3 Impact of Dynamic Scene-Adaptive Tracker Switching

8. **Chapter 8: Ethical Considerations, Privacy & Clinical Deployment**
   - 8.1 Privacy-by-Design & Zero-Biometric Storage Architecture
   - 8.2 Compliance with HIPAA & GDPR Medical Informatics Standards
   - 8.3 Demographic Fairness & Pediatric Age-Bias Mitigation
   - 8.4 Failure Mode Analysis & Fail-Closed Clinical Safeguards
   - 8.5 Deployment Blueprint for Resource-Constrained Clinics

9. **Chapter 9: Conclusion & Future Research Directions**
   - 9.1 Summary of Research Achievements
   - 9.2 Key Clinical Findings & Theoretical Insights
   - 9.3 Limitations of the Current System
   - 9.4 Directions for Future Exploration

10. **References & Bibliography**

11. **Appendices**
    - Appendix A: Complete System Configuration Schema
    - Appendix B: Mathematical Derivations
    - Appendix C: Test Suite Architecture & Verification Protocols

---

## List of Figures

- **Figure 1.1:** The "Invisible Child" phenomenon illustrated in high-density clinical triage waiting rooms.
- **Figure 2.1:** Architectural comparison of single-stage (YOLO) versus two-stage (Faster R-CNN) object detectors.
- **Figure 2.2:** ByteTrack two-stage bipartite matching bipartite graph.
- **Figure 3.1:** High-level block diagram of the NiceGUI Monolith architecture.
- **Figure 3.2:** Decoupled dual-thread capture-inference timing diagram illustrating buffer-drain synchronization.
- **Figure 4.1:** Neural architecture of the fine-tuned YOLO pediatric detector.
- **Figure 4.2:** LAB color space separation and CLAHE histogram clipping curve.
- **Figure 4.3:** Ground-plane perspective normalization geometry showing optical horizon and expected height scaling.
- **Figure 5.1:** State transition diagram of the adaptive MultiTrackerEngine.
- **Figure 5.2:** Spatial centroid fallback matching and temporal lost-track debouncing queue workflow.
- **Figure 6.1:** Clinical Command Center Dashboard interface (`/dashboard`).
- **Figure 6.2:** Stream Evaluation and Testing Lab interface (`/video-test`).
- **Figure 7.1:** Precision-Recall curves across Adult, Child, and Combined patient classes.
- **Figure 7.2:** Inference latency and frame throughput comparison: PyTorch FP32 vs. ONNX Runtime CPU.
- **Figure 7.3:** Tracking continuity comparison under severe caregiver occlusion: Standard ByteTrack vs. Adaptive MultiTracker with Spatial Fallback.

---

## List of Tables

- **Table 2.1:** Comparative taxonomy of modern Multi-Object Tracking (MOT) algorithms.
- **Table 4.1:** Model architecture suite parameters, input dimensions, and runtime properties.
- **Table 5.1:** Tracker recommendation rules based on scene motion and occlusion density.
- **Table 6.1:** Telemetry state data schema and mathematical definitions.
- **Table 7.1:** Pediatric and adult detection performance metrics (IoU threshold = 0.50).
- **Table 7.2:** Multi-Object Tracking benchmark results across clinical waiting room test sequences.
- **Table 7.3:** Hardware resource utilization and FPS benchmarks across multiple compute targets.
- **Table 7.4:** Ablation study evaluating CLAHE preprocessing in low-light environments.
- **Table 7.5:** Ablation study evaluating spatial centroid fallback under occluded tracks.
- **Table 7.6:** Ablation study comparing static vs. dynamic scene-adaptive tracking.
- **Table 8.1:** Privacy and regulatory compliance matrix (HIPAA vs. GDPR vs. Local Guidelines).

---

## Nomenclature & Acronyms

| Acronym | Definition |
|:---|:---|
| **AI** | Artificial Intelligence |
| **BoT-SORT** | Bag of Tricks - Simple Online and Realtime Tracking |
| **ByteTrack** | Byte-level Multi-Object Tracking by Associating Every Detection Box |
| **CCTV** | Closed-Circuit Television |
| **CDD** | Child Detection Dataset |
| **CLAHE** | Contrast Limited Adaptive Histogram Equalization |
| **CNN** | Convolutional Neural Network |
| **CSV** | Comma-Separated Values |
| **ED** | Emergency Department |
| **EMA** | Exponential Moving Average |
| **EOF** | End of File |
| **FPS** | Frames Per Second |
| **FP32** | 32-bit Floating Point Representation |
| **GDPR** | General Data Protection Regulation |
| **GPU** | Graphics Processing Unit |
| **HOTA** | Higher Order Tracking Accuracy |
| **HTTP** | Hypertext Transfer Protocol |
| **IDF1** | Identification F1-Score |
| **IDSW** | Identity Switches |
| **IoU** | Intersection-over-Union |
| **JPEG / MJPEG** | Joint Photographic Experts Group / Motion JPEG |
| **KNUST** | Kwame Nkrumah University of Science and Technology |
| **LAB** | Lightness, A (Green-Red), B (Blue-Yellow) Color Space |
| **mAP** | Mean Average Precision |
| **MOT** | Multi-Object Tracking |
| **MOTA** | Multiple Object Tracking Accuracy |
| **MOTP** | Multiple Object Tracking Precision |
| **NMS** | Non-Maximum Suppression |
| **OC-SORT** | Observation-Centric SORT |
| **ONNX** | Open Neural Network Exchange |
| **PDF** | Portable Document Format |
| **PyTorch** | Open-source Machine Learning Framework |
| **R-CNN** | Region-based Convolutional Neural Network |
| **REST** | Representational State Transfer |
| **RGB** | Red, Green, Blue Color Model |
| **RTSP** | Real-Time Streaming Protocol |
| **SORT** | Simple Online and Realtime Tracking |
| **UI / UX** | User Interface / User Experience |
| **UVC** | USB Video Class |
| **V4L2** | Video4Linux2 |
| **YOLO** | You Only Look Once (Object Detection Framework) |
