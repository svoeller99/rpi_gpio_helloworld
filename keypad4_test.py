#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from keypad import KeyPad

try:
    key_pad = KeyPad()

    while True:
        entered_sequence = key_pad.read()
        print(entered_sequence)
        sleep(.05)
        
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()
