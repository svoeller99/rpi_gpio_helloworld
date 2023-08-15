#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

PWM_PIN = 18

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

# This servo rotates from 0 to 180 degrees.
ANGLE_MIN_DEGREES = 0
ANGLE_MAX_DEGREES = 180

# Pretty obvious :)
PERCENT_MIN = 0
PERCENT_MAX = 100

def calculate_duty_cycle_for_angle(raw_angle):
    """Given an angle, convert to duty cycle needed to get the servo to rotate accordingly."""

    angle = max(ANGLE_MIN_DEGREES, min(ANGLE_MAX_DEGREES, raw_angle))
    pulse_width = map_angle_to_servo_pulse_width_micros(angle)
    duty_cycle = map_pulse_width_micros_to_duty_cycle_percentage(pulse_width)
    print(f"Angle: {angle}, pulse_width={pulse_width}, duty_cycle={duty_cycle}")
    return duty_cycle

def calculate_duty_cycle_for_percentage(raw_percent):
    """Given a percentage, convert to duty cycle needed to get the servo to rotate accordingly."""

    percentage = max(PERCENT_MIN, min(PERCENT_MAX, raw_percent))
    pulse_width = map_percentage_to_servo_pulse_width_micros(percentage)
    duty_cycle = map_pulse_width_micros_to_duty_cycle_percentage(pulse_width)
    print(f"percentage: {percentage}, pulse_width={pulse_width}, duty_cycle={duty_cycle}")
    return duty_cycle

def map_percentage_to_servo_pulse_width_micros(percentage):
    """Convert a percentage to corresponding pulse width microseconds."""

    return (SERVO_MAX_PULSE_MICROS - SERVO_MIN_PULSE_MICROS) * (percentage - PERCENT_MIN) / (PERCENT_MAX - PERCENT_MIN) + SERVO_MIN_PULSE_MICROS

def map_angle_to_servo_pulse_width_micros(angle):
    """Convert an angle to corresponding pulse width microseconds."""

    return (SERVO_MAX_PULSE_MICROS - SERVO_MIN_PULSE_MICROS) * (angle - ANGLE_MIN_DEGREES) / (ANGLE_MAX_DEGREES - ANGLE_MIN_DEGREES) + SERVO_MIN_PULSE_MICROS

def map_pulse_width_micros_to_duty_cycle_percentage(pulse_width_micros):
    """Convert from pulse width microseconds to a duty cycle percentage."""

    return (PERCENT_MAX - PERCENT_MIN) * pulse_width_micros / PERIOD_MICROS + PERCENT_MIN

ANGLE_MODE = 'angle'
PERCENTAGE_MODE = 'percent'
MODES = [ANGLE_MODE, PERCENTAGE_MODE]

def prompt_for_mode():
    while True:
        raw_mode_str = input("Enter a desired mode ('angle' or 'percent'): ")
        mode_str = raw_mode_str.lower().strip()
        if mode_str in MODES:
            return mode_str
        print(f"'{raw_mode_str}' is not a supported mode. Please try again.")

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.output(PWM_PIN, GPIO.LOW)

pwm = GPIO.PWM(PWM_PIN, FREQUENCY_HZ)
pwm.start(0)

mode = prompt_for_mode()
print(f"Selected mode: '{mode}'")

try:
    while True:
        if mode == ANGLE_MODE:
            angle = float(input('Angle: '))
            duty_cycle = calculate_duty_cycle_for_angle(angle)
            pwm.ChangeDutyCycle(duty_cycle)
        if mode == PERCENTAGE_MODE:
            percent = float(input('Percent: '))
            duty_cycle = calculate_duty_cycle_for_percentage(percent)
            pwm.ChangeDutyCycle(duty_cycle)
        sleep(.1)
except KeyboardInterrupt:
    print('bye')

pwm.stop()
GPIO.cleanup()
