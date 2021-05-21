import numpy as np
import cv2
import timeit

# True 2D coordinate values
points_world3d = []

for j in range(10, 20, 2):
    for i in range(4, -5, -2):
        points_world3d.append([i, j, 0])
        # print(str(i) + " " + str(j))

#print("points_world3d")
#print(points_world3d)

# Read image pixel coordinates by file( Must use more than 2 file )
points_img1 = []

with open("points_img1.txt") as data:
    for line in data.readlines():
        x = int(line.split(',')[0])
        y = int(line.split(',')[1])
        points_img1.append([x, y])

points_img2 = []

with open("points_img2.txt") as data:
    for line in data.readlines():
        x = int(line.split(',')[0])
        y = int(line.split(',')[1])
        points_img2.append([x, y])

obj_points = [np.array(points_world3d).astype(np.float32), np.array(points_world3d).astype(np.float32)]
img_points = [np.array(points_img1).astype(np.float32), np.array(points_img2).astype(np.float32)]

# Get image size
img1 = cv2.imread("image1_result.png")
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

print('\nobj_points')
print(obj_points)

print('\nimg_points')
print(img_points)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

print('Ret')
print(ret)
print('\nmtx')
print(mtx)
# print(mtx[0])
# print(mtx[1])
# print(mtx[2])
print('\ndist')
print(dist)
print('\nrvecs')
print(rvecs)
# print(rvecs[0])
# print(rvecs[1])
print('\ntvecs')
print(tvecs)
# print(tvecs[0])
# print(tvecs[1])

# Calculate
cal_time = timeit.default_timer()

errors = []

for image_num in range(0, 1):
    for point_num in range(0, 25):

        target_pixel = img_points[image_num][point_num]

        u = target_pixel[0]
        v = target_pixel[1]

        fx = mtx[0][0]
        fy = mtx[1][1]
        cx = mtx[0][2]
        cy = mtx[1][2]

        R = np.zeros(shape = (3, 3))
        cv2.Rodrigues(rvecs[image_num], R)

        t = tvecs[image_num]

        norm_camera_frame = np.zeros(shape = t.shape).astype(np.float32)
        norm_camera_frame[0] = (u - cx) / fx
        norm_camera_frame[1] = (v - cy) / fy
        norm_camera_frame[2] = 1.0

        s = np.dot(R.T, t)[2] / np.dot(R.T, norm_camera_frame)[2]

        result = np.dot(R.T, norm_camera_frame) * s - np.dot(R.T, t)

        #print("Result : ", result.T[0])
        #print("True value : ", obj_points[image_num][point_num])

        error = np.linalg.norm(result.T[0] - obj_points[image_num][point_num])
        errors.append(error)

terminate_time = timeit.default_timer()

avg_error = np.mean(errors)
std_error = np.std(errors)
max_error = np.max(errors)

print("\nPosition calculation : %.5f sec/img" % ((terminate_time - cal_time) / 50.0))
print("Avg_error : %.4f m" % avg_error)
print("Std_error : %.4f m" % std_error)
print("Max_error : %.4f m" % max_error)