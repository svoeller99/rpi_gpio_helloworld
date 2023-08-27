#!/usr/bin/python3

import RPi.GPIO as GPIO
import threading
import time
from keypad import KeyPad
import LCD1602

stop_event = threading.Event()
LCD1602.init(0x3f, 1)

def output_to_lcd(output):
    LCD1602.clear()
    LCD1602.write(0, 0, output)

def read_from_keypad(stop_event):
    key_pad = KeyPad(stop_event=stop_event)
    while True:
        if stop_event.is_set():
            break
        entered_sequence = key_pad.read()
        output_to_lcd(entered_sequence)

keypad_thread = threading.Thread(target=read_from_keypad, args=(stop_event,))

try:
    keypad_thread.start()
    while True:
        time.sleep(.1)
        
except KeyboardInterrupt:
    stop_event.set()
    keypad_thread.join()
    print('bye')

GPIO.cleanup()