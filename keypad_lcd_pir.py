#!/usr/bin/python3

"""Small program that reads from a keypad and displays the output on an LCD display."""

import threading
import time
from RPi import GPIO
from keypad import KeyPad
from i2caddr import I2C_ADDR
import LCD1602

read_from_keypad_stop_event = threading.Event()
LCD1602.init(I2C_ADDR, 1)

is_armed = False
passcode = '1234'
command_string = ''

def output_to_lcd(line_one, line_two=None):
    """Output a string to the LCD display."""
    LCD1602.clear()
    LCD1602.write(0, 0, line_one)
    if line_two:
        LCD1602.write(0, 1, line_two)

def read_from_keypad(stop_event):
    """Continuously read key pad input and display the result on an LCD display."""
    global command_string
    key_pad = KeyPad(stop_event=stop_event)
    while True:
        if stop_event.is_set():
            break
        command_string = key_pad.read()

def show_brief_message(line_one, line_two=None):
    output_to_lcd(line_one, line_two)
    time.sleep(2)
    output_to_lcd('')

def handle_command():
    global passcode, is_armed, command_string
    if command_string == 'A'+passcode:
        is_armed = True
        output_to_lcd('Armed      ')
    elif command_string == 'B'+passcode:
        is_armed = False
        output_to_lcd('Disarmed   ')
    elif command_string == 'C'+passcode:
        output_to_lcd('New Passcode? ')
        while command_string == 'C'+passcode:
            pass
        passcode = command_string
        show_brief_message('New Passcode: ', passcode)
    else:
        show_brief_message('Unknown command')


keypad_thread = threading.Thread(target=read_from_keypad, args=(read_from_keypad_stop_event,))

try:
    keypad_thread.start()
    while True:
        handle_command()
        time.sleep(.1)

except KeyboardInterrupt:
    read_from_keypad_stop_event.set()
    keypad_thread.join()
    print('bye')

GPIO.cleanup()
