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
import dht11

# BCM PIN numbers for inputs
TEMP_SENSOR_PIN = 17
BUTTON_PIN = 6

# constants for outputs
LCD_ADDRESS = 0x3f # TODO: verify this via `i2cdetect -y 1`
ADC_CHANNEL = 0

GPIO.setmode(GPIO.BCM)

# setup button
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    pass
except KeyboardInterrupt:
    print('bye')

GPIO.cleanup()