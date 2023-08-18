#!/usr/bin/python3

import ADC0834
import RPi.GPIO as GPIO
from time import sleep

# BCM pin numbers
PIR_PIN = 6
BUZZER_PIN = 26

LIGHT_MIN_THRESHOLD = 80
LOW_LIGHT_READINGS_THRESHOLD = 10
MOTION_DETECTION_THRESHOLD = 5

# state
consecutive_pir_readings = 0
consecutive_low_light_readings = 0

GPIO.setmode(GPIO.BCM)
ADC0834.setup()

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def evaluate_readings(photoresistor_reading, pir_reading):
    global consecutive_pir_readings, consecutive_low_light_readings

    if photoresistor_reading > LIGHT_MIN_THRESHOLD:
        consecutive_low_light_readings = 0
    else:
        consecutive_low_light_readings += 1

    if pir_reading == 0:
        consecutive_pir_readings = 0
    else:
        consecutive_pir_readings += 1
    
    print(consecutive_low_light_readings, ' - ', consecutive_pir_readings)

    if consecutive_low_light_readings >= LOW_LIGHT_READINGS_THRESHOLD and consecutive_pir_readings >= MOTION_DETECTION_THRESHOLD:
        print('TIME TO SOUND THE ALARM!')
        # TODO: turn buzzer on here
    else:
        # TODO: turn buzzer off here
        pass

try:
    while True:
        photoresistor_reading = ADC0834.getResult(0)
        pir_reading = GPIO.input(PIR_PIN)
        evaluate_readings(photoresistor_reading, pir_reading)
        sleep(.1)
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()