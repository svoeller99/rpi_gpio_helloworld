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
BUTTON_PIN = 5

# constants for outputs
LCD_ADDRESS = 0x3f # TODO: verify this via `i2cdetect -y 1`
LCD_BACKLIGHT_ON = 1
LCD_WIDTH = 16 # LCD width is 16 characters
ADC_CHANNEL = 0
ADC_MAX_READING = 255
BUZZER_PIN = 6

# constants for program/monitor modes
PROGRAM_MODE = 'program'
MONITOR_MODE = 'monitor'

# constants for min/max temperatures
MIN_TEMP_F = 32
MAX_TEMP_F = 100

# state
current_mode = PROGRAM_MODE
lcd_line_one = ""
lcd_line_two = ""
in_alarm = False
trigger_temp = MAX_TEMP_F

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

# setup buzzer
# GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    while True:
        mode_toggle_button.read_state()
        if current_mode == MONITOR_MODE:
            reading = temp_hum_sensor.read()
            if reading.is_valid():
                celcius = reading.temperature
                fahrenheit = celcius_to_fahrenheit(celcius)
                lcd_line_one = f"Temp: {fahrenheit: .1f} F"
                if fahrenheit > trigger_temp:
                    in_alarm = True
                    lcd_line_two = "IN ALARM"
                else:
                    in_alarm = False
                    lcd_line_two = ""
        if current_mode == PROGRAM_MODE:
            in_alarm = False
            reading = ADC0834.getResult(ADC_CHANNEL)
            reading ^= ADC_MAX_READING
            trigger_temp = map_adc_reading_to_temp(reading)
            lcd_line_one = f"Set Trigger Temp:"
            lcd_line_two = f"{trigger_temp: .1f} F"
        if in_alarm:
            pass
            # GPIO.output(BUZZER_PIN, GPIO.LOW)
        LCD1602.write(0, 0, lcd_line_one.ljust(LCD_WIDTH, ' '))
        LCD1602.write(0, 1, lcd_line_two.ljust(LCD_WIDTH, ' '))
        sleep(.1)
except KeyboardInterrupt:
    print('bye')

LCD1602.clear()
GPIO.cleanup()
