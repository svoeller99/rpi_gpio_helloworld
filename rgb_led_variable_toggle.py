#!/usr/bin/python3

import RPi.GPIO as GPIO
from button import Button
from math import log10, pow
from time import sleep
from vpython import *

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
MAX_DUTY_CYCLE = 100
INCREMENT_COUNT = 8
# base for exponential calculation of duty cycle based on the desired number of increments
# supports a smoother / more linear visual brightness transition
INCREMENT_BASE = pow(10, log10(MAX_DUTY_CYCLE) / (INCREMENT_COUNT - 1))

class LED:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.current_increment_count = 0
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, FREQUENCY_HZ)
        self.pwm.start(0)
    
    def toggle(self):
        self.current_increment_count += 1
        if self.current_increment_count > INCREMENT_COUNT:
            self.current_increment_count = 0
        duty_cycle = self.calculate_duty_cycle()
        print(f'Setting LED "{self.name}" to {self.current_increment_count} increment. Duty cycle: {duty_cycle}')
        self.pwm.ChangeDutyCycle(duty_cycle)    

    def calculate_duty_cycle(self):
        global INCREMENT_BASE
        if self.current_increment_count == 0:
            return 0
        duty_cycle = pow(INCREMENT_BASE, self.current_increment_count)
        if duty_cycle > MAX_DUTY_CYCLE:
            duty_cycle = MAX_DUTY_CYCLE
        return duty_cycle

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

# init vpython objects
mySphere = sphere(color=color.white, radius=1, pos=vector(0, 2.5, 0))
myCylinder = cylinder(color=color.white, radius=1, length=2.5, axis=vector(0,1,0))
myBase = cylinder(color=color.white, radius=1.2, length=.25, axis=vector(0,1,0))
myLeg1 = box(pos=vector(-.75,-1,0), size=vector(.1,6,.1), color=vector(.2, .2, .2))
myLeg2 = box(pos=vector(-..5,-1,0), size=vector(.1,6,.1), color=vector(.2, .2, .2))
myLeg3 = box(pos=vector(-.25,-1,0), size=vector(.1,6,.1), color=vector(.2, .2, .2))
colored_vpython_objects = [mySphere, myCylinder, myBase]

try:
    while True:
        for button in buttons: button.read_state()
        for vpython_object in colored_vpython_objects:
            vpython_color_increment = 100 / INCREMENT_COUNT
            vpython_object.color = vector(
                red_led.current_increment_count * vpython_color_increment,
                green_led.current_increment_count * vpython_color_increment,
                blue_led.current_increment_count * vpython_color_increment
            )
        sleep(.1)
except KeyboardInterrupt:
    print('bye')

for led in leds: del led
GPIO.cleanup()