#!/usr/bin/python3

import LCD1602
import smbus2
from i2caddr import I2C_ADDR

# first arg - address that can be obtained by running `i2cdetect -y 1`
# second arg - whether or not to backlight the LCD (1=true, 0=false)
LCD1602.init(I2C_ADDR, 1)

try:
    while True:
        # first two args are X and Y coordinates to write to (start is top-left)
        LCD1602.write(0, 0, "Hello World")
        LCD1602.write(0, 1, "Welcome")
except KeyboardInterrupt:
    print('bye')

LCD1602.clear()
