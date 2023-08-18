#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

BUZZER_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.HIGH)
buzzer_pwm = GPIO.PWM(BUZZER_PIN, 440)
buzzer_pwm.start(50)

try:
    while True:
        buzzer_pwm.ChangeFrequency(110)
        sleep(.5)
        buzzer_pwm.ChangeFrequency(220)
        sleep(.5)
        buzzer_pwm.ChangeFrequency(440)
        sleep(1)
except KeyboardInterrupt:
    print('bye')

buzzer_pwm.stop()
GPIO.output(BUZZER_PIN, GPIO.HIGH)
GPIO.cleanup()