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

## Temperature / Humidity Detector

Display the current temperature and humidity.

[The code](temp_humidity_detector.py)

The circuit:
![Temp / Humidity Detector](temp_humidity_detector.jpeg)

## LCD Temperature / Humidity Display

Display the current temperature and humidity with a button to toggle between Celcius and Fahrenheit.

[The code](lcd_temperature_display.py)

The circuit:
![LCD Temp/Humidity Display](lcd_temperature_display.jpeg)

## Buzzers - Active and Passive

Make buzzers make sounds.

[Active buzzer code](active_buzzer.py)

[Passive buzzer code](passive_buzzer.py)

The circuit (identical for both active/passive, except for the type of buzzer used):
![Buzzer](buzzer.jpeg)

## Temperature Sensor With Configurable Alarm

Temperature sensor with configurable temperature that - if exceeded - will cause a buzzer to sound.

[The code](temperature_sensing_alarm.py)

The circuit:
![Temperature Sensor With Configurable Alarm](temperature_sensing_alarm.jpeg)

## Photoresistor

Photoresistor experiments.

[Basic photoresistor test](photoresistor.py)
[Photoresistor / motion detector alarm](photoresistor_motion_detector.py)