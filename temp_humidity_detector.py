#!/usr/bin/python3

import RPi.GPIO as GPIO
import dht11
import time

def celcius_to_fahrenheit(celcius):
    return (celcius * 9/5) + 32

GPIO.setmode(GPIO.BCM)

DHT_PIN = 17
dht = dht11.DHT11(pin = DHT_PIN)

try:
    while True:
        reading = dht.read()
        if reading.is_valid():
            celcius = reading.temperature
            fahrenheit = celcius_to_fahrenheit(celcius)
            print(f"Temperature (celcius) is: {celcius}. Temperature (fahrenheit) is {fahrenheit}. Humidity is {reading.humidity}.")
        time.sleep(.2)
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()
