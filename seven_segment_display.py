import RPi.GPIO as GPIO
import time

# Set up pins

# Serial data input pin.
# Serial shift input pin - this receives the data via a sequence of 8 bits.
SDI   = 17    # connects to pin 14 (DS) of 74HC595

# Time sequence input of storage register. 
# On the rising edge, data in the shift register moves into memory register.
RCLK  = 18    # connects to pin 12 (STcp) of 74HC595

# Time sequence input of shift register. 
# On the rising edge, the data in shift register moves successively one bit, 
# i.e. data in Q1 moves to Q2, and so forth. 
# While on the falling edge, the data in shift register remain unchanged.
SRCLK = 27    # connects to pin 11 (SHcp) of 74HC595

# Define a segment code from 0 to F in Hexadecimal
segCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71]

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SDI, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RCLK, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(SRCLK, GPIO.OUT, initial=GPIO.LOW)

# Shift the data to 74HC595
def hc595_shift(dat):
    for bit in range(0, 8):
        # send the current bit
        GPIO.output(SDI, 0x80 & (dat << bit))
        # set high to move the bit we just sent in the shift register of the 74CH595
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001) # wait a moment to allow the chip to see the SRCLK transition
        # set SRCLK back to low - no change to the shift register resulting from this
        GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)

def main():
    while True:
        # Shift the code one by one from segCode list
        for code in segCode:
            hc595_shift(code)
            print ("segCode[%s]: 0x%02X"%(segCode.index(code), code)) # %02X means double digit HEX to print
            time.sleep(0.5)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()