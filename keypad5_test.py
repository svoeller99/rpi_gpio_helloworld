#!/usr/bin/python3

import RPi.GPIO as GPIO
import threading
from keypad import KeyPad

def read_from_keypad():
    key_pad = KeyPad()

    while True:
        entered_sequence = key_pad.read()
        print(entered_sequence)

try:
    keypad_thread = threading.Thread(read_from_keypad)
    keypad_thread.start()
    keypad_thread.join()
        
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()
