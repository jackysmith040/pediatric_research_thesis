# Chapter 11: Appendices

---

## Appendix A: System Configuration & Hyperparameter Schema

The system configuration is centralized within the `Settings` class (`src/engine/config.py`), which introspects environment variables (`.env`) with strict typing enforced via Pydantic:

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Neural Model Parameters
    MODEL_PATH: str = "models/fine_tuned/pediatric-model.pt"
    CONFIDENCE_THRESHOLD: float = 0.45
    IOU_THRESHOLD: float = 0.40
    PEDIATRIC_CONF_THRESHOLD: float = 0.30
    MAX_FRAME_WIDTH: int = 1280

    # CLAHE Illumination Preprocessing
    ENABLE_CLAHE: bool = True
    CLAHE_CLIP_LIMIT: float = 2.0
    CLAHE_TILE_GRID_SIZE: int = 8

    # Roboflow Supervision & ByteTrack Parameters
    TRACKER_CONFIG: str = "bytetrack.yaml"
    ID_EXPIRY_SECONDS: int = 30
    UNTRACKED_SPATIAL_MATCH_RADIUS: float = 40.0
    BYTETRACK_TRACK_THRESH: float = 0.30
    BYTETRACK_MATCH_THRESH: float = 0.80
    BYTETRACK_FRAME_RATE: int = 30

    # Perspective Normalization & Aspect Ratio Heuristics
    ENABLE_PERSPECTIVE_CORRECTION: bool = True
    PERSPECTIVE_HORIZON_Y: float = 0.20
    PERSPECTIVE_FAR_HEIGHT_RATIO: float = 0.22
    PERSPECTIVE_NEAR_HEIGHT_RATIO: float = 0.55
    TEMPORAL_VOTING_WINDOW: int = 15

    # Multi-Tracker Engine & Adaptive Scene Switching
    DEFAULT_TRACKER_MODE: str = "auto"
    AUTO_SWITCH_STABILIZATION_SECONDS: float = 3.0
    CAMERA_MOTION_THRESHOLD: float = 12.0
    OCCLUSION_DENSITY_THRESHOLD: float = 0.25

    # Clinical Triage Overcrowding Logic
    WAITING_ROOM_CAPACITY: int = 50
    PEDIATRIC_ALERT_THRESHOLD_PERCENT: float = 30.0
    CAMERA_ID: str = "outpatient_waiting_cctv_01"
    VIDEO_SOURCE: str = "0"

    # Class Mappings (Fine-Tuned Weights: 0=Adult, 1=Child)
    ADULT_CLASS_ID: int = 0
    CHILD_CLASS_ID: int = 1
```

---

## Appendix B: Mathematical Derivations

### B.1 Derivation of Complete Intersection-over-Union (CIoU) Loss
Let $B = (x, y, w, h)$ be the predicted bounding box and $B^{\text{gt}} = (x^{\text{gt}}, y^{\text{gt}}, w^{\text{gt}}, h^{\text{gt}})$ be the ground-truth box.

The intersection $\mathcal{I}$ and union $\mathcal{U}$ are:
$$\mathcal{I} = \max(0, \min(x_2, x_2^{\text{gt}}) - \max(x_1, x_1^{\text{gt}})) \times \max(0, \min(y_2, y_2^{\text{gt}}) - \max(y_1, y_1^{\text{gt}}))$$
$$\mathcal{U} = \text{Area}(B) + \text{Area}(B^{\text{gt}}) - \mathcal{I}$$
$$\text{IoU} = \frac{\mathcal{I}}{\mathcal{U}}$$

The centroid Euclidean distance penalty is:
$$\mathcal{R}_{\text{distance}} = \frac{\rho^2(b, b^{\text{gt}})}{c^2} = \frac{(x - x^{\text{gt}})^2 + (y - y^{\text{gt}})^2}{c_w^2 + c_h^2}$$

Where $c$ is the diagonal length of the smallest enclosing box covering both $B$ and $B^{\text{gt}}$.

The aspect ratio consistency parameter $v$ and balancing weight $\alpha$ are:
$$v = \frac{4}{\pi^2} \left( \arctan\frac{w^{\text{gt}}}{h^{\text{gt}}} - \arctan\frac{w}{h} \right)^2$$
$$\alpha = \frac{v}{(1 - \text{IoU}) + v}$$

The complete loss minimized during backpropagation is:
$$\mathcal{L}_{\text{CIoU}} = 1 - \text{IoU} + \frac{\rho^2(b, b^{\text{gt}})}{c^2} + \alpha v$$

### B.2 CLAHE Histogram Pixel Redistribution Formula
For an image tile with $N_{\text{pixels}}$ total pixels and $L = 256$ histogram bins, let the clip limit factor be $\beta \ge 1.0$. The maximum permitted count per bin $N_{\text{clip}}$ is:

$$N_{\text{clip}} = \frac{N_{\text{pixels}}}{L} + \frac{\beta}{L} (N_{\text{pixels}} - \frac{N_{\text{pixels}}}{L})$$

Total excess clipped pixels $N_{\text{excess}}$:
$$N_{\text{excess}} = \sum_{k=0}^{L-1} \max(0, h_k - N_{\text{clip}})$$

Uniform redistribution step per bin $\Delta h$:
$$\Delta h = \frac{N_{\text{excess}}}{L}$$

Adjusted histogram $h'_k$:
$$h'_k = \min(h_k, N_{\text{clip}}) + \Delta h$$

The normalized Cumulative Distribution Function (CDF) mapping $T(k)$ is:
$$T(k) = \text{round}\left( \frac{L - 1}{\sum_{j=0}^{L-1} h'_j} \sum_{j=0}^k h'_j \right)$$

---

## Appendix C: Automated Test Suite Architecture & Verification Protocols

The system includes a 100% passing automated test suite (`tests/unit/`) executed via Pytest:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     UNIT TEST SUITE ARCHITECTURE                        │
│                                                                         │
│  Test Module                  Tests Covered    Status                   │
│  ─────────────────────────────────────────────────────────────────────  │
│  test_counter.py              7 Test Cases     PASS (100%)              │
│  test_detector.py             17 Test Cases    PASS (100%)              │
│  test_stream_resolver.py      5 Test Cases     PASS (100%)              │
│  test_tracker_engine.py       5 Test Cases     PASS (100%)              │
│  ─────────────────────────────────────────────────────────────────────  │
│  TOTAL SUITE VERIFICATION:    34 / 34 PASSED   PASS (Zero Errors)       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Test Cases Verified:
- `test_counter_spatial_debounce`: Asserts that re-appearing lost tracks within $150\text{ px}$ radius do not increment cumulative patient totals.
- `test_detector_clahe_preprocessing`: Asserts that CLAHE preserves BGR array dimensions and improves luminance contrast.
- `test_detector_perspective_normalization`: Asserts that standing children, standing adults, and seated adults receive correct perspective class assignments.
- `test_stream_resolver_youtube_and_webcam`: Verifies dynamic input resolution across webcam indices, local files, and YouTube URLs.
- `test_tracker_engine_auto_switching`: Verifies that camera motion ($\Delta I > 12.0$) and crowd occlusion ($\Omega > 0.25$) trigger tracker auto-switching subject to $3.0\text{-second}$ hysteresis barriers.
