import numpy as np
import cv2

fileName = "Image/TileT60P0.png"
select_ImageNum = 0

R = np.zeros(shape = (3, 3))

 # [np.array([[ 2.39716243], [ 0.00643657], [-0.01549726]])

rvecs = [np.array([[2.68704701], [-0.04515365], [0.0685591]]), \
    np.array([[ 2.4023664 ], [ 0.00758432], [-0.01087085]]), \
    np.array([[ 2.4012871 ], [ 0.00502361], [-0.01511133]]), \
    np.array([[ 2.39871168], [ 0.00723819], [-0.01976027]]), \
    np.array([[ 2.40066348], [ 0.01007791], [-0.00933283]]), \
    np.array([[ 2.39910289], [ 0.00153764283], [-0.0131109416]]), \
    np.array([[ 2.40175499], [ 0.00619047], [-0.01815338]]), \
    np.array([[ 2.40075497], [ 0.00683308], [-0.01438562]]), \
    np.array([[ 2.40139077], [ 0.00578933], [-0.00637289]])]

# [np.array([[-0.0132861 ], [ 7.29122845], [ 1.76766496]])

tvecs = [np.array([[0.07508033], [6.57770835], [1.2092695]]), \
    np.array([[0.00164646187], [7.32519305], [1.85517072]]), \
    np.array([[-0.00884761], [ 7.31841537], [ 1.83583264]]), \
    np.array([[-0.03091849], [ 7.26637327], [ 1.84637852]]), \
    np.array([[-0.0391394 ], [ 7.31660051], [ 1.80983197]]), \
    np.array([[0.05171532], [7.27048698], [1.7975711 ]]), \
    np.array([[-0.0182006 ], [ 7.31582198], [ 1.84514239]]), \
    np.array([[-0.02383365], [ 7.33357091], [ 1.77518965]]), \
    np.array([[0.03339832], [7.29473913], [1.88299888]])]

cv2.Rodrigues(rvecs[select_ImageNum], R)
norm_camera_frame = np.zeros(shape = tvecs[select_ImageNum].shape).astype(np.float32)
# mtx = [[718.64434949, 0.0, 952.90698419], [0.0, 441.36653185, 487.34878521], [0.0, 0.0, 1.0]]
mtx = [[481.57110245, 0.0, 985.84778984], [0.0, 313.50328101, 614.51197833], [0.0, 0.0, 1.0]]

def leftMouseDown(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        target_pixel = [x, y]
        print("\nMouse X : " + str(x) + " Y : " + str(y))
        norm_camera_frame[0] = (target_pixel[0] - mtx[0][2]) / mtx[0][0]
        norm_camera_frame[1] = (target_pixel[1] - mtx[1][2]) / mtx[1][1]
        norm_camera_frame[2] = 1.0
        s = np.dot(R.T, tvecs[select_ImageNum])[2] / np.dot(R.T, norm_camera_frame)[2]
        result = np.dot(R.T, norm_camera_frame) * s - np.dot(R.T, tvecs[select_ImageNum])
        print(str(result[0]) + " " + str(result[1]) + " " + str(result[2]))

cv2.namedWindow("calibration")
cv2.setMouseCallback("calibration", leftMouseDown)

image1 = cv2.imread(fileName)
cv2.imshow("calibration", image1)

while True:
    if cv2.waitKey() == ord('q'):
        print("done.")
        break