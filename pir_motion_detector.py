#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

MOTION_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_PIN, GPIO.IN)

sleep(10)

print('Ready to detect motion')
try:
    while True:
        motion = GPIO.input(MOTION_PIN)
        print(motion)
        sleep(.1)
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()