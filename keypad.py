#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

ROW_PINS = [18,23,24,25]
COL_PINS = [10,22,27,17]

GPIO.setmode(GPIO.BCM)
for pin in ROW_PINS: GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
for pin in COL_PINS: GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        # cycle through row pins and turn each on, followed by reading each column pin in a nested loop to detect what keys are pressed
        for row_idx, row_pin in enumerate(ROW_PINS):
            GPIO.output(row_pin, GPIO.HIGH)
            for col_idx, col_pin in enumerate(COL_PINS):
                if GPIO.input(col_pin) == 1:
                    print(f"row {row_idx} col {col_idx}")
            GPIO.output(row_pin, GPIO.LOW)
        sleep(.5)
        
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()