import RPi.GPIO as GPIO

# Constants for button state
BUTTON_DOWN = 1
BUTTON_UP = 0

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