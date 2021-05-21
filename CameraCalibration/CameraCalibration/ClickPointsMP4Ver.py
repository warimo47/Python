import cv2

# Initalize image coordinate list
points = []

fileName = "T70P0"
imageCaptureTime = 73

# Define mouse call back function
def leftMouseDown(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        print("Mouse : ",(x, y))

# Get video's pointer
videoFile = cv2.VideoCapture("Video/" + fileName + ".mp4")

videoFPS = videoFile.get(cv2.CAP_PROP_FPS)
videoFile.set(1, imageCaptureTime * videoFPS)
ret1, captureImage = videoFile.read()

# Release video's pointer
videoFile.release()

cv2.imwrite("Image/" + fileName + ".png", captureImage)

# Initialize video output window
cv2.namedWindow("calibration")
cv2.setMouseCallback("calibration", leftMouseDown)

# Viewing first image and select coordinates
cv2.imshow("calibration", captureImage)
print("Points selection start")

while True:
    if cv2.waitKey() == ord('q'):
        print("Points selection done.")
        break

txtFile = open("Text/" + fileName + ".txt", 'w')

for point in points:
    cv2.circle(captureImage, (point[0], point[1]), 3, (0, 0, 255), -1)
    txtFile.write(str(point)[1:len(str(point)) - 1] + "\n")

txtFile.close()

cv2.imwrite("Image/Points" + fileName + ".png", captureImage)