from MotorModule import Motor
from LaneDetectionmodule import getLaneCurve
import WebcamModule
import KeyPressModule as kp
import cv2
import utlis

############################################
motor = Motor(2,3,4,11,10,9) #(EnA,In1A,In2A,EnB,In1B,In2B)

motorSpeed = 0.4 #MOTOR SPEED
sen = 1 #SENSITIVITY
maxTurn = 0.2 #MAX SPEED
leftCurveThres = 0.01
rightCurveThres = 0.01
display = 2
############################################


def keyPad():
    kp.init()
    if kp.getKey('UP'):
        motor.move(motorSpeed,0,0.1) #(Speed,turn,delay)
    elif kp.getKey('DOWN'):
        motor.move(-motorSpeed,0,0.1)
    elif kp.getKey('LEFT'):
        motor.move(motorSpeed,maxTurn,0.1)
    elif kp.getKey('RIGHT'):
        motor.move(motorSpeed,-maxTurn,0.1)
    elif kp.getKey('s'):
        motor.stop(0.1)

def camData():
    img = WebcamModule.getImg()
    curveVal = getLaneCurve(img,display)

    if curveVal > maxTurn : curveVal = maxTurn
    if curveVal < -maxTurn : curveVal = -maxTurn

    print("Curve =  ",curveVal)
    if curveVal>0:
        if curveVal < rightCurveThres : curveVal = 0
    else:
        if curveVal > -leftCurveThres : curveVal = 0

    motor.move(motorSpeed,curveVal*sen,0.05)

    if display != 0 : cv2.waitKey(1)

if __name__ == '__main__':
    while True:
        keyPad()
        initialTrackBarVals = [102,80,20,214]
        utlis.initializeTrackbars(initialTrackBarVals)
        camData()