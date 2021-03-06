import numpy as np
import cv2
import serial
import time
import argparse
import sys

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to detect")
args = vars(ap.parse_args())

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["type"]))
	sys.exit(0)
# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
arucoParams = cv2.aruco.DetectorParameters_create()
# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")

cap = cv2.VideoCapture(2)
c1 = 0
linecolor = (100, 215, 255)
lwr_red = np.array([0, 0, 0])
upper_red = np.array([179, 65, 55])
countl = False
countr = False
Ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)
Ser.flush()
width = cap.get(3)
while True:
    ret, frame = cap.read()
    if not ret:
        _, frame = cap.read()

    # detect ArUco markers in the input frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
    arucoDict, parameters=arucoParams)


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.inRange(hsv, lwr_red, upper_red)
    mask = cv2.dilate(mask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # verify at least one ArUco marker was detected
    if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()
        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned
            # in top-left, top-right, bottom-right, and bottom-left
            # order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            # draw the bounding box of the ArUCo detection
            cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
            # compute and draw the center (x, y)-coordinates of the
            # ArUco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
        # draw the ArUco marker ID on the frame

        cv2.putText(frame, str(markerID),
                    (topLeft[0], topLeft[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        if markerID == 0:
            if not countl:
                countr = False
                countl=True
                i='f'
                for lp in range(12):
                    Ser.write(i.encode())
                    time.sleep(0.1)
                cv2.putText(frame, '<--', (5, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
                print("Left")
                i = 'l' # left turn
                for lp in range(6):
                    Ser.write(i.encode())
                    time.sleep(0.5)
                i='f'
                for lp in range(7):
                    Ser.write(i.encode())
                    time.sleep(0.1)
        elif markerID == 1:
            if not countr:
                countl = False
                countr=True
                i='f'
                for lp in range(8):
                    Ser.write(i.encode())
                    time.sleep(0.1)
                i = 'r' # left turn
                cv2.putText(frame, '-->', (5, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
                print("Right")
                for lp in range(6):
                    Ser.write(i.encode())
                    time.sleep(0.5)
        else:
            i = 'x'
            Ser.write(i.encode())
            print("Invalid")

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 3:
            # cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 255), 2)
            cv2.circle(frame, center, 5, linecolor, -1)

        if (x > 0.25 * width and x <= 0.75 * width):
            print('Forward')
            cv2.putText(frame, '^', (5, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
            Ser.write(b'f')
            # time.sleep(0.01)

    else:
        print("Track Not Visible")
        c1 += 1
        if (c1 == 5):
            print("Backward")
            cv2.putText(frame, 'V', (5, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
            Ser.write(b'b')
            c1 = 0

    time.sleep(0.2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        Ser.close()
        cv2.destroyAllWindows()
        break