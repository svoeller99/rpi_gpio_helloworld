#!/usr/bin/python3

import ADC0834
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
ADC0834.setup()

try:
    while True:
        reading = ADC0834.getResult(0)
        if reading.is_valid():
            print(reading)
        sleep(.2)
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()