#!/usr/bin/python3

import RPi.GPIO as GPIO
import threading
import time
from keypad import KeyPad

key_pad = KeyPad()
do_continue = True

def read_from_keypad():
    global key_pad, do_continue
    while do_continue:
        entered_sequence = key_pad.read()
        print(entered_sequence)

keypad_thread = threading.Thread(target=read_from_keypad)

try:
    keypad_thread.start()
    while True:
        time.sleep(.1)
        
except KeyboardInterrupt:
    do_continue = False
    keypad_thread.join()
    print('bye')

GPIO.cleanup()