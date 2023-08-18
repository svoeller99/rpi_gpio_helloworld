#!/usr/bin/python3

# Build a programmable temperature alarm using the following components:
#     * Push button
#         * used to toggle between “program” mode and “monitor” mode
#     * LCD screen
#         * “Monitor” mode - display temp and alarm status
#         * “Program” mode - display “trigger” temp
#     * Potentiometer
#         * “Monitor” mode - does nothing
#         * “Program” mode - used to set the “trigger” temp
#     * Alarm
#         * “Monitor” mode - sound the alarm if the trigger temp is reached
#         * “Program” mode - does nothing

import RPi.GPIO as GPIO
import ADC0834
import LCD1602
import dht11
from button import Button
from time import sleep

# BCM PIN numbers for inputs
TEMP_SENSOR_PIN = 16
BUTTON_PIN = 6

# constants for outputs
LCD_ADDRESS = 0x3f # TODO: verify this via `i2cdetect -y 1`
LCD_BACKLIGHT_ON = 1
ADC_CHANNEL = 0
ADC_MAX_READING = 255

# constants for program/monitor modes
PROGRAM_MODE = 'program'
MONITOR_MODE = 'monitor'

# constants for min/max temperatures
MIN_TEMP_F = 32
MAX_TEMP_F = 100

# state
current_mode = PROGRAM_MODE
display_temp = ""
display_humidity = ""

def celcius_to_fahrenheit(celcius):
    return (celcius * 9/5) + 32

def handle_button_press():
    global current_mode
    if current_mode == PROGRAM_MODE:
        current_mode = MONITOR_MODE
    else:
        current_mode = PROGRAM_MODE
    print('button pressed - current mode: ', current_mode)

def map_adc_reading_to_temp(adc_reading):
    return adc_reading * (MAX_TEMP_F - MIN_TEMP_F) / ADC_MAX_READING + MIN_TEMP_F

GPIO.setmode(GPIO.BCM)

# setup button
mode_toggle_button = Button(BUTTON_PIN, handle_button_press)

# setup DHT
temp_hum_sensor = dht11.DHT11(pin = TEMP_SENSOR_PIN)

# setup ADC
ADC0834.setup()

# setup LCD
LCD1602.init(LCD_ADDRESS, LCD_BACKLIGHT_ON)

try:
    while True:
        mode_toggle_button.read_state()
        if current_mode == MONITOR_MODE:
            reading = temp_hum_sensor.read()
            if reading.is_valid():
                celcius = reading.temperature
                fahrenheit = celcius_to_fahrenheit(celcius)
                display_temp = f"Temp: {fahrenheit: .1f} F"
                display_humidity = f"Hum: {reading.humidity: .1f} %"
                # print(f"Temperature {fahrenheit: .2f} F. Humidity is {reading.humidity: .2f}%.")
        if current_mode == PROGRAM_MODE:
            reading = ADC0834.getResult(ADC_CHANNEL)
            reading ^= ADC_MAX_READING
            temp = map_adc_reading_to_temp(reading)
            print(reading, ' - ', temp)
        LCD1602.write(0, 0, display_temp)
        LCD1602.write(0, 1, display_humidity)
        sleep(.2)
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()