import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(EnaA,GPIO.OUT)
        GPIO.setup(In1A,GPIO.OUT)
        GPIO.setup(In2A,GPIO.OUT)
        GPIO.setup(EnaB,GPIO.OUT)
        GPIO.setup(In1B,GPIO.OUT)
        GPIO.setup(In2B,GPIO.OUT)
        self.pwmA = GPIO.PWM(EnaA, 100);
        self.pwmA.start(0);
        self.pwmB = GPIO.PWM(EnaB, 100);
        self.pwmB.start(0);

    def move(self,speed=0.6,turn=0,t=0):
        speed *= 100
        turn *= 100

        leftSpeed = speed + turn
        rightSpeed = speed - turn

        if leftSpeed > 100 : leftSpeed = 100
        elif leftSpeed < -100 : leftSpeed = -100
        if rightSpeed > 100 : rightSpeed = 100
        elif rightSpeed < -100 : rightSpeed = -100

        print("Turn =",turn)
        print("Left speed = ",abs(leftSpeed))
        print("Right speed = ",abs(rightSpeed))
        self.pwmA.ChangeDutyCycle(abs(leftSpeed));
        self.pwmB.ChangeDutyCycle(abs(rightSpeed));

        if leftSpeed > 0:
            GPIO.output(self.In1A,GPIO.HIGH)
            GPIO.output(self.In2A,GPIO.LOW)
        elif leftSpeed < 0:
            GPIO.output(self.In1A,GPIO.LOW)
            GPIO.output(self.In2A,GPIO.HIGH)

        if rightSpeed > 0:
            GPIO.output(self.In1B,GPIO.HIGH)
            GPIO.output(self.In2B,GPIO.LOW)
        elif rightSpeed < 0:
            GPIO.output(self.In1B,GPIO.LOW)
            GPIO.output(self.In2B,GPIO.HIGH)

        sleep(t)
    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        sleep(t)
        GPIO.cleanup()

def main():
    motor.move(0.6,2)
    motor.stop(20)

if __name__ == '__main__':
    motor = Motor(26,5,6,17,22,27)
    main()