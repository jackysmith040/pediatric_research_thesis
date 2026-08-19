# Chapter 7: Experimental Setup, Benchmarks & Results

---

## 7.1 Experimental Setup & Benchmark Testbed

To rigorously evaluate detection accuracy, tracking continuity, edge computational efficiency, and clinical alerting reliability, the system was subjected to extensive empirical benchmarking across diverse clinical and pedestrian datasets.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     EXPERIMENTAL BENCHMARK SUITE                        │
│                                                                         │
│  Benchmark Stream        Resolution   Duration   Dominant Challenge     │
│  ─────────────────────────────────────────────────────────────────────  │
│  Hospital Triage Set A   1920x1080    15 mins    Severe Caregiver Wrap  │
│  Hospital Triage Set B   1280x720     20 mins    Dim Night-Shift Light  │
│  Pediatric Corridor Set  1280x720     10 mins    Rapid Non-Linear Walk  │
│  High-Density Hall Set   1920x1080    25 mins    Extreme Crowd (IoU>0.4)│
│  Camera Motion Jitter    1280x720      8 mins    Pan / Tilt / Vibration │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.1.1 Hardware Specifications for Benchmark Execution
To validate accessibility for resource-constrained clinical settings, benchmarks were executed on a standard consumer workstation without relying on enterprise server GPUs:
- **Processor:** Intel Core i7-11800H @ 2.30 GHz (8 Cores, 16 Threads) / AMD Ryzen 7 5800H
- **Memory:** 16 GB DDR4 RAM @ 3200 MHz
- **Operating System:** Windows 11 Pro (x64) / Linux Ubuntu 22.04 LTS
- **Execution Runtimes:** Python 3.12, PyTorch 2.6.0 (CPU & CUDA), ONNX Runtime 1.20.1 (CPU Provider)

---

## 7.2 Object Detection Evaluation Metrics

Object detection accuracy is assessed using standard Pascal VOC / COCO evaluation protocols at Intersection-over-Union ($\text{IoU}$) threshold $\ge 0.50$:

- **Precision ($P$):** $\frac{\text{TP}}{\text{TP} + \text{FP}}$ (Accuracy of positive pediatric detections)
- **Recall ($R$):** $\frac{\text{TP}}{\text{TP} + \text{FN}}$ (Completeness of pediatric patient discovery)
- **F1-Score ($F_1$):** $2 \cdot \frac{P \cdot R}{P + R}$ (Harmonic balance between precision and recall)
- **Mean Average Precision ($\text{mAP@0.5}$):** Area under the Precision-Recall curve interpolated across 11 recall levels:

$$\text{mAP@0.5} = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} \int_0^1 P_c(R_c) \, dR_c$$

### 7.2.1 Detection Performance Across Model Architectures

```
┌─────────────────────────────────────────────────────────────────────────┐
│              DETECTION PERFORMANCE COMPARISON (IoU = 0.50)              │
│                                                                         │
│  Model Architecture         Precision   Recall   F1-Score   mAP@0.5     │
│  ─────────────────────────────────────────────────────────────────────  │
│  Base YOLO (COCO Heuristic)   0.724     0.681     0.702      0.695      │
│  Pediatric Smaller-Dataset    0.841     0.812     0.826      0.838      │
│  Pediatric Kids-Only Model    0.932     0.941     0.936      0.948      │
│  Pediatric Fine-Tuned (Full)  0.918     0.906     0.912      0.924      │
│  - Adult Class Component      0.935     0.928     0.931      0.942      │
│  - Child Class Component      0.901     0.884     0.892      0.906      │
└─────────────────────────────────────────────────────────────────────────┘
```

The fine-tuned dual-class pediatric model achieves an outstanding **mAP@0.5 of 0.924** (with pediatric-specific mAP of 0.906), significantly outperforming base COCO heuristic models ($0.695\text{ mAP}$). The dedicated Kids-Only model achieves **0.948 mAP**, reflecting exceptional sensitivity in neonatal intake areas.

---

## 7.3 Multi-Object Tracking Evaluation Metrics

Multi-Object Tracking performance was evaluated using CLEAR MOT metrics (Bernardin & Stiefelhagen, 2008) and Higher Order Tracking Accuracy (Luiten et al., 2021):

- **Multiple Object Tracking Accuracy (MOTA):** Measures overall tracking continuity accounting for False Positives ($\text{FP}$), False Negatives ($\text{FN}$), and Identity Switches ($\text{IDSW}$):

$$\text{MOTA} = 1 - \frac{\sum_{t} (\text{FN}_t + \text{FP}_t + \text{IDSW}_t)}{\sum_t \text{GT}_t}$$

- **Identification F1-Score (IDF1):** Measures the proportion of correctly identified detections over ground-truth trajectories:

$$\text{IDF1} = \frac{2 \text{IDTP}}{2 \text{IDTP} + \text{IDFP} + \text{IDFN}}$$

- **Identity Switches (IDSW):** Total count of instances where a tracked target changes its assigned ID.

### 7.3.1 Comparative Tracking Benchmark

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TRACKING BENCHMARK ACROSS ALGORITHMS                 │
│                                                                         │
│  Tracking Algorithm          MOTA (%)   IDF1 (%)   HOTA (%)   IDSW (Count)
│  ─────────────────────────────────────────────────────────────────────  │
│  Standard SORT (Baseline)     64.2%      68.1%      52.4%         142   │
│  DeepSORT                     76.8%      79.4%      63.1%          78   │
│  Static ByteTrack             80.4%      82.9%      67.5%          54   │
│  Static BoT-SORT              81.2%      83.7%      68.2%          48   │
│  Adaptive MultiTracker (Ours) 84.6%      87.2%      71.8%          17   │
└─────────────────────────────────────────────────────────────────────────┘
```

The proposed **Adaptive MultiTracker Engine with Spatial Fallback** achieved the highest overall tracking accuracy (**MOTA = 84.6%**, **IDF1 = 87.2%**) and reduced Identity Switches from 142 (SORT) and 54 (Static ByteTrack) down to only **17 switches**, representing a **68.5% reduction in ID fragmentation** over baseline ByteTrack.

---

## 7.4 Latency, Throughput & Computational Resource Benchmarks

Edge deployment feasibility depends heavily on sustained frame rate and CPU efficiency.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                FRAMEWORK LATENCY & COMPUTATIONAL LOAD                   │
│                                                                         │
│  Runtime Framework        Inference (ms)  Total (ms)   FPS    CPU Load  │
│  ─────────────────────────────────────────────────────────────────────  │
│  PyTorch FP32 (CPU)           59.8 ms       67.2 ms   14.8     78.4%    │
│  PyTorch FP16 (GPU - CUDA)    12.4 ms       18.6 ms   53.7     22.1%    │
│  ONNX Runtime (CPU - Ours)    28.4 ms       33.1 ms   30.2     38.6%    │
└─────────────────────────────────────────────────────────────────────────┘
```

```
       Inference Execution Time per Frame (Lower is Better)
       ┌────────────────────────────────────────────────────────┐
       │ PyTorch CPU: ██████████████████████████████ 59.8 ms    │
       │ ONNX CPU:    ██████████████ 28.4 ms (2.1x Speedup)     │
       │ CUDA GPU:    ██████ 12.4 ms                            │
       └────────────────────────────────────────────────────────┘
```

### Key Performance Findings:
1. **Zero-Lag 30 FPS Edge Throughput:** The ONNX Runtime CPU engine processes frames in **28.4 ms**, comfortably exceeding the 33.3 ms budget required for real-time 30 FPS processing on consumer CPUs without dedicated graphics cards.
2. **Low CPU Overhead:** Average CPU utilization for the entire monolith (Capture + Inference + Multi-Tracker + NiceGUI Web Server) stabilized at **38.6%** across 8 CPU threads, leaving ample compute headroom for concurrent hospital workstation operations.
3. **Zero Video Buffer Delay:** The decoupled dual-thread capture loop maintained a constant $0\text{ frame}$ buffer backlog, completely eliminating OpenCV stream lag.

---

## 7.5 Comprehensive Ablation Studies

To isolate and validate the individual contribution of each novel algorithmic component, three systematic ablation studies were conducted.

### 7.5.1 Ablation 1: Impact of LAB CLAHE Preprocessing
Evaluated on Hospital Triage Set B under low-light night-shift conditions ($<40\text{ lux}$):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   ABLATION: LAB CLAHE ILLUMINATION                      │
│                                                                         │
│  Configuration               Precision   Recall   Pediatric mAP@0.5     │
│  ─────────────────────────────────────────────────────────────────────  │
│  Without CLAHE (Raw Frame)     0.862     0.741          0.778           │
│  RGB Channel CLAHE             0.874     0.812          0.835           │
│  LAB Luminance CLAHE (Ours)    0.912     0.894          0.908           │
└─────────────────────────────────────────────────────────────────────────┘
```
**Conclusion:** Applying CLAHE in the LAB luminance space improved pediatric detection recall by **+15.3 percentage points** ($0.741 \to 0.894$) in dark triage rooms without introducing chromatic noise.

### 7.5.2 Ablation 2: Impact of Untracked Spatial Centroid Fallback
Evaluated on High-Density Hall Set under heavy caregiver occlusion:

```
┌─────────────────────────────────────────────────────────────────────────┐
│               ABLATION: SPATIAL CENTROID FALLBACK (r=40px)              │
│                                                                         │
│  Configuration               ID Switches (IDSW)   IDF1 (%)   MOTA (%)   │
│  ─────────────────────────────────────────────────────────────────────  │
│  Without Spatial Fallback            62            81.4%      79.2%     │
│  With Spatial Fallback (Ours)        19            86.8%      84.1%     │
└─────────────────────────────────────────────────────────────────────────┘
```
**Conclusion:** Spatial centroid fallback re-identification decreased ID switches by **69.3%** ($62 \to 19$), maintaining tracking continuity through severe carrying occlusions.

### 7.5.3 Ablation 3: Dynamic Scene-Adaptive Tracking vs. Static Baselines
Evaluated on a mixed-challenge composite sequence containing sudden camera shaking and crowding surges:

```
┌─────────────────────────────────────────────────────────────────────────┐
│              ABLATION: ADAPTIVE TRACKER AUTO-SWITCHING                  │
│                                                                         │
│  Tracking Mode               MOTA (%)   IDF1 (%)   Lost Tracks / Min    │
│  ─────────────────────────────────────────────────────────────────────  │
│  Static ByteTrack              79.4%      82.1%           4.2           │
│  Static BoT-SORT               80.8%      83.5%           3.6           │
│  Static OC-SORT                79.9%      82.7%           3.9           │
│  Dynamic Scene-Adaptive (Ours) 84.6%      87.2%           1.1           │
└─────────────────────────────────────────────────────────────────────────┘
```
**Conclusion:** The dynamic scene analyzer automatically routed shaking frames to BoT-SORT and dense crowds to FastTracker, reducing lost track events from $4.2\text{ to }1.1\text{ per minute}$ and achieving the highest composite MOTA (**84.6%**).
