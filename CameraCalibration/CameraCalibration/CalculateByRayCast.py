import numpy as np
import numpy.linalg as lin
import cv2
import math

fileName = "Image/BT50P0.png"

mtx = np.array([[1804.511, 0, 960], [0, 1894.737, 540], [0, 0, 1]])
tvecs = np.array([[0.030584481], [0.190627691], [1.454587318]])
degree_AxisX = 130
degree_AxisY = 0
degree_AxisZ = 0
AxisX_R = np.array([[1, 0, 0], \
    [0, math.cos(math.radians(degree_AxisX)), - math.sin(math.radians(degree_AxisX))], \
    [0, math.sin(math.radians(degree_AxisX)), math.cos(math.radians(degree_AxisX))]])
AxisY_R = np.array([[math.cos(math.radians(degree_AxisY)), 0, - math.sin(math.radians(degree_AxisY))], \
    [0, 1, 0], \
    [math.sin(math.radians(degree_AxisY)), 0, math.cos(math.radians(degree_AxisY))]])
AxisZ_R = np.array([[math.cos(math.radians(degree_AxisZ)), - math.sin(math.radians(degree_AxisZ)), 0], \
    [math.sin(math.radians(degree_AxisZ)), math.cos(math.radians(degree_AxisZ)), 0], \
    [0, 0, 1]])
R = AxisX_R @ AxisY_R @ AxisZ_R

def leftMouseDown(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        target_pixel = [x, y]
        print("\nMouse : %d , %d (px)" %(x, y))

        norm_camera_frame = np.array([[(target_pixel[0] - mtx[0][2]) / mtx[0][0]], [(target_pixel[1] - mtx[1][2]) / mtx[1][1]], [1]])
        s = np.dot(R.T, tvecs)[2] / np.dot(R.T, norm_camera_frame)[2]
        result = np.dot(R.T, norm_camera_frame) * s - np.dot(R.T, tvecs)
        print("World : %.6f , %.6f , %.1f (m)" %(result[0], result[1], result[2]))

cv2.namedWindow("calibration")
cv2.setMouseCallback("calibration", leftMouseDown)

image1 = cv2.imread(fileName)
cv2.imshow("calibration", image1)

while True:
    if cv2.waitKey() == ord('q'):
        print("done.")
        break