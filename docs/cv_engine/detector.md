# 👁️ CV Engine: `detector.py`

## What does `detector.py` do?
This is the heavy lifter. The `detector.py` file is where the actual Artificial Intelligence lives. It loads the YOLOv26 neural network and feeds the camera video into it frame by frame.

### The Problem it Solves:
Object detection takes time. If a camera is shooting video at 30 frames per second, but the AI takes 0.1 seconds to think about a frame, the video will stutter and lag horribly. 

### The Solution (Decoupled Threading):
To fix the lag, the `Detector` class uses Python `threading`. It creates two completely separate mini-programs (threads) that run at the same time:
1. **The Capture Thread (`_capture_loop`):** This thread does nothing but pull the absolute newest picture from the camera as fast as possible.
2. **The YOLO Thread (`_yolo_loop`):** This thread grabs the newest picture, feeds it to the AI, and saves the coordinates of where the people are.

Because these two tasks are separated, the video stream remains incredibly smooth (Zero-Latency) even if the AI is running on a slow computer!

### Drawing the UI:
The file also contains `draw_bbox` and `draw_trail`. These functions use the OpenCV library (`cv2`) to draw the colorful squares around people and the little trails that follow them as they move.

---

### 🧸 Explain Like I'm 5 (ELI5)
Imagine you are trying to draw portraits of cars driving by on a highway. If you stop to draw a highly detailed portrait of one car (the AI inference), 50 other cars will zoom by while you aren't looking! 
To fix this, you get a friend with a camera (the Capture Thread). Your friend just snaps photos of the highway as fast as possible. When you finish your drawing, you ask your friend for their *absolute newest* photo and start drawing that one. You might miss a few cars in between, but the highway never stops moving!

---

### 👩‍💻 How to Contribute
If you want to change how the video looks—like changing the colors of the boxes, adding new text to the screen, or drawing circles instead of squares—this is the file you edit. Look for the `cv2.putText` and `cv2.rectangle` lines inside the `get_frame_generator()` and `draw_bbox()` functions!
