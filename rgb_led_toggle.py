#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

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

# TODO: factor out for reuse
# Constants for button state
BUTTON_DOWN = 1
BUTTON_UP = 0

# TODO: factor out for reuse
# Represents a pressable button with a function pointer to execute on press.
# NOTE: GPIO.add_event_detect looks like a better alternative to this and reading state in a loop, but we'll get to that later
class Button:
    def __init__(self, pin, on_press):
        self.pin = pin
        self.on_press = on_press
        self.last_read_state = BUTTON_UP
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    def read_state(self):
        prior_state = self.last_read_state
        new_state = GPIO.input(self.pin)
        self.last_read_state = new_state
        if new_state == BUTTON_DOWN and prior_state == BUTTON_UP:
            self.on_press()

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