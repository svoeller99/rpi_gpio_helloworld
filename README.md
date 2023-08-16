# RPi GPIO Experiments

## LED Brightness Toggle

A simple, two-button LED brightness toggle using PWM.

[The code](led_brightness_toggle.py)

The circuit:
![LED brightness toggle](led_brightness_toggle.jpeg)

## RGB LED Toggle

3-button RGB LED toggle.

[The code](rgb_led_toggle.py)

The circuit:
![RGB LED Toggle](rgb_led_toggle.jpeg)

## RGB LED Variable Brightness

3-button RGB LED toggle, but where each color of the RGB LED increments exponentially, rather than simply turning on/off.

[The code](rgb_led_variable_toggle.py)

The circuit in this case is identical to [RGB LED Toggle](#rgb-led-toggle).

## Analog Input - Single LED

Analog input with ADC0834 analog-to-digital converter, used to control the brightness of an LED.

[The code](analog_input.py)

The circuit:
![Analog Input - Single LED](analog_input.jpeg)

## Analog Input - RGB LED

Analog input with ADC0834 analog-to-digital converter, used to control the brightness of a the three components of an RGB LED.

[The code](analog_input_rgb_led.py)

The circuit:
![Analog Input - RGB LED](analog_input_rgb_led.jpeg)

## Servo Control From User Input via PWM

Control a servo using PWM given a user-supplied percentage.

[The code](pwm_servo.py)

The circuit:
![Servo Control via PWM](pwm_servo.jpeg)

## Servo Control Using Potentiometer via PWM

Control a servo using PWM given a potentiometer reading.

[The code](pwm_servo_potentiometer.py)

The circuit:
![Servo Control Using Potentiometer](pwm_servo_potentiometer.jpeg)

## Ultrasonic Sensor

Use an ultrasonic sensor to measure the distance of an object in inches.

[The code](ultrasonic_sensor.py)

The circuit:
![Ultrasonic sensor](ultrasonic_sensor.jpeg)