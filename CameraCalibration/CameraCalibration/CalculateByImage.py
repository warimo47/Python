import numpy as np
import numpy.linalg as lin
import cv2
import math

fileName = "Image/PointsCT50P0.png"

# mtx = np.array([[1811.001456721, 0, 989.228699478], [0, 1957.971952606, 723.879227634], [0, 0, 1]])
mtx = np.array([[1804.511, 0, 960], [0, 1894.737, 540], [0, 0, 1]])

# degree_AxisX = 132.306849
degree_AxisX = 130.0
# degree_AxisY = 0.011895
degree_AxisY = 0.0
# degree_AxisZ = 2.290061
degree_AxisZ = 0.0

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

cv2.namedWindow("calibration")

image1 = cv2.imread(fileName)
cv2.imshow("calibration", image1)

for row in range(1080):
    for col in range(1920):
        # print("\n[" + str(col) + ", " + str(row) + "] " + str(image1[row, col][0]) + " " + str(image1[row, col][1]) + " " + str(image1[row, col][2]))
        if image1[row, col][0] == 255 and image1[row, col][1] == 0 and image1[row, col][2] == 255 :
            target_pixel = [col, row]
            print("\n U : " + str(col) + " V : " + str(row))
            norm_camera_frame = np.array([[(target_pixel[0] - mtx[0][2]) / mtx[0][0]], [(target_pixel[1] - mtx[1][2]) / mtx[1][1]], [1]])
            s = np.dot(R.T, tvecs)[2] / np.dot(R.T, norm_camera_frame)[2]
            result = np.dot(R.T, norm_camera_frame) * s - np.dot(R.T, tvecs)
            print(str(result[0]) + " " + str(result[1]) + " " + str(result[2]))