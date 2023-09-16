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
    increments = 100
    degrees_increment = abs(new_degrees - prior_degrees) / increments
    if new_degrees < prior_degrees:
        degrees_increment *= -1
    print(f"Changing from {prior_degrees} to {new_degrees} degrees. Increment: {degrees_increment}")
    current_degrees = prior_degrees
    while (degrees_increment > 0 and current_degrees < new_degrees) or (degrees_increment < 0 and current_degrees > new_degrees):
        current_degrees += degrees_increment
        pwm.ChangeDutyCycle(degrees_to_duty_cycle(current_degrees))
        time.sleep(.005)

for ii in range(0,2):
    gradually_change_duty_cycle(tilt_pwm, 90, 30)
    time.sleep(1)
    gradually_change_duty_cycle(tilt_pwm, 30, 120)
    time.sleep(1)
    gradually_change_duty_cycle(tilt_pwm, 120, 90)
    time.sleep(1)

for ii in range(0,2):
    gradually_change_duty_cycle(pan_pwm, 90, 30)
    time.sleep(1)
    gradually_change_duty_cycle(pan_pwm, 30, 120)
    time.sleep(1)
    gradually_change_duty_cycle(pan_pwm, 120, 90)
    time.sleep(1)

tilt_pwm.ChangeDutyCycle(0)
pan_pwm.ChangeDutyCycle(0)
tilt_pwm.stop()
pan_pwm.stop()
GPIO.cleanup()
