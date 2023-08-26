#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from keypad import KeyPad

try:
    key_pad = KeyPad()

    while True:
        key_pad.sample()
        sleep(.05)
        
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()
