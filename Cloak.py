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

while video.isOpened(): # Standard OpenCV loop to check video open
    success, frame = video.read()
    if not success:
        break # Breaks if webcam not accessible

    frame = np.flip(frame, axis=1) # Flip the frame
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV for filtering masking etc
    blurred_hsv = cv2.GaussianBlur(hsv_img, (35, 35), 0) # Reduce fluctuations / noise

    # Range 1: deeper blue
    lower_blue1 = np.array([90, 150, 50])
    upper_blue1 = np.array([110, 255, 255])

    # Range 2: lighter / more cyan blue
    lower_blue2 = np.array([111, 100, 50])
    upper_blue2 = np.array([130, 255, 255])

    # Combine both ranges
    mask1 = cv2.inRange(blurred_hsv, lower_blue1, upper_blue1)
    mask2 = cv2.inRange(blurred_hsv, lower_blue2, upper_blue2)
    mask = cv2.bitwise_or(mask1, mask2)

    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

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



