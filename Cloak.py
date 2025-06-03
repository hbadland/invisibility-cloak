import os
import numpy as np
import time
import cv2

video = cv2.VideoCapture(0)
time.sleep(3) # 3 sec delay for camera focus

bg_frame = None
for _ in range(30): # Capture 30 frames
    success, bg_frame = video.read() # Reads frame from webcam

bg_frame = np.flip(bg_frame, axis=1) # Flip the webcam needs to be flipped before loop

HSV_RANGES = {
    "blue": {
        "lower": [np.array([90, 150, 50]), np.array([111, 100, 50])],
        "upper": [np.array([110, 255, 255]), np.array([130, 255, 255])]
    },
    "red": {
        "lower": [np.array([0, 120, 70]), np.array([170, 120, 70])],
        "upper": [np.array([10, 255, 255]), np.array([180, 255, 255])]
    },
    "green": {
        "lower": [np.array([35, 100, 50])],
        "upper": [np.array([85, 255, 255])]
    }
}

cloak_color = input("Choose cloak color (blue, red, green): ").strip().lower()
if cloak_color not in HSV_RANGES:
    print("Unsupported color.")
    exit(1)

while video.isOpened(): # Standard OpenCV loop to check video open
    success, frame = video.read()
    if not success:
        break # Breaks if webcam not accessible

    frame = np.flip(frame, axis=1) # Flip the frame
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV for filtering masking etc
    blurred_hsv = cv2.GaussianBlur(hsv_img, (35, 35), 0) # Reduce fluctuations / noise

    # HSV bounds for selected color
    lower_bounds = HSV_RANGES[cloak_color]["lower"]
    upper_bounds = HSV_RANGES[cloak_color]["upper"]

    # Mask from HSV bands
    mask = cv2.inRange(blurred_hsv, lower_bounds[0], upper_bounds[0])
    for i in range(1, len(lower_bounds)):
        mask |= cv2.inRange(blurred_hsv, lower_bounds[i], upper_bounds[i])

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # frame[np.where(mask == 255)] = bg_frame[np.where(mask == 255)]

    cloak_area = cv2.bitwise_and(bg_frame, bg_frame, mask=mask)
    non_cloak = cv2.bitwise_and(frame, frame, mask = cv2.bitwise_not(mask))
    frame = cv2.add(cloak_area, non_cloak)

    cv2.imshow("frame", frame)

    # Exit option with 'esc'
    if cv2.waitKey(10) == 27:
        break

video.release()
cv2.destroyAllWindows()



