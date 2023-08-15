#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

PWM_PIN = 18
FREQUENCY_HZ = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)

pwm = GPIO.PWM(PWM_PIN, FREQUENCY_HZ)
pwm.start(0)

try:
    pwm_percent = float(input('PWM % '))
    pwm.ChangeDutyCycle(pwm_percent)
    sleep(.1)
except KeyboardInterrupt:
    print('bye')

pwm.stop()
GPIO.cleanup()