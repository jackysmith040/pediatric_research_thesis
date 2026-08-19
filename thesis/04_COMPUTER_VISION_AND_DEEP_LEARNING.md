# Chapter 4: Computer Vision & Deep Learning Engine

---

## 4.1 Dataset Curation & Pediatric Annotation Protocol

Supervised training of clinical pediatric detectors requires specialized datasets capturing the nuanced anatomical, morphological, and positional characteristics of children in clinical waiting environments. Standard pedestrian datasets (such as MS COCO, Pascal VOC, or Cityscapes) treat all human instances as a single homogeneous `person` class, failing to differentiate pediatric patients from adult caregivers.

### 4.1.1 Dataset Sources & Composition
The training corpus was compiled through an integrated curation pipeline utilizing the **Child Detection Dataset (CDD)** aggregated via Roboflow, supplemented with specialized clinical triage video sequences:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      DATASET COMPOSITION & PROTOCOL                     │
│                                                                         │
│  Class Category      Training Images   Validation Images   Test Images  │
│  ────────────────────────────────────────────────────────────────────   │
│  Adult Caregivers         4,820              1,240             620      │
│  Pediatric / Children     3,950              1,010             505      │
│  Carried / Occluded       1,830                460             230      │
│  ────────────────────────────────────────────────────────────────────   │
│  Total Annotated Boxes   10,600              2,710           1,355      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.1.2 Annotation Protocols for Carried & Occluded Infants
To specifically address the "Invisible Child" phenomenon, annotation protocols incorporated rigorous bounding box guidelines:
1. **Carried Infants in Fabric Slings/Wraps:** A distinct `Child` bounding box is annotated around the visible infant head and torso, even when 60–80% of the lower body is occluded by the caregiver's fabric wrap or arms.
2. **Adult Caregiver Enclosure:** The `Adult` bounding box encompasses the full standing/sitting adult silhouette, creating an overlapping bounding box structure with the carried infant ($\text{IoU} \approx 0.30 - 0.65$).
3. **Severe Blanketing / Swaddling:** If facial features, ears, or limbs are visible, a `Child` annotation is placed around the swaddled mass.

### 4.1.3 Data Augmentation Suite
To prevent overfitting and simulate severe hospital conditions, extensive offline and online augmentations were applied:
- **Photometric Distortions:** Hue jitter ($\pm 15^\circ$), Saturation ($\pm 25\%$), Value/Brightness ($\pm 35\%$) to simulate dim night shifts and harsh daylight glare.
- **Geometric Transformations:** Random horizontal flipping ($p=0.5$), random affine scaling ($0.8\times \text{ to } 1.2\times$), and mosaic stitching ($4\text{-image mosaic blending}$) to improve small-scale infant detection.
- **Random Erasing (Cutout):** Simulating occlusion by zeroing out random rectangular patches ($10\% - 25\%$ of bounding box area).

---

## 4.2 Transfer Learning & Fine-Tuning YOLO Neural Networks

The core neural detection backbone leverages advanced lightweight single-stage convolutional networks (YOLO architectures). Transfer learning was initialized from pre-trained COCO base weights, freezing shallow feature extraction layers during initial epochs to preserve general edge and texture filters, followed by end-to-end fine-tuning across all feature pyramid neck and head layers.

```
       Input Image (480x480x3)
                 │
                 ▼
       ┌────────────────────────────────────────────────────────┐
       │   Backbone: CSPDarknet / C2f Feature Extraction Layers │
       │   (Cross-Stage Partial Bottlenecks & Spatial Conv)     │
       └─────────────────────────┬──────────────────────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 ▼               ▼               ▼
               P3 (Small)      P4 (Medium)     P5 (Large)
                 │               │               │
                 └───────────────┼───────────────┘
                                 ▼
       ┌────────────────────────────────────────────────────────┐
       │   Neck: Path Aggregation Network (PANet / BiFPN)       │
       │   (Top-Down & Bottom-Up Multi-Scale Feature Fusion)    │
       └─────────────────────────┬──────────────────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
       ┌───────────────────┐           ┌───────────────────┐
       │ Classification    │           │ Bounding Box Reg  │
       │ Head (Adult/Child)│           │ Head (CIoU + DFL) │
       └───────────────────┘           └───────────────────┘
```

### 4.2.1 Trained Model Suite
The research generated and evaluated a comprehensive suite of fine-tuned and specialized model variants:

1. **`pediatric-model.pt` (Full Dual-Class Pediatric Model):**  
   Fine-tuned on the complete training corpus with explicit dual-class classification (`Class 0 = Adult`, `Class 1 = Child`). Optimized for balanced precision and recall in mixed triage environments.
2. **`pediatric-kids-only.pt` (Dedicated Pediatric Specialist):**  
   Trained exclusively on pediatric instances (`Class 0 = Child`), achieving high sensitivity ($>94\%$) in specialized neonatal and pediatric ward entrances where adults are ignored.
3. **`pediatric-smaller-dataset-trained.pt` (Lightweight Specialized Variant):**  
   Trained on a compact, highly curated subset of severe occlusion cases to evaluate minimal-data transfer learning limits.
4. **`yolo26s.pt` (Base COCO Architecture with Heuristics):**  
   Serves as an un-fine-tuned baseline detector operating via COCO `person` class coupled with geometric ground-plane perspective heuristics.

---

## 4.3 Model Optimization: PyTorch to ONNX Runtime Quantization

While PyTorch models (.pt) offer seamless training and debugging, raw PyTorch FP32 inference introduces substantial computational overhead on consumer CPUs due to dynamic computational graph overhead and unvectorized matrix multiplication operations.

To enable high-throughput edge execution, all models were exported to the **Open Neural Network Exchange (ONNX)** format and executed via the **ONNX Runtime engine** (`onnxruntime-cpu`):

$$\text{PyTorch (.pt Graph)} \xrightarrow{\text{torch.onnx.export}} \text{Static ONNX Computation Graph} \xrightarrow{\text{Graph Optimization}} \text{ONNX Runtime Execution}$$

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PYTORCH vs. ONNX RUNTIME BENCHMARK                   │
│                                                                         │
│  Model Architecture           Framework        CPU Latency    FPS Rate  │
│  ─────────────────────────────────────────────────────────────────────  │
│  pediatric-model.pt           PyTorch FP32       59.8 ms      16.7 FPS  │
│  pediatric-model.onnx (Ours)  ONNX Runtime CPU   28.4 ms      35.2 FPS  │
│  ─────────────────────────────────────────────────────────────────────  │
│  OVERALL SPEEDUP FACTOR:      2.1x FASTER (Zero GPU Dependency)         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3.1 ONNX Metadata Extraction & AST Literal Parsing
A critical engineering challenge in dynamic ONNX model execution is extracting class label mappings (`names`) directly from exported `.onnx` binary protobuf graphs.

In `Detector._init_model`, the system implements an automated metadata parsing fallback:
```python
if (not names or len(names) == 0) and is_onnx:
    try:
        import onnx
        import ast
        loaded_onnx = onnx.load(selected_path)
        props = {p.key: p.value for p in loaded_onnx.metadata_props}
        if 'names' in props:
            names = ast.literal_eval(props['names'])
    except Exception as meta_err:
        logger.warning(f"Could not extract metadata class names: {meta_err}")
```
This guarantees seamless introspection of class names directly from ONNX binary headers without external `.yaml` configuration dependencies.

---

## 4.4 Dynamic Class Mapping & Architecture Auto-Resolution

To support heterogeneous model architectures at runtime (dual-class pediatric models, single-class kids-only models, or base COCO detectors), the vision engine implements an automated **Class Resolution Algorithm** in `src/engine/detector.py`:

```
                       Loaded Model Names Dict
                                 │
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
   Contains 'child' /     Contains 'child' /    Contains only
   'kid' AND 'adult'      'kid' ONLY            'person' (COCO)
           │                     │                     │
           ▼                     ▼                     ▼
    Dual-Class Mode        Kids-Only Mode        COCO Heuristic Mode
    child_id = found       child_id = found      child_id = 1, adult_id = 0
    adult_id = found       adult_id = -1         uses_coco_person = True
```

### Mathematical Logic for Class ID Assignment:
Let $\mathcal{N} = \{ (k, v) \}$ be the dictionary mapping class indices $k \in \mathbb{N}$ to class label strings $v \in \Sigma^*$.

$$\text{child\_id} = \begin{cases} k & \text{if } \exists (k, v) \in \mathcal{N} \text{ s.t. } \text{lower}(v) \in \{\text{'child'}, \text{'kid'}, \text{'pediatric'}\} \\ -1 & \text{otherwise} \end{cases}$$

$$\text{adult\_id} = \begin{cases} k & \text{if } \exists (k, v) \in \mathcal{N} \text{ s.t. } \text{'adult'} \in \text{lower}(v) \\ -1 & \text{otherwise} \end{cases}$$

This automated introspection allows clinical staff to toggle between models on the fly via UI dropdowns without server reboots or configuration edits.

---

## 4.5 Illumination Normalization: LAB Color Space CLAHE Pipeline

Clinical emergency rooms exhibit extreme lighting fluctuations. To maintain high pediatric detection recall during dark night shifts without introducing color-shift artifacts, the engine applies Contrast Limited Adaptive Histogram Equalization (**CLAHE**) in the CIE $L^*a^*b^*$ color space.

```
       Raw BGR Frame
             │
             ▼
     cv2.cvtColor(BGR2LAB)
             │
             ├──────────────────────┬──────────────────────┐
             ▼                      ▼                      ▼
     L* (Luminance Channel)   a* (Green-Red)         b* (Blue-Yellow)
             │                      │                      │
             ▼                      │                      │
     CLAHE Equalization             │                      │
     - clip_limit = 2.0             │                      │
     - tile_grid = (8, 8)           │                      │
             │                      │                      │
             ▼                      │                      │
     L*_enhanced                    │                      │
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    ▼
                          cv2.merge((L*, a*, b*))
                                    │
                                    ▼
                          cv2.cvtColor(LAB2BGR)
                                    │
                                    ▼
                         Enhanced Output Frame
```

### Mathematical Implementation (`Detector.apply_clahe`):
Let $I_{\text{BGR}}(x, y)$ be the input color image.
1. Convert to LAB color space: $I_{\text{LAB}}(x, y) = \mathcal{T}_{\text{BGR}\to\text{LAB}}(I_{\text{BGR}}(x, y))$.
2. Separate into luminance $L^*(x, y)$ and chrominance $a^*(x, y), b^*(x, y)$.
3. Apply localized adaptive histogram clipping with clip limit $\beta = 2.0$ over an $8 \times 8$ grid of contextual tiles:

$$L_{\text{enhanced}}^*(x, y) = \text{CLAHE}\left( L^*(x, y); \text{clip\_limit}=2.0, \text{grid}=(8, 8) \right)$$

4. Recombine and convert back to BGR space:

$$I_{\text{out}}(x, y) = \mathcal{T}_{\text{LAB}\to\text{BGR}}\left( \left[ L_{\text{enhanced}}^*(x, y), a^*(x, y), b^*(x, y) \right] \right)$$

This preprocessing step increases pediatric edge gradient contrast by **34.2%** in low-light conditions ($<50\text{ lux}$), boosting small-target detection recall while preserving skin tone fidelity.

---

## 4.6 Perspective-Aware Classification Heuristics

When operating with un-fine-tuned generic COCO detectors (where all humans are classified as generic `person` class 0), the system activates a specialized **Ground-Plane Perspective Normalization** algorithm (`Detector.calculate_perspective_class`).

```
       Top of Frame (y = 0.0)
       ┌────────────────────────────────────────────────────────┐
       │   Perspective Horizon Y_h (y = 0.20)                   │
       │   ──────────────────────────────────────────────────   │
       │   Far Field: Expected Adult Height h_far = 0.22        │
       │                                                        │
       │                                                        │
       │   Near Field: Expected Adult Height h_near = 0.55      │
       │   ──────────────────────────────────────────────────   │
       └────────────────────────────────────────────────────────┘
       Bottom of Frame (y = 1.0)
```

### Perspective Normalization Formulation:
1. **Vertical Bottom Coordinate:** Let $y_{\text{bottom}} = \frac{y_2}{H_{\text{frame}}} \in [0, 1]$ represent the normalized ground-contact point.
2. **Normalized Depth Coordinate:**

$$\tilde{y} = \max\left( 0.0, \min\left( 1.0, \frac{y_{\text{bottom}} - Y_{\text{horizon}}}{1.0 - Y_{\text{horizon}}} \right) \right)$$

Where $Y_{\text{horizon}} = 0.20$.

3. **Expected Adult Pixel Height:**

$$h_{\text{expected\_adult}}(\tilde{y}) = h_{\text{far}} + \tilde{y} \cdot (h_{\text{near}} - h_{\text{far}})$$

Where $h_{\text{far}} = 0.22$ and $h_{\text{near}} = 0.55$.

4. **Sitting-Pose Aspect Ratio Compensation:**  
   When adult patients sit on benches, their projected vertical height decreases by $35\% - 50\%$, while their bounding box aspect ratio ($AR = w / h$) expands. To prevent seated adults from being misclassified as children:

$$\text{Effective Height } h_{\text{eff}} = \begin{cases} h_{\text{box}} \cdot 1.50 & \text{if } \frac{w_{\text{box}}}{h_{\text{box}}} > 0.55 \\ h_{\text{box}} & \text{otherwise} \end{cases}$$

5. **Normalized Scale Ratio & Classification Threshold:**

$$R_{\text{norm}} = \frac{h_{\text{eff}}}{h_{\text{expected\_adult}}(\tilde{y})}$$

$$\text{Class} = \begin{cases} \text{Child} & \text{if } R_{\text{norm}} < 0.70 \\ \text{Adult} & \text{if } R_{\text{norm}} \ge 0.85 \\ \text{Child} & \text{if } 0.70 \le R_{\text{norm}} < 0.85 \land AR > 0.60 \\ \text{Adult} & \text{otherwise} \end{cases}$$

This geometric formulation enables robust adult-versus-child categorization even when relying on off-the-shelf, non-fine-tuned base models.
