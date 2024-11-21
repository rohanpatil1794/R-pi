import cv2
import numpy as np
cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)
while True:
    ret, frame = cap.read()
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()