#!/usr/bin/python3

import RPi.GPIO as GPIO
import dht11
import time

GPIO.setmode(GPIO.BCM)

DHT_PIN = 17
dht = dht11.DHT11(pin = DHT_PIN)

try:
    reading = dht.read()
    if reading.is_valid():
        print(f"Temperature is: {reading.temperature}. Humidity is {reading.humidity}.")
    time.sleep(.2)
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()
