import cv2
import numpy as np
import timeit

start_time = timeit.default_timer() # 시작 시간 체크

'''
Calibration을 수행
1) world 좌표 기준 참값 리스트를 작성
2) 이와 1:1 매칭되는 calibration에 사용할 image 좌표들을 파일로부터 로드
'''

# 2D 좌표 참값 리스트 작성
points_world3d = []
for i in range(4,-5,-2):
	for j in range(10,20,2):
		points_world3d.append([i,j,0])

# file에서 image pixel 좌표들 불러오기 (2가지 이상의 서로 다른 구도를 사용해야 한다.)
points_img1 = []
with open('points_img1_.txt') as data:
	for line in data.readlines():
		x = int(line.split(',')[0])
		y = int(line.split(',')[1])
		points_img1.append([[x,y]])

points_img2 = []
with open('points_img2_.txt') as data:
	for line in data.readlines():
		x = int(line.split(',')[0])
		y = int(line.split(',')[1])
		points_img2.append([[x,y]])

obj_points = [np.array(points_world3d).astype(np.float32), np.array(points_world3d).astype(np.float32)]
img_points = [np.array(points_img1).astype(np.float32), np.array(points_img2).astype(np.float32)]

# 단순히 이미지 사이즈를 얻기 위한 작업으로 이미지의 내용과는 관련이 없음
img1 = cv2.imread('image1_result.png')
gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

cal_time = timeit.default_timer() # 종료 시간 체크  

print("calibration: %.4f초 소요." % (cal_time - start_time))

'''
물체 위치 추정 시작
'''

## 임시로 calibration에 사용한 지점 중 하나를 선택해 테스트한다.
errors = []
for image_num in range(0,1):
	for point_num in range(0,25):

		target_pixel = img_points[image_num][point_num][0]

		u = target_pixel[0]
		v = target_pixel[1]

		fx = mtx[0][0]
		fy = mtx[1][1]
		cx = mtx[0][2]
		cy = mtx[1][2]

		R = np.zeros(shape=(3,3))
		cv2.Rodrigues(rvecs[image_num], R)

		t = tvecs[image_num]

		norm_camera_frame = np.zeros(shape=t.shape).astype(np.float32)
		norm_camera_frame[0] = (u-cx)/fx
		norm_camera_frame[1] = (v-cy)/fy
		norm_camera_frame[2] = 1.0

		# z = 0을 가정한 산식 (single RGB로는 z = constant인 경우만 계산 가능)
		# 즉 물체가 ground level이 아닌 구덩이나 다른 물체 위에 있는 경우 정확하지 않을 수 있음
		s = np.dot(R.T, t)[2] / np.dot(R.T, norm_camera_frame)[2]

		result = np.dot(R.T, norm_camera_frame) * s - np.dot(R.T, t)

		#print('결과: ', result.T[0])
		#print('참값: ', obj_points[image_num][point_num])

		error = np.linalg.norm(result.T[0]-obj_points[image_num][point_num])
		errors.append(error)

terminate_time = timeit.default_timer() # 종료 시간 체크  

avg_error = np.mean(errors)
std_error = np.std(errors)
max_error = np.max(errors)

print("position calculation: %.5f초/img 소요." % ((terminate_time - cal_time)/50.0))
print("Avg_error: %.4f m" % avg_error)
print("Std_error: %.4f m" % std_error)
print("Max_error: %.4f m" % max_error)
#print(np.where(errors==max_error))