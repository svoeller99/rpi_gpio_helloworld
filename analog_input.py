#!/usr/bin/python3

import ADC0834
import RPi.GPIO as GPIO
from math import log10
from time import sleep

ADC_CHANNEL = 0
LED_OUT_PIN = 26
FREQUENCY_HZ = 100
MAX_DUTY_CYCLE = 100
INCREMENT_COUNT = 255
# base for exponential calculation of duty cycle based on the desired number of increments
# supports a smoother / more linear visual brightness transition
INCREMENT_BASE = pow(10, log10(MAX_DUTY_CYCLE) / (INCREMENT_COUNT - 1))

def calculate_duty_cycle(reading):
    duty_cycle = pow(INCREMENT_BASE, reading)
    if duty_cycle > MAX_DUTY_CYCLE:
        duty_cycle = MAX_DUTY_CYCLE
    return duty_cycle

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_OUT_PIN, GPIO.OUT)
    led_pwm = GPIO.PWM(LED_OUT_PIN, FREQUENCY_HZ)
    led_pwm.start(0)

    ADC0834.setup()

    while True:
        reading = ADC0834.getResult(ADC_CHANNEL)
        reading ^= 255
        duty_cycle = calculate_duty_cycle(reading) #int((reading / 255) * 100)
        print(reading, duty_cycle)
        led_pwm.ChangeDutyCycle(duty_cycle)
        sleep(.2)

except KeyboardInterrupt:
    print('bye')

led_pwm.stop()
GPIO.cleanup()