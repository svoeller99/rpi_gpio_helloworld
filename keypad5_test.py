#!/usr/bin/python3

import RPi.GPIO as GPIO
import threading
import time
from keypad import KeyPad

stop_event = threading.Event()

def read_from_keypad(stop_event):
    key_pad = KeyPad(stop_event=stop_event)
    while True:
        if stop_event.is_set():
            break
        entered_sequence = key_pad.read()
        print(entered_sequence)

keypad_thread = threading.Thread(target=read_from_keypad, args=(stop_event,))

try:
    keypad_thread.start()
    while True:
        time.sleep(.1)
        
except KeyboardInterrupt:
    print("Got keyboard interrupt")
    stop_event.set()
    keypad_thread.join()
    print('bye')

GPIO.cleanup()