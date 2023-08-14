#!/usr/bin/python3

import ADC0834
import RPi.GPIO as GPIO
from math import log10
from time import sleep
from led import LED

# ADC0834 channels corresponding to RGB
RED_ADC_CHANNEL = 0
GREEN_ADC_CHANNEL = 1
BLUE_ADC_CHANNEL = 2

# BCM channel numbers for each RGB LED component
RED_LED_OUT_PIN = 13
GREEN_LED_OUT_PIN = 19
BLUE_LED_OUT_PIN = 26

FREQUENCY_HZ = 100
MAX_DUTY_CYCLE = 100
INCREMENT_COUNT = 255
# base for exponential calculation of duty cycle based on the desired number of increments
# supports a smoother / more linear visual brightness transition
INCREMENT_BASE = pow(10, log10(MAX_DUTY_CYCLE) / (INCREMENT_COUNT - 1))

leds = []

class ADCControlledLED:
    def __init__(self, name, adc_channel, led):
        self.name = name
        self.adc_channel = adc_channel
        self.led = led
    
    def sample(self):
        reading = ADC0834.getResult(self.adc_channel)
        reading ^= 255
        duty_cycle = self.calculate_duty_cycle(reading)
        print(self.name, reading, duty_cycle)
        led.set_duty_cycle(duty_cycle)

    def calculate_duty_cycle(self, reading):
        duty_cycle = pow(INCREMENT_BASE, reading)
        if duty_cycle > MAX_DUTY_CYCLE:
            duty_cycle = MAX_DUTY_CYCLE
        return duty_cycle

try:
    GPIO.setmode(GPIO.BCM)
    red_led = LED(RED_LED_OUT_PIN)
    green_led = LED(GREEN_LED_OUT_PIN)
    blue_led = LED(BLUE_LED_OUT_PIN)
    leds = [red_led, green_led, blue_led]

    ADC0834.setup()

    adc_controlled_leds = [
        ADCControlledLED('Red', RED_ADC_CHANNEL, red_led),
        ADCControlledLED('Green', GREEN_ADC_CHANNEL, green_led),
        ADCControlledLED('Blue', BLUE_ADC_CHANNEL, blue_led)
    ]

    while True:
        for adc_controlled_led in adc_controlled_leds: adc_controlled_led.sample()
        sleep(.2)

except KeyboardInterrupt:
    print('bye')

for led in leds: del led
GPIO.cleanup()