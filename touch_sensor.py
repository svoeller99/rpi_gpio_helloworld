#!/usr/bin/python3

import time
from RPi import GPIO

TOUCH_SENSOR_PIN = 17
LED_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_SENSOR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

last_reading = 0
led_on = False

try:
    while True:
        reading = GPIO.input(TOUCH_SENSOR_PIN)
        if reading != last_reading:
            last_reading = reading
            if reading:
                led_on = not led_on
                GPIO.output(LED_PIN, led_on)
        time.sleep(.1)
except KeyboardInterrupt:
    print('bye')
GPIO.cleanup()
