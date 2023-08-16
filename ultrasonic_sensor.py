#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

TRIGGER_PIN = 23
ECHO_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

SPEED_OF_SOUND_FEET_PER_SECOND = 1125
SPEED_OF_SOUND_INCHES_PER_MICROSECOND = SPEED_OF_SOUND_FEET_PER_SECOND * 12 / 1E6 # 0.0135

def calculate_distance_in_inches(ping_travel_time_microseconds):
    ping_travel_distance_inches = SPEED_OF_SOUND_INCHES_PER_MICROSECOND * ping_travel_time_microseconds
    return ping_travel_distance_inches / 2

try:
    while True:
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
        ping_travel_time_microseconds = (echo_end_time - echo_start_time) * 1E6
        distance_in_inches = calculate_distance_in_inches(ping_travel_time_microseconds)
        print(f"Ping travel time (us): {int(ping_travel_time_microseconds)}.")
        print(f"Object distance (in): {distance_in_inches}.")
        print()
        time.sleep(.5)
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()
