#!/usr/bin/python3

from RPi import GPIO
import time

ledPins = [11, 12, 13, 15, 16, 18, 22, 3, 5, 24]

GPIO.setmode(GPIO.BOARD)
for i in ledPins:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.LOW)

GPIO.cleanup()