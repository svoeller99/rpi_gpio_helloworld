#!/usr/bin/python3

"""Small program that reads from a keypad and displays the output on an LCD display."""

import threading
import time
from i2caddr import I2C_ADDR
from RPi import GPIO
from keypad import KeyPad
import LCD1602

read_from_keypad_stop_event = threading.Event()
LCD1602.init(I2C_ADDR, 1)

def output_to_lcd(output):
    """Output a string to the LCD display."""
    LCD1602.clear()
    LCD1602.write(0, 0, output)

def read_from_keypad(stop_event):
    """Continuously read key pad input and display the result on an LCD display."""
    key_pad = KeyPad(stop_event=stop_event)
    while True:
        if stop_event.is_set():
            break
        entered_sequence = key_pad.read()
        output_to_lcd(entered_sequence)

keypad_thread = threading.Thread(target=read_from_keypad, args=(read_from_keypad_stop_event,))

try:
    keypad_thread.start()
    while True:
        time.sleep(.1)

except KeyboardInterrupt:
    read_from_keypad_stop_event.set()
    keypad_thread.join()
    print('bye')

GPIO.cleanup()
