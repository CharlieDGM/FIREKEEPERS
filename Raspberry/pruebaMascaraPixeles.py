import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_color = np.array([40, 50, 50])
    upper_color = np.array([80, 255, 255])

    mask = cv2.inRange(hsv, lower_color, upper_color)

    num_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    percentage = (num_pixels * 100) / total_pixels

    #print("Percentage of pixels in the specified color range: ", percentage)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    #cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()