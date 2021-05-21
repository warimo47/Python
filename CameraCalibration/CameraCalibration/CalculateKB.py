import numpy as np
import numpy.linalg as lin
import cv2
import math

fileName = "Image/CT50P0.png"

# uvPoint = np.array([[0.0], [0.0], [1.0]])
# 
# intrinsicMat = np.array([[1948, 0.0, 960.0], [0.0, 3224, 540.0], [0.0, 0.0, 1.0]])
# print("카메라 내부 매트릭스")
# print(intrinsicMat)
# 
# invertibleMat_intrinsicMat = lin.inv(intrinsicMat)
# print("\n카메라 내부 매트릭스 역행렬")
# print(invertibleMat_intrinsicMat)
# 
# extrinsicMat = np.array([ \
#     [1.0, 0.0, 0.0, 0.0], \
#     [0.0, math.cos(-1.91986), - math.sin(-1.91986), 0.0], \
#     [0.0, math.sin(-1.91986), math.cos(-1.91986), 4.8], \
#     [0.0, 0.0, 0.0, 1.0]])
# 
# print("\n카메라 외부 매트릭스")
# print(extrinsicMat)
# 
# invertibleMat_extrinsicMat = lin.inv(extrinsicMat)
# print("\n카메라 외부 매트릭스 역행렬")
# print(invertibleMat_extrinsicMat)
# 
# cut_invertibleMat_extrinsicMat = invertibleMat_extrinsicMat.T[:, 0:3]
# print("\n카메라 외부 매트릭스 역행렬'")
# print(cut_invertibleMat_extrinsicMat)

mtx = np.array([[1811.001456721, 0, 989.228699478], [0, 1957.971952606, 723.879227634], [0, 0, 1]])

degree_AxisX = 132.306849
degree_AxisY = 0.011895
degree_AxisZ = 2.290061

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

print("Mat R")
print(R)

rvecs = np.array([[2.308811288], [-0.046252689], [0.020158312]])

tvecs = np.array([[-0.015059964], [0.724811501], [0.694086324]])

rodriguesR = np.zeros(shape = (3, 3))

cv2.Rodrigues(rvecs, rodriguesR)
print("\nRodrigues R")
print(rodriguesR)
# R = rodriguesR

def leftMouseDown(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        target_pixel = [x, y]
        print("\nMouse U : " + str(x) + " V : " + str(y))

        norm_camera_frame = np.array([[(target_pixel[0] - mtx[0][2]) / mtx[0][0]], [(target_pixel[1] - mtx[1][2]) / mtx[1][1]], [1]])
        s = np.dot(R.T, tvecs)[2] / np.dot(R.T, norm_camera_frame)[2]
        result = np.dot(R.T, norm_camera_frame) * s - np.dot(R.T, tvecs)
        print(str(result[0]) + " " + str(result[1]) + " " + str(result[2]))

cv2.namedWindow("calibration")
cv2.setMouseCallback("calibration", leftMouseDown)

image1 = cv2.imread(fileName)
cv2.imshow("calibration", image1)

while True:
    if cv2.waitKey() == ord('q'):
        print("done.")
        break