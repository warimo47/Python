import numpy as np
import cv2
import timeit

# True 2D coordinate values
points_world3d = []

# Read image pixel coordinates by file( Must use more than 2 file )
world3D_points = []
uv2D_points = []

point2D_UVs = []

fileNames = ["CT45P_5", "CT45P0", "CT45P5", \
    "CT50P_5", "CT50P0", "CT50P5", \
    "CT55P_5", "CT55P0", "CT55P5", \
    "CT60P_5", "CT60P0", "CT60P5"]

for idx, fn in enumerate(fileNames):
    with open("Text/" + fn + ".txt") as data:
        for line in data.readlines():
            u = int(line.split(',')[0])
            v = int(line.split(',')[1])
            x = float(line.split(',')[2])
            y = float(line.split(',')[3])            
            point2D_UVs.append([u, v])
            points_world3d.append([x, y, 0])

    world3D_points.append(np.array(points_world3d).astype(np.float32))
    uv2D_points.append(np.array(point2D_UVs).astype(np.float32))
    point2D_UVs = []
    points_world3d = []

# Get image size
img1 = cv2.imread("Image/CT50P0.png")
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# print("\nworld3D_points")
# print(world3D_points)

# print('\nuv2D_points')
# print(uv2D_points)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(world3D_points, uv2D_points, gray.shape[::-1], None, None)

# print("Ret")
# print(ret)
print("\nmtx")
# print(mtx)
print(str(mtx[0][0]) + "," + str(mtx[0][1]) + "," + str(mtx[0][2]))
print(str(mtx[1][0]) + "," + str(mtx[1][1]) + "," + str(mtx[1][2]))
print(str(mtx[2][0]) + "," + str(mtx[2][1]) + "," + str(mtx[2][2]))
# print("\ndist")
# print(dist)
print("\nrvecs tvecs")
for idxR, rv in enumerate(rvecs):
    print(str(rv[0][0]) + ",,,,," + str(tvecs[idxR][0][0]))
    print(str(rv[1][0]) + ",,,,," + str(tvecs[idxR][1][0]))
    print(str(rv[2][0]) + ",,,,," + str(tvecs[idxR][2][0]))

rodriguesR = np.zeros(shape = (3, 3))

print("\nRodrigues R")
for rr in rvecs:
    cv2.Rodrigues(rr, rodriguesR)
    print(str(rodriguesR[0][0]) + "," + str(rodriguesR[0][1]) + "," + str(rodriguesR[0][2]))
    print(str(rodriguesR[1][0]) + "," + str(rodriguesR[1][1]) + "," + str(rodriguesR[1][2]))
    print(str(rodriguesR[2][0]) + "," + str(rodriguesR[2][1]) + "," + str(rodriguesR[2][2]))

