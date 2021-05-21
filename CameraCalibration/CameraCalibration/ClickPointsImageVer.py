import cv2

# Initalize world3d coordinate list
wpz0 = [[0.45, 1.35], [0, 1.35], [-0.45, 1.35], \
    [0.45, 1.8], [0, 1.8], [-0.45, 1.8], \
    [0.45, 2.25], [0, 2.25], [-0.45, 2.25], \
    [0.45, 2.7], [0, 2.7], [-0.45, 2.7]]

# Initalize image coordinate list
points = []
pointsNum = 1

# Define mouse call back function
def leftMouseDown(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global pointsNum
        points.append([x, y])
        print(str(pointsNum) + " Mouse : (" + str(x) + ", " + str(y) + ")")
        pointsNum += 1

fileName = "CT60P5"

# Get Image's pointer
image = cv2.imread("Image/" + fileName + ".png")

# Initialize video output window
cv2.namedWindow("calibration")
cv2.setMouseCallback("calibration", leftMouseDown)

# Viewing first image and select coordinates
cv2.imshow("calibration", image)
print("Points selection start")

while True:
    if cv2.waitKey() == ord('q'):
        print("Points selection done.")
        break

txtFile = open("Text/" + fileName + ".txt", 'w')

for idx, point in enumerate(points):
    cv2.circle(image, (point[0], point[1]), 1, (255, 0, 255), -1)
    writeLine = str(point[0]) + ", " + str(point[1]) + ", " + str(wpz0[idx][0]) + ", " + str(wpz0[idx][1]) + "\n"
    txtFile.write(writeLine)

txtFile.close()

cv2.imwrite("Image/Points" + fileName + ".png", image)