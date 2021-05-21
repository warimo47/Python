import cv2

# 이미지 좌표 리스트 초기화
points = [] 

# mouse call back 함수 선언
def on_mouse(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		points.append([x,y])
		print((x,y), ' stored.')

# 영상의 포인터 획득
t65p_5 = cv2.VideoCapture('T65P_5.mp4')
t75p5 = cv2.VideoCapture('T75P5.mp4')

# 원하는 시간의 프레임 선택 
fps = t65p_5.get(cv2.CAP_PROP_FPS)
time = 50
t65p_5.set(1, time * fps)
ret1, image1 = t65p_5.read()

t75p5.set(1, time * fps)
ret2, image2 = t75p5.read()

# 영상 포인터 해제
t65p_5.release()
t75p5.release()

# 영상 출력 창 초기화
cv2.namedWindow('calibration')
cv2.setMouseCallback('calibration', on_mouse)

# 첫 번째 이미지 표시 및 관심 좌표 선택 (우하->좌측->상방)
cv2.imshow('calibration', image1)
print('1st calibration start')
while True:
	if cv2.waitKey() == ord('q'):
		print('point selection done')
		break
points_img1 = points.copy()
points = []
file = open('points_img1.txt', 'w')
for point in points_img1:
	cv2.circle(image1, (point[0], point[1]), 3, (0,0,255), -1)
	file.write(str(point)[1:len(str(point))-1]+'\n')
file.close()
cv2.imwrite('image1_result.png', image1)

# 두 번째 이미지 표시 및 관심 좌표 선택 (우하->좌측->상방)
cv2.imshow("calibration", image2)
print('2nd calibration start')
while True:
	if cv2.waitKey() == ord('q'):
		print('point selection done')
		break
points_img2 = points.copy()
points = []
file = open('points_img2.txt', 'w')
for point in points_img2:
	cv2.circle(image2, (point[0], point[1]), 3, (0,0,255), -1)
	file.write(str(point)[1:len(str(point))-1]+'\n')
file.close()
cv2.imwrite('image2_result.png', image2)