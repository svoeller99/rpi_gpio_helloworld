#!/usr/bin/python3

import ADC0834
import RPi.GPIO as GPIO
from time import sleep

SERVO_PIN = 18

ADC_CHANNEL = 0

# PWM period in hertz
FREQUENCY_HZ = 50
# PWM period in milliseconds (ms)
PERIOD_MILLIS = 1 / FREQUENCY_HZ * 1000
# PWM period in microseconds (us)
PERIOD_MICROS = PERIOD_MILLIS * 1000

# Min/max pulse microseconds to get the servo to rotate from 0 to 180 degrees
# These values are taken from sunfounder's website, though the data sheet suggests
# a smaller range (1ms-2ms, or 1000us - 2000us).
# See also http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf.
SERVO_MIN_PULSE_MICROS = 500  # 0 degrees
SERVO_MAX_PULSE_MICROS = 2400 # 180 degrees - originally 2500 on sunfounder's website

# Min/max readings from ADC chip
POTENTIOMETER_MIN = 0
POTENTIOMETER_MAX = 255

# Pretty obvious :)
PERCENT_MIN = 0
PERCENT_MAX = 100

def calculate_duty_cycle_for_potentiometer_reading(raw_reading):
    """Given a percentage, convert to duty cycle needed to get the servo to rotate accordingly."""

    potentiometer_reading = max(POTENTIOMETER_MIN, min(POTENTIOMETER_MAX, raw_reading))
    pulse_width = map_potentiometer_reading_to_servo_pulse_width_micros(potentiometer_reading)
    duty_cycle = map_pulse_width_micros_to_duty_cycle_percentage(pulse_width)
    print(f"potentiometer_reading: {potentiometer_reading}, pulse_width={pulse_width}, duty_cycle={duty_cycle}")
    return duty_cycle

def map_potentiometer_reading_to_servo_pulse_width_micros(potentiometer_reading):
    """Convert a percentage to corresponding pulse width microseconds."""

    return (SERVO_MAX_PULSE_MICROS - SERVO_MIN_PULSE_MICROS) * (potentiometer_reading - POTENTIOMETER_MIN) / (POTENTIOMETER_MAX - POTENTIOMETER_MIN) + SERVO_MIN_PULSE_MICROS

def map_pulse_width_micros_to_duty_cycle_percentage(pulse_width_micros):
    """Convert from pulse width microseconds to a duty cycle percentage."""

    return (PERCENT_MAX - PERCENT_MIN) * pulse_width_micros / PERIOD_MICROS + PERCENT_MIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.output(SERVO_PIN, GPIO.LOW)

pwm = GPIO.PWM(SERVO_PIN, FREQUENCY_HZ)
pwm.start(0)

try:
    ADC0834.setup()

    while True:
        potentiometer_reading = ADC0834.getResult(ADC_CHANNEL)
        duty_cycle = calculate_duty_cycle_for_potentiometer_reading(potentiometer_reading)
        pwm.ChangeDutyCycle(duty_cycle)
        sleep(.2)
except KeyboardInterrupt:
    print('bye')

pwm.stop()
GPIO.cleanup()
