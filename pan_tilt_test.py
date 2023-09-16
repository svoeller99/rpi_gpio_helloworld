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

def gradually_change_duty_cycle(pwm, prior_degrees, new_degrees):
    increments = 10
    degrees_increment = abs(new_degrees - prior_degrees) / increments
    if new_degrees < prior_degrees:
        degrees_increment *= -1
    current_degrees = prior_degrees
    while current_degrees < new_degrees:
        current_degrees += degrees_increment
        pwm.ChangeDutyCycle(degrees_to_duty_cycle(current_degrees))
        time.sleep(.05)

for ii in range(0,3):
    gradually_change_duty_cycle(tilt_pwm, 90, 30)
    # tilt_pwm.ChangeDutyCycle(degrees_to_duty_cycle(30)) # 30 degrees
    time.sleep(1)
    # tilt_pwm.ChangeDutyCycle(degrees_to_duty_cycle(120)) # 120 degrees
    gradually_change_duty_cycle(tilt_pwm, 30, 120)
    time.sleep(1)
    # tilt_pwm.ChangeDutyCycle(degrees_to_duty_cycle(90)) # 90 degrees
    gradually_change_duty_cycle(tilt_pwm, 120, 90)
    time.sleep(1)

tilt_pwm.ChangeDutyCycle(0)
pan_pwm.ChangeDutyCycle(0)
tilt_pwm.stop()
pan_pwm.ChangeDutyCycle(0)
GPIO.cleanup()
