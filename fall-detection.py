# Based on Zed code - Person Fall detection using raspberry pi camera and opencv lib.
# Link: https://www.youtube.com/watch?v=eXMYZedp0Uo
#
# Improvement by Rangsiman Ketkaew
# - Support IP camera and stream video

import cv2
import time

######################
ip_cam = '192.168.1.64/1'
username = 'admin'
password = '12345'
fitToEllipse = False
######################

# Video clip
# cap = cv2.VideoCapture('abc.mp4')
# IP camera
# cap = cv2.VideoCapture(f'rtsp://{username}:{password}@{ip_cam}')
# Laptop camera
cap = cv2.VideoCapture(1)

print("Fall detection")
time.sleep(2)

fgbg = cv2.createBackgroundSubtractorMOG2()
f = 0
j = 0

while(True):
    ret, frame = cap.read()

    # Convert each frame to gray scale and subtract the background
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)

        # Find contours
        contours, _ = cv2.findContours(
            fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:

            # List to hold all areas
            areas = []

            for contour in contours:
                ar = cv2.contourArea(contour)
                areas.append(ar)

            max_area = max(areas, default=0)

            max_area_index = areas.index(max_area)

            cnt = contours[max_area_index]

            M = cv2.moments(cnt)

            x, y, w, h = cv2.boundingRect(cnt)

            cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 3, maxLevel=0)

            if h < w:
                j += 1

            if j > 10:
                print(f"FALL !! ==> {f+1}")
                f += 1
                #cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            if h > w:
                j = 0
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('video', frame)

            if cv2.waitKey(33) == 27:
                break

    except Exception as e:
        break

cv2.destroyAllWindows()
