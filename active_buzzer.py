#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

BUZZER_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.HIGH)

try:
    while True:
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        sleep(0.1)
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        sleep(0.1)
except KeyboardInterrupt:
    print('bye')

GPIO.output(BUZZER_PIN, GPIO.HIGH)
GPIO.cleanup()