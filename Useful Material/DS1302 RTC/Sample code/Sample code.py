from machine import Pin, I2C
from utime import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from ds1302 import DS1302

I2C_ADDR = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

ds = DS1302(Pin(0), Pin(1), Pin(2))

while True:
    (Y, M, D, day, hr, m, s) = ds.date_time()
    if s < 10:
        s = "0" + str(s)
    if m < 10:
        m = "0" + str(m)
    if hr < 10:
        hr = "0" + str(hr)
    if D < 10:
        D = "0" + str(D)
    if M < 10:
        M = "0" + str(M)

    lcd.move_to(0, 0)
    lcd.putstr("Time: " + str(hr) + ":" + str(m) + ":" + str(s))
    lcd.move_to(0, 1)
    lcd.putstr("Date: " + str(D) + "/" + str(M) + "/" + str(Y))

