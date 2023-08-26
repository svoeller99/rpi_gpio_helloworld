#!/usr/bin/python3

import RPi.GPIO as GPIO
import threading
from keypad import KeyPad

key_pad = KeyPad()

def read_from_keypad():
    global key_pad
    while True:
        entered_sequence = key_pad.read()
        print(entered_sequence)

keypad_thread = threading.Thread(target=read_from_keypad)

try:
    keypad_thread.start()
    keypad_thread.join()
        
except KeyboardInterrupt:
    key_pad.stop()
    print('bye')

GPIO.cleanup()
