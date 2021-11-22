# HSV limit finding from webcam feed

import cv2
import numpy as np

def empty(a):  # argument required
    pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

cap = cv2.VideoCapture(0) # 0 - default webcam
cap.set(3, 640) # width
cap.set(4, 480) # height
cap.set(10, 100) # brightness

cv2.namedWindow('Trackbars')  # Creating trackbars to isolate required color
cv2.resizeWindow('Trackbars', 640, 240)

# cv2.createTrackbar('H minimum', 'Trackbars', 0, 179, empty) # 180 hues available in opencv (lower and upper limits for trackbars), empty is a function called each time the trackbar is changed
# cv2.createTrackbar('H maximum', 'Trackbars', 179, 179, empty) # initial trackbars for color detection and limit identification
# cv2.createTrackbar('S minimum', 'Trackbars', 0, 255, empty)
# cv2.createTrackbar('S maximum', 'Trackbars', 255, 255, empty)
# cv2.createTrackbar('V minimum', 'Trackbars', 0, 255, empty)
# cv2.createTrackbar('V maximum', 'Trackbars', 255, 255, empty)

cv2.createTrackbar('H minimum', 'Trackbars', 29, 179, empty)  # trackbars for specific colour
cv2.createTrackbar('H maximum', 'Trackbars', 146, 179, empty)
cv2.createTrackbar('S minimum', 'Trackbars', 13, 255, empty)
cv2.createTrackbar('S maximum', 'Trackbars', 93, 255, empty)
cv2.createTrackbar('V minimum', 'Trackbars', 66, 255, empty)
cv2.createTrackbar('V maximum', 'Trackbars', 127, 255, empty)

while True:

    success, img = cap.read() # <successful execution (boolean)>, <image variable>

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # conversion to HSV from BGR

    hMin = cv2.getTrackbarPos('H minimum', 'Trackbars')
    hMax = cv2.getTrackbarPos('H maximum', 'Trackbars')
    sMin = cv2.getTrackbarPos('S minimum', 'Trackbars')
    sMax = cv2.getTrackbarPos('S maximum', 'Trackbars')
    vMin = cv2.getTrackbarPos('V minimum', 'Trackbars')
    vMax = cv2.getTrackbarPos('V maximum', 'Trackbars')
    # print(hMin, hMax, sMin, sMax, vMin, vMax)

    lower = np.array([hMin, sMin, vMin])  # minimum range array
    upper = np.array([hMax, sMax, vMax])  # maximum range array
    mask = cv2.inRange(imgHSV, lower, upper)  # filtering out colours from HSV image
    imgResult = cv2.bitwise_and(img, img,mask=mask)  # adds two images and creates a new one where non black colours on the mask are given colour from the original

    imgStacked = stackImages(0.5, ([img, mask, imgResult]))

    cv2.imshow('Test window', imgStacked)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print()
print('Required values : ')
print('hMin, sMin, vMin, hMax, sMax, vMax = ', hMin, ',', sMin, ',', vMin, ',', hMax, ',', sMax, ',', vMax)
