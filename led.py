import RPi.GPIO as GPIO

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
            self.set_duty_cycle(100)
        else:
            self.set_duty_cycle(0)
        print(f'Toggled LED "{self.name}" to {self.current_state}')

    def set_duty_cycle(self, duty_cycle):
        self.pwm.ChangeDutyCycle(duty_cycle)

    def __del__(self):
        self.pwm.stop()