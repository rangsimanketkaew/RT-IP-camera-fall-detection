import cv2
# For laptop, 0 is rear camera and 1 is front camera
cap = cv2.VideoCapture(1)

while True:
    ret, img = cap.read()
    cv2.imshow('Video', img)
    if(cv2.waitKey(10) & 0xFF == ord('b')):
        break
