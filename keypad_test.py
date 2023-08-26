#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

ROW_PINS = [18,23,24,25]
COL_PINS = [10,22,27,17]

BUTTONS = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

GPIO.setmode(GPIO.BCM)
for pin in ROW_PINS: GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
for pin in COL_PINS: GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    last_buttons_pressed = []

    while True:
        # cycle through row pins and turn each on, followed by reading each column pin in a nested loop to detect what keys are pressed
        buttons_pressed = []
        for row_idx, row_pin in enumerate(ROW_PINS):
            GPIO.output(row_pin, GPIO.HIGH)
            for col_idx, col_pin in enumerate(COL_PINS):
                if GPIO.input(col_pin) == GPIO.HIGH:
                    buttons_pressed.append(BUTTONS[row_idx][col_idx])
            GPIO.output(row_pin, GPIO.LOW)
        if buttons_pressed != last_buttons_pressed:
            if buttons_pressed:
                print(buttons_pressed)
            last_buttons_pressed = buttons_pressed
        sleep(.2)
        
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()