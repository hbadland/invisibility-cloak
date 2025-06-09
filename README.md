# 🧥 Invisibility Cloak (OpenCV)

Real‑time “invisibility” effect implemented with **Python + OpenCV**.  
A uniformly‑coloured cloak (red, blue, or green) is replaced by the pre‑captured background, making the wearer appear transparent on‑screen.

---

## 🏗 How It Works

1. **Background Capture** – grab 30 frames at startup (3 s delay) and average one to form a static background.  
2. **HSV Masking** – convert each frame to HSV, blur to reduce noise, and threshold the selected colour range.  
3. **Morphological Cleaning** – `cv2.morphologyEx` removes small blobs / holes in the mask.  
4. **Segmentation** –  
   ```python
   cloak_area  = bitwise_and(background, background, mask=mask)
   non_cloak   = bitwise_and(frame, frame, mask=~mask)
   output      = cloak_area + non_cloak
