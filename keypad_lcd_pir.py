#!/usr/bin/python3

"""Small program that reads from a keypad and displays the output on an LCD display."""

import threading
import time
from RPi import GPIO
from keypad import KeyPad
from i2caddr import I2C_ADDR
from typing import List
import LCD1602

# BCM pin numbers
PIR_PIN = 6
BUZZER_PIN = 26

# Constants
MOTION_DETECTION_THRESHOLD = 5
MIN_ALARM_TIME = 5 # seconds

# State
is_armed = False
passcode = '1234'
command_string = ''
prior_command_string = ''
consecutive_pir_readings = 0
alarm_start_time = 0

def output_to_lcd(line_one, line_two=None):
    """Output a string to the LCD display."""
    print(line_one, line_two)
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

def detect_motion(stop_event):
    global is_armed, consecutive_pir_readings
    while True:
        if stop_event.is_set():
            break
        pir_reading = GPIO.input(PIR_PIN)
        # print("pir_reading", pir_reading)
        if pir_reading == 0:
            consecutive_pir_readings = 0
        else:
            consecutive_pir_readings += 1
        time.sleep(.1)

def evaluate_alarm_threshold(stop_event):
    global consecutive_pir_readings, alarm_start_time, is_armed
    print(consecutive_pir_readings, alarm_start_time, is_armed)
    while True:
        if stop_event.is_set():
            break
        if not is_armed:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            return
        if consecutive_pir_readings >= MOTION_DETECTION_THRESHOLD:
            print('TIME TO SOUND THE ALARM!')
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            alarm_start_time = time.time()
        else:
            current_time = time.time()
            if current_time - alarm_start_time > MIN_ALARM_TIME:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(.1)

def show_brief_message(line_one, line_two=None):
    output_to_lcd(line_one, line_two)
    time.sleep(2)
    output_to_lcd('')

def handle_command():
    global passcode, is_armed, command_string, prior_command_string
    if command_string == prior_command_string:
        return
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
    elif command_string[0:1] in ['A', 'B', 'C']:
        show_brief_message('Bad Passcode', command_string)
    else:
        show_brief_message('Unknown command: ', command_string)
    prior_command_string = command_string

# initialize LCD display
LCD1602.init(I2C_ADDR, 1)

# initialize GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.HIGH)

# event to trigger thread stop
program_stop_event = threading.Event()

# list of async functions
async_functions = [
    read_from_keypad, 
    detect_motion, 
    evaluate_alarm_threshold
]

threads = list(map(lambda func: threading.Thread(target=func, args=(program_stop_event,), daemon=True), async_functions))

try:
    for thread in threads: thread.start()
    while True:
        handle_command()
        time.sleep(.1)

except KeyboardInterrupt:
    program_stop_event.set()
    for thread in threads: thread.join()
    print('bye')

GPIO.cleanup()
