#!/usr/bin/python3

import RPi.GPIO as GPIO
import threading
from keypad import KeyPad

key_pad = KeyPad()

def read_from_keypad():
    global key_pad
    while True:
        try:
            entered_sequence = key_pad.read()
            print(entered_sequence)
        except Exception as e:
            GPIO.cleanup()
            raise e

keypad_thread = threading.Thread(target=read_from_keypad)

try:
    keypad_thread.start()
    keypad_thread.join()
        
except KeyboardInterrupt:
    print('bye')