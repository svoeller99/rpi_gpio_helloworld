#!/usr/bin/python3

from i2caddr import I2C_ADDR
import RPi.GPIO as GPIO
import LCD1602
import dht11
import smbus2 # NOTE: not referenced, here, but used by LCD1602, internally
from button import Button

def celcius_to_fahrenheit(celcius):
    return (celcius * 9/5) + 32

DHT_PIN = 17
BUTTON_PIN = 16

# first arg - address that can be obtained by running `i2cdetect -y 1`
# second arg - whether or not to backlight the LCD (1=true, 0=false)
LCD1602.init(I2C_ADDR, 1)

GPIO.setmode(GPIO.BCM)
dht = dht11.DHT11(pin = DHT_PIN)

is_celcius = True
display_temp = ""
display_humidity = ""

def toggle_temp():
    global is_celcius
    is_celcius = not is_celcius

temp_toggle_button = Button(BUTTON_PIN, toggle_temp)

try:
    while True:
        temp_toggle_button.read_state()
        dht_reading = dht.read()
        if dht_reading.is_valid():
            celcius = dht_reading.temperature
            if is_celcius:
                display_temp = f"Temp: {celcius: .1f} C"
            else:
                fahrenheit = celcius_to_fahrenheit(celcius)
                display_temp = f"Temp: {fahrenheit: .1f} F"
            display_humidity = f"Hum: {dht_reading.humidity: .1f} %"
        # first two args are X and Y coordinates to write to (start is top-left)
        LCD1602.write(0, 0, display_temp)
        LCD1602.write(0, 1, display_humidity)
except KeyboardInterrupt:
    print('bye')

LCD1602.clear()
