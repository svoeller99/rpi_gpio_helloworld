#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from button import Button
from led import LED

# GPIO channels
# inputs
RED_BUTTON_CHANNEL = 33   # BCM 13
GREEN_BUTTON_CHANNEL = 35 # BCM 19
BLUE_BUTTON_CHANNEL = 37  # BCM 26
# outputs
RED_LED_CHANNEL = 36      # BCM 16
GREEN_LED_CHANNEL = 38    # BCM 20
BLUE_LED_CHANNEL = 40     # BCM 12

# init GPIO
GPIO.setmode(GPIO.BOARD)

# init RGB LED objects
red_led = LED('red', RED_LED_CHANNEL)
green_led = LED('green', GREEN_LED_CHANNEL)
blue_led = LED('blue', BLUE_LED_CHANNEL)
leds = [red_led, green_led, blue_led]

# init RGB buttons
red_button = Button(RED_BUTTON_CHANNEL, red_led.toggle)
green_button = Button(GREEN_BUTTON_CHANNEL, green_led.toggle)
blue_button = Button(BLUE_BUTTON_CHANNEL, blue_led.toggle)
buttons = [red_button, green_button, blue_button]

try:
    while True:
        for button in buttons: button.read_state()
        sleep(.1)
except KeyboardInterrupt:
    print('bye')

for led in leds: del led
GPIO.cleanup()