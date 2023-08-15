#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

PWM_PIN = 18
FREQUENCY_HZ = 50
MIN_DUTY_CYCLE = 2
MAX_DUTY_CYCLE = 12

def calculate_duty_cycle(percent):
    return (percent/100 * (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE)) + MIN_DUTY_CYCLE

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)

pwm = GPIO.PWM(PWM_PIN, FREQUENCY_HZ)
pwm.start(0)

try:
    while True:
        pwm_percent = float(input('PWM % '))
        duty_cycle = calculate_duty_cycle(pwm_percent)
        print(duty_cycle)
        pwm.ChangeDutyCycle(duty_cycle)
        sleep(.1)
except KeyboardInterrupt:
    print('bye')

pwm.stop()
GPIO.cleanup()
