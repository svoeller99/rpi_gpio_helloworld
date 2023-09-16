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
time.sleep(.2)
tilt_pwm.ChangeDutyCycle(0) # set duty cycle to achieve 90 degrees (0 degrees is 2.0, 180 degrees is 13.0
pan_pwm.ChangeDutyCycle(0)
time.sleep(.5)

def change_degrees(pwm, prior_degrees, new_degrees):
    # suddenly_change_degrees(pwm, new_degrees)
    gradually_change_degrees(pwm, prior_degrees, new_degrees)

def gradually_change_degrees(pwm, prior_degrees, new_degrees):
    increments = 100
    degrees_increment = abs(new_degrees - prior_degrees) / increments
    if new_degrees < prior_degrees:
        degrees_increment *= -1
    print(f"Changing from {prior_degrees} to {new_degrees} degrees. Increment: {degrees_increment}")
    current_degrees = prior_degrees
    while (degrees_increment > 0 and current_degrees < new_degrees) or (degrees_increment < 0 and current_degrees > new_degrees):
        current_degrees += degrees_increment
        pwm.ChangeDutyCycle(degrees_to_duty_cycle(current_degrees))
        time.sleep(0.01)
    pwm.ChangeDutyCycle(0)
    time.sleep(.2)

def suddenly_change_degrees(pwm, new_degrees):
    pwm.ChangeDutyCycle(degrees_to_duty_cycle(new_degrees))
    time.sleep(0.2)
    pwm.ChangeDutyCycle(0)

def test_pan(pan_pwm, change_degrees):
    for ii in range(0,2):
        change_degrees(pan_pwm, 90, 30) #left
        time.sleep(1)
        change_degrees(pan_pwm, 30, 120) #right
        time.sleep(1)
        change_degrees(pan_pwm, 120, 90) #center
        time.sleep(1)

def test_tilt(tilt_pwm, change_degrees):
    for ii in range(0,2):
        change_degrees(tilt_pwm, 90, 30) #up 
        time.sleep(1)
        change_degrees(tilt_pwm, 30, 120) #down
        time.sleep(1)
        change_degrees(tilt_pwm, 120, 90) #center
        time.sleep(1)

test_tilt(tilt_pwm, change_degrees)

test_pan(pan_pwm, change_degrees)

tilt_pwm.ChangeDutyCycle(0)
pan_pwm.ChangeDutyCycle(0)
tilt_pwm.stop()
pan_pwm.stop()
GPIO.cleanup()
