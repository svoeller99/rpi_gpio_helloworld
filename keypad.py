import RPi.GPIO as GPIO
from time import sleep

class KeyPad:
    BUTTONS = [
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"]
    ]
    DEFAULT_ROW_PINS = [18,23,24,25]
    DEFAULT_COL_PINS = [10,22,27,17]
    DEFAULT_RETURN_CHAR = 'D'

    def __init__(self, row_pins=DEFAULT_ROW_PINS.copy(), column_pins=DEFAULT_COL_PINS.copy(), return_char=DEFAULT_RETURN_CHAR):
        self.row_pins = row_pins
        self.column_pins = column_pins
        self.return_char = return_char
        self.last_button_pressed = None
        self.buttons_pressed = []
        self.__init_gpio()

    def __init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.row_pins: GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        for pin in self.column_pins: GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read(self):
        # cycle through row pins and turn each on, followed by reading each column pin in a nested loop to detect what keys are pressed
        button_pressed = None
        for row_idx, row_pin in enumerate(self.row_pins):
            GPIO.output(row_pin, GPIO.HIGH)
            for col_idx, col_pin in enumerate(self.column_pins):
                if GPIO.input(col_pin) == GPIO.HIGH:
                    button_pressed = self.BUTTONS[row_idx][col_idx]
            GPIO.output(row_pin, GPIO.LOW)
        if button_pressed != self.last_button_pressed:
            self.last_button_pressed = button_pressed
            if button_pressed == self.return_char:
                entered_sequence = "".join(self.buttons_pressed)
                self.buttons_pressed = []
                return entered_sequence
            elif button_pressed:
                self.buttons_pressed.append(button_pressed)
        sleep(.05)
