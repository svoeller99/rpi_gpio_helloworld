#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from math import log10, pow

# GPIO pin numbers
# pinout reference: https://toptechboy.com/understanding-raspberry-pi-4-gpio-pinouts/
DOWN_BUTTON_PIN = 33 # BCM 13
UP_BUTTON_PIN = 35 # BCM 19
LED_PIN = 37 # BCM 26

# Constants for button state
BUTTON_DOWN = 1
BUTTON_UP = 0

# Constants for PWM
FREQUENCY_HZ = 100
MAX_DUTY_CYCLE = 100
INCREMENT_COUNT = 8
# base for exponential calculation of duty cycle based on the desired number of increments
# supports a smoother / more linear visual brightness transition
INCREMENT_BASE = pow(10, log10(MAX_DUTY_CYCLE) / (INCREMENT_COUNT - 1))

# Mutable state
# number of LED brightness increments - power to apply to INCREMENT_BASE to get duty cycle
current_increment_count = 0

# Represents a pressable button with a function pointer to execute on press.
# NOTE: GPIO.add_event_detect looks like a better alternative to this and reading state in a loop, but we'll get to that later
class Button:
    def __init__(self, pin, on_press):
        self.pin = pin
        self.on_press = on_press
        self.last_read_state = BUTTON_UP
        
    def read_state(self):
        prior_state = self.last_read_state
        new_state = GPIO.input(self.pin)
        self.last_read_state = new_state
        if new_state == BUTTON_DOWN and prior_state == BUTTON_UP:
            self.on_press()

# initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(UP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm = GPIO.PWM(LED_PIN, FREQUENCY_HZ)

def dim_led():
    change_led(False)

def brighten_led():
    change_led(True)

def change_led(brighten):
    global current_increment_count
    if brighten:
        if current_increment_count < INCREMENT_COUNT - 1:
            current_increment_count += 1
            print('brightening LED')
    else:
        if current_increment_count > 0:
            current_increment_count -= 1
            print('dimming LED')
    current_duty_cycle = calculate_duty_cycle()
    pwm.ChangeDutyCycle(current_duty_cycle)

def calculate_duty_cycle():
    global current_increment_count, INCREMENT_BASE
    if current_increment_count == 0:
        return 0
    duty_cycle = pow(INCREMENT_BASE, current_increment_count)
    if duty_cycle > MAX_DUTY_CYCLE:
        duty_cycle = MAX_DUTY_CYCLE
    return duty_cycle

pwm.start(calculate_duty_cycle())

# create our buttons
dim_button = Button(DOWN_BUTTON_PIN, dim_led)
brighten_button = Button(UP_BUTTON_PIN, brighten_led)
buttons = [dim_button, brighten_button]

# Until keyboard interrupt occurs, read button states, allowing Button to trigger dim/brighten functions
try:
    while True:
        print(current_increment_count, calculate_duty_cycle())
        for button in buttons: 
            button.read_state()
        sleep(.1)

except KeyboardInterrupt:
    print('bye')

pwm.stop()
GPIO.cleanup()