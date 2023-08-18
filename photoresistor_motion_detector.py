#!/usr/bin/python3

import ADC0834
import RPi.GPIO as GPIO
from time import sleep

# BCM pin numbers
PIR_PIN = 6
BUZZER_PIN = 26

LIGHT_MIN_THRESHOLD = 80

GPIO.setmode(GPIO.BCM)
ADC0834.setup()

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.HIGH)

def evaluate_readings(photoresistor_reading, pir_reading):
    print(photoresistor_reading, ' - ', pir_reading)
    # TODO: logic to trip buzzer, here

try:
    while True:
        photoresistor_reading = ADC0834.getResult(0)
        pir_reading = GPIO.input(PIR_PIN)
        evaluate_readings(photoresistor_reading, pir_reading)
        sleep(.1)
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()
