import numpy as np
import cv2
import timeit

# True 2D coordinate values
points_world3d = []

# Read image pixel coordinates by file( Must use more than 2 file )
point2D_UVs = []

fileName = "TileT60P0_1"

with open("Text/" + fileName + ".txt") as data:
    for line in data.readlines():
        u = int(line.split(',')[0])
        v = int(line.split(',')[1])
        x = int(line.split(',')[2])
        y = int(line.split(',')[3])
        point2D_UVs.append([u, v])
        points_world3d.append([x, y, 0])

world3D_points = [np.array(points_world3d).astype(np.float32)]
uv2D_points = [np.array(point2D_UVs).astype(np.float32)]

# Get image size
img1 = cv2.imread("Image/TileT60P0.png")
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

print("\nworld3D_points")
print(world3D_points)

# print('\nuv2D_points')
# print(uv2D_points)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(world3D_points, uv2D_points, gray.shape[::-1], None, None)

# print("Ret")
# print(ret)
print("\nmtx")
# print(mtx)
print(mtx[0])
print(mtx[1])
print(mtx[2])
# print("\ndist")
# print(dist)
print("\nrvecs")
print(rvecs[0])
print("\ntvecs")
print(tvecs[0])
