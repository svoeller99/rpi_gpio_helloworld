#!/usr/bin/python3

import RPi.GPIO as GPIO
import threading
import time
from keypad import KeyPad

key_pad = KeyPad()
do_continue = True

def read_from_keypad():
    global key_pad
    while do_continue:
        try:
            entered_sequence = key_pad.read()
            print(entered_sequence)
        except Exception as e:
            print(e)
    GPIO.cleanup()

keypad_thread = threading.Thread(target=read_from_keypad)

try:
    keypad_thread.start()
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    do_continue = False
    keypad_thread.join()
    print('bye')