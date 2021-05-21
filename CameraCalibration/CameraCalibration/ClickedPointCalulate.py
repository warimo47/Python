import numpy as np
import numpy.linalg as lin
import cv2
import math

# R = np.zeros(shape = (3, 3))
# 
# rvecs = np.array([[1.98338315], [0.08760511], [-0.09096691]])
# tvecs = np.array([[0.12398641], [3.77633495], [1.37988607]])
# 
# cv2.Rodrigues(rvecs, R)
# norm_camera_frame = np.zeros(shape = tvecs.shape).astype(np.float32)

mtx = [[1900.880609204, 0, 925.055519672], [0, 1893.851243872, 600.951582528], [0, 0, 1]]

degreeX = 132.183557
degreeY = 1.140147833
degreeZ = -9.835780167

AxisX_R = np.array([[1, 0, 0], \
    [0, math.cos(math.radians(degreeX)), - math.sin(math.radians(degreeX))], \
    [0, math.sin(math.radians(degreeX)), math.cos(math.radians(degreeX))]])

AxisY_R = np.array([[math.cos(math.radians(degreeY)), 0, - math.sin(math.radians(degreeY))], \
    [0, 1, 0], \
    [math.sin(math.radians(degreeY)), 0, math.cos(math.radians(degreeY))]])

AxisZ_R = np.array([[math.cos(math.radians(degreeZ)), - math.sin(math.radians(degreeZ)), 0], \
    [math.sin(math.radians(degreeZ)), math.cos(math.radians(degreeZ)), 0], \
    [0, 0, 1]])

R = AxisX_R @ AxisY_R @ AxisZ_R

tvecs = np.array([[0.204066591], [0.191560653], [1.450389809]])

def leftMouseDown(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        target_pixel = [x, y]
        print("\nMouse X : " + str(x) + " Y : " + str(y))
        norm_camera_frame = np.array([[(target_pixel[0] - mtx[0][2]) / mtx[0][0]],\
            [(target_pixel[1] - mtx[1][2]) / mtx[1][1]], [1.0]])

        s = np.dot(R.T, tvecs)[2] / np.dot(R.T, norm_camera_frame)[2]

        result = np.dot(R.T, norm_camera_frame) * s - np.dot(R.T, tvecs)

        print("\nWorld : %.6f %.6f %.6f" %(result[0],result[1],result[2]))

cv2.namedWindow("calibration")
cv2.setMouseCallback("calibration", leftMouseDown)

image1 = cv2.imread("Image/BT50P_10.png")
cv2.imshow("calibration", image1)

while True:
    if cv2.waitKey() == ord('q'):
        print("done.")
        break