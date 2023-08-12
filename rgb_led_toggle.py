#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from button import Button

# GPIO channels
# inputs
RED_BUTTON_CHANNEL = 33   # BCM 13
GREEN_BUTTON_CHANNEL = 35 # BCM 19
BLUE_BUTTON_CHANNEL = 37  # BCM 26
# outputs
RED_LED_CHANNEL = 36      # BCM 16
GREEN_LED_CHANNEL = 38    # BCM 20
BLUE_LED_CHANNEL = 40     # BCM 12

# Constants for PWM
FREQUENCY_HZ = 100

class LED:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.current_state = False
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, FREQUENCY_HZ)
        self.pwm.start(0)
    
    def toggle(self):
        self.current_state = not self.current_state
        if self.current_state:
            self.pwm.ChangeDutyCycle(100)
        else:
            self.pwm.ChangeDutyCycle(0)
        print(f'Toggled LED "{self.name}" to {self.current_state}')    

    def __del__(self):
        self.pwm.stop()

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