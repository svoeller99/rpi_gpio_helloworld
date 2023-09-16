import RPi.GPIO as GPIO
import time
from servo_util import degrees_to_duty_cycle

tilt_pin = 13
pan_pin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(tilt_pin, GPIO.OUT)
GPIO.setup(pan_pin, GPIO.OUT)

tilt_pwm = GPIO.PWM(tilt_pin, 50) # 50 Hz (20 ms PWM period)
pan_pwm = GPIO.PWM(pan_pin, 50)

tilt_pwm.start(7.0) # set duty cycle to achieve 90 degrees (0 degrees is 2.0, 180 degrees is 13.0
pan_pwm.start(7.0)
time.sleep(.5)

for ii in range(0,3):
    tilt_pwm.ChangeDutyCycle(degrees_to_duty_cycle(30)) # 30 degrees
    time.sleep(1)
    tilt_pwm.ChangeDutyCycle(degrees_to_duty_cycle(120)) # 120 degrees
    time.sleep(1)
    tilt_pwm.ChangeDutyCycle(degrees_to_duty_cycle(90)) # 90 degrees
    time.sleep(1)

tilt_pwm.ChangeDutyCycle(0)
pan_pwm.ChangeDutyCycle(0)
tilt_pwm.stop()
pan_pwm.ChangeDutyCycle(0)
GPIO.cleanup()
