import cv2
import numpy as np
import utlis

curveList = []
avgVal = 10

def getLaneCurve(img, display=2):

    imgCopy = img.copy()
    imgResult = img.copy()

    #### Step 1
    imgThres = utlis.thresholding(img)

    #### Step 2
    hT, wT, c = img.shape
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = utlis.drawPoints(imgCopy, points)

    #### Step 3
    middlePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHist = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint

    #### Step 4
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))

    #### Step 5
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)

    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Result', imgResult)

    #### NORMALIZATION
    curve = curve / 100
    if curve > 1: curve == 1
    if curve < -1: curve == -1

    return curve

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)  # Access the webcam
    initialTrackBarVals = [102, 80, 20, 214]
    utlis.initializeTrackbars(initialTrackBarVals)
    frameCounter = 0
    while True:
        frameCounter += 1
        success, img = cap.read()
        if not success:
            break
        img = cv2.resize(img, (480, 240))
        curve = getLaneCurve(img, display=2)
        print(curve)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()