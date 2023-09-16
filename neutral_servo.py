import RPi.GPIO as GPIO
import time

servo_pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50) # 50 Hz (20 ms PWM period)

pwm.start(7.0) # set duty cycle to achieve 90 degrees (0 degrees is 2.0, 180 degrees is 13.0
time.sleep(.5)

for ii in range(0,3):
    pwm.ChangeDutyCycle(2.0) # 0 degrees
    time.sleep(1)
    pwm.ChangeDutyCycle(12.0) # 180 degrees
    time.sleep(1)
    pwm.ChangeDutyCycle(7.0) # 90 degrees
    time.sleep(1)

pwm.ChangeDutyCycle(0)
pwm.stop()
GPIO.cleanup()
