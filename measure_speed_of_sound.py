#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

TRIGGER_PIN = 23
ECHO_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_ping_travel_time_seconds():
    global TRIGGER_PIN, ECHO_PIN
    GPIO.output(TRIGGER_PIN, 0)
    time.sleep(2E-6) # sleep for 2 microseconds
    GPIO.output(TRIGGER_PIN, 1)
    time.sleep(10E-6) # sleep for 10 microseconds
    GPIO.output(TRIGGER_PIN, 0)
    while GPIO.input(ECHO_PIN) == 0:
        pass
    echo_start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pass
    echo_end_time = time.time()
    ping_travel_time_seconds = (echo_end_time - echo_start_time)
    return ping_travel_time_seconds

def calculate_speed_of_sound_feet_per_second(sound_travel_time_seconds_per_foot):
    return 1 / sound_travel_time_seconds_per_foot

try:
    while True:
        input("Place your test object 1 foot in front of the sensor and press <Enter>: ")
        ping_travel_time_seconds = measure_ping_travel_time_seconds()
        speed_of_sound_feet_per_second = calculate_speed_of_sound_feet_per_second(ping_travel_time_seconds / 2)
        print(f"Speed of sound (ft/s): {speed_of_sound_feet_per_second}")

except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()
