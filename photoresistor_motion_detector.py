#!/usr/bin/python3

import ADC0834
import RPi.GPIO as GPIO
import time

# BCM pin numbers
PIR_PIN = 6
BUZZER_PIN = 26

LIGHT_MIN_THRESHOLD = 80
LOW_LIGHT_READINGS_THRESHOLD = 10
MOTION_DETECTION_THRESHOLD = 5
MIN_ALARM_TIME = 5 # seconds

# state
consecutive_pir_readings = 0
consecutive_low_light_readings = 0
alarm_start_time = 0

GPIO.setmode(GPIO.BCM)
ADC0834.setup()

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.HIGH)

def evaluate_readings(photoresistor_reading, pir_reading):
    global consecutive_pir_readings, consecutive_low_light_readings, alarm_start_time

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
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        alarm_start_time = time.time()
    else:
        current_time = time.time()
        if current_time - alarm_start_time > MIN_ALARM_TIME:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)

try:
    while True:
        photoresistor_reading = ADC0834.getResult(0)
        pir_reading = GPIO.input(PIR_PIN)
        evaluate_readings(photoresistor_reading, pir_reading)
        time.sleep(.1)
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()
