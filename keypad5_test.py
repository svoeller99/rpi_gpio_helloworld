#!/usr/bin/python3

import RPi.GPIO as GPIO
import threading
import time
from keypad import KeyPad

key_pad = KeyPad()
stop_event = threading.Event()

def read_from_keypad():
    global key_pad, stop_event
    while not stop_event.is_set():
        entered_sequence = key_pad.read()
        print(entered_sequence)

keypad_thread = threading.Thread(target=read_from_keypad)

try:
    keypad_thread.start()
    while True:
        time.sleep(.1)
        
except KeyboardInterrupt:
    stop_event.set()
    keypad_thread.join()
    print('bye')

GPIO.cleanup()