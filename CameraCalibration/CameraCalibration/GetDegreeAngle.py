import numpy as np
import numpy.linalg as lin
import cv2
import math

rvecs = [\
    np.array([2.383203206, 0.091510871, -0.043129772]), \
    np.array([2.387725443, -0.010505886, 0.002210865]), \
    np.array([2.383606545, -0.146761152, 0.060684069]), \
    np.array([2.307255348, 0.051404371, -0.027038351]), \
    np.array([2.308811288, -0.046252689, 0.020158312]), \
    np.array([2.306926958, -0.145073966, 0.066738481]), \
    np.array([2.229198959, 0.048031054, -0.029226122]), \
    np.array([2.230152061, -0.047139151, 0.021829387]), \
    np.array([2.228964, -0.14168598, 0.07072243]), \
    np.array([2.150239375, 0.045094377, -0.031355367]), \
    np.array([2.152511324, -0.047143622, 0.022719531]), \
    np.array([2.15063323, -0.137504498, 0.074305988])]

StartXValueArray = [134, 134, 134, 129, 129, 129, 124, 124, 124, 0, 0, 0]
StartYValueArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
StartZValueArray = [-6, -1, 4, -6, -1, 4, -6, -1, 4, 0, 0, 0]


rodriguesR = []

for rv in rvecs:
    temp = np.zeros(shape = (3, 3))
    cv2.Rodrigues(rv, temp)
    rodriguesR.append(temp)

for idx, rdrgs in enumerate(rodriguesR):
    StartXValue = StartXValueArray[idx]
    EndXValue = StartXValue + 2
    StartYValue = StartYValueArray[idx]
    EndYValue = StartYValue + 2
    StartZValue = StartZValueArray[idx]
    EndZValue = StartZValue + 2

    nowDegreeX = StartXValueArray[idx] + 1
    nowDegreeY = StartYValueArray[idx] + 1
    nowDegreeZ = StartZValueArray[idx] + 1

    AxisType = 0
    DigitCount = 0

    plusValue = 0.1

    sumDiffArray = []

    whileStop = False

    while whileStop == False:
        sumDiffArray = []

        for i in range(21):
            # print("check " + str(StartXValue))
            if (AxisType == 0):
                nowDegreeX = StartXValue + plusValue * i
            elif (AxisType == 1):
                nowDegreeY = StartYValue + plusValue * i
            elif (AxisType == 2):
                nowDegreeZ = StartZValue + plusValue * i
    
            AxisX_RM = np.array([[1, 0, 0], \
                [0, math.cos(math.radians(nowDegreeX)), - math.sin(math.radians(nowDegreeX))], \
                [0, math.sin(math.radians(nowDegreeX)), math.cos(math.radians(nowDegreeX))]])
    
            AxisY_RM = np.array([[math.cos(math.radians(nowDegreeY)), 0, - math.sin(math.radians(nowDegreeY))], \
                [0, 1, 0], \
                [math.sin(math.radians(nowDegreeY)), 0, math.cos(math.radians(nowDegreeY))]])
    
            AxisZ_RM = np.array([[math.cos(math.radians(nowDegreeZ)), - math.sin(math.radians(nowDegreeZ)), 0], \
                [math.sin(math.radians(nowDegreeZ)), math.cos(math.radians(nowDegreeZ)), 0], \
                [0, 0, 1]])
    
            TRM = AxisX_RM @ AxisY_RM @ AxisZ_RM # Total rotation matrix

            sumDiff = abs(TRM[0][0] - rdrgs[0][0]) + \
                abs(TRM[0][1] - rdrgs[0][1]) + \
                abs(TRM[0][2] - rdrgs[0][2]) + \
                abs(TRM[1][0] - rdrgs[1][0]) + \
                abs(TRM[1][1] - rdrgs[1][1]) + \
                abs(TRM[1][2] - rdrgs[1][2]) + \
                abs(TRM[2][0] - rdrgs[2][0]) + \
                abs(TRM[2][1] - rdrgs[2][1]) + \
                abs(TRM[2][2] - rdrgs[2][2])

            sumDiffArray.append(sumDiff)

        minIndex = np.argmin(sumDiffArray)
    
        if (minIndex == 0):
            if (AxisType == 0):
                StartXValue = StartXValue - (plusValue * 10)
                EndXValue = EndXValue - (plusValue * 10)
            elif (AxisType == 1):
                StartYValue = StartYValue - (plusValue * 10)
                EndYValue = EndYValue - (plusValue * 10)
            elif (AxisType == 2):
                StartZValue = StartZValue - (plusValue * 10)
                EndZValue = EndZValue - (plusValue * 10)
        elif (minIndex == 20):
            if (AxisType == 0):
                StartXValue = StartXValue + (plusValue * 10)
                EndXValue = EndXValue + (plusValue * 10)
            elif (AxisType == 1):
                StartYValue = StartYValue + (plusValue * 10)
                EndYValue = EndYValue + (plusValue * 10)
            elif (AxisType == 2):
                StartZValue = StartZValue + (plusValue * 10)
                EndZValue = EndZValue + (plusValue * 10)
        else:
            if (AxisType == 0):
                nowDegreeX = StartXValue + minIndex * plusValue
                StartXValue = StartXValue + (minIndex - 1) * plusValue
                EndXValue = StartXValue + plusValue * 2
            elif (AxisType == 1):
                nowDegreeY = StartYValue + minIndex * plusValue
                StartYValue = StartYValue + (minIndex - 1) * plusValue
                EndYValue = StartYValue + plusValue * 2
            elif (AxisType == 2):
                nowDegreeZ = StartZValue + minIndex * plusValue
                StartZValue = StartZValue + (minIndex - 1) * plusValue
                EndZValue = StartZValue + plusValue * 2
                DigitCount += 1
                plusValue = plusValue / 10
                if (DigitCount == 6):
                    whileStop = True
                    # print("Sum Diff : %.10f" %min(sumDiffArray))
                    break
            AxisType += 1
            AxisType = AxisType % 3
        
    print(str(nowDegreeX))
    print(str(nowDegreeY))
    print(str(nowDegreeZ))