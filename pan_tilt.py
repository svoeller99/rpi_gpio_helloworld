import RPi.GPIO as GPIO
import time
from servo_util import degrees_to_duty_cycle

# change modes
SUDDEN = 'SUDDEN'
GRADUAL = 'GRADUAL'
PAN_PIN_DEFAULT = 12
TILT_PIN_DEFAULT = 13

class PanTilt:
    def __init__(self, pan_pin=PAN_PIN_DEFAULT, tilt_pin=TILT_PIN_DEFAULT, change_mode=SUDDEN):
        self.pan_pin = pan_pin
        self.tilt_pin = tilt_pin
        self.change_mode = change_mode
        self.degrees_by_pin = dict([(pan_pin, 0), (tilt_pin, 0)])

    def start(self):
        self.tilt_pwm = self._init_servo_pwm(self.tilt_pin)
        self.pan_pwm = self._init_servo_pwm(self.pan_pin)
        
    def stop(self):
        self.tilt_pwm.ChangeDutyCycle(0)
        self.pan_pwm.ChangeDutyCycle(0)
        self.tilt_pwm.stop()
        self.pan_pwm.stop()
    
    def set_pan(self, pan_degrees):
        self._change_degrees(self.pan_pin, PanTilt._normalize_degrees(pan_degrees))

    def set_tilt(self, tilt_degrees):
        self._change_degrees(self.tilt_pin, PanTilt._normalize_degrees(tilt_degrees))

    def _change_degrees(self, pin, degrees):
        if self.change_mode == SUDDEN:
            self._suddenly_change_degrees(pin, degrees)
        else:
            self._gradually_change_degrees(pin, degrees)
        self.degrees_by_pin.update(dict([(pin, degrees)]))
        print(self.degrees_by_pin)

    def _gradually_change_degrees(self, pin, degrees):
        increments = 100
        pwm = self._pwm_for_pin(pin)
        prior_degrees = self.degrees_by_pin.get(pin)
        degrees_increment = abs(degrees - prior_degrees) / increments
        if degrees < prior_degrees:
            degrees_increment *= -1
        print(f"Changing from {prior_degrees} to {degrees} degrees. Increment: {degrees_increment}")
        current_degrees = prior_degrees
        while (degrees_increment > 0 and current_degrees < degrees) or (degrees_increment < 0 and current_degrees > degrees):
            current_degrees += degrees_increment
            pwm.ChangeDutyCycle(degrees_to_duty_cycle(current_degrees))
            time.sleep(0.01)
        pwm.ChangeDutyCycle(0)
        time.sleep(.2)

    def _suddenly_change_degrees(self, pin, new_degrees):
        pwm = self._pwm_for_pin(pin)
        duty_cycle = degrees_to_duty_cycle(new_degrees)
        self._set_duty_cycle_and_stop(pwm, duty_cycle)

    def _pwm_for_pin(self, pin) -> GPIO.PWM:
        if pin == self.pan_pin:
            return self.pan_pwm
        if pin == self.tilt_pin:
            return self.tilt_pwm
        raise NotImplementedError(f"No PWM for pin {pin}")

    def _init_servo_pwm(self, pin) -> GPIO.PWM:
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 50) # 50 Hz (20 ms PWM period)
        pwm.start(degrees_to_duty_cycle(90))
        self.degrees_by_pin.update(dict([(pin, 90)]))
        return pwm

    @staticmethod
    def _set_duty_cycle_and_stop(pwm: GPIO.PWM, duty_cycle):
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.2) # wait for motion to complete
        pwm.ChangeDutyCycle(0) # turn off servo
    
    @staticmethod
    def _normalize_degrees(degrees):
        if degrees < 0:
            degrees = 0
        if degrees > 180:
            degrees = 180
        return degrees


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    pan_tilt = PanTilt()
    pan_tilt.start()
    
    # test pan
    for ii in range(0,2):
        pan_tilt.set_pan(30) # right
        time.sleep(1)
        pan_tilt.set_pan(120) # left
        time.sleep(1)
        pan_tilt.set_pan(90) # center
        time.sleep(1)

    # test tilt
    for ii in range(0,2):
        pan_tilt.set_tilt(30) # up
        time.sleep(1)
        pan_tilt.set_tilt(120) # down
        time.sleep(1)
        pan_tilt.set_tilt(90) # center
        time.sleep(1)

    pan_tilt.stop()
    GPIO.cleanup()