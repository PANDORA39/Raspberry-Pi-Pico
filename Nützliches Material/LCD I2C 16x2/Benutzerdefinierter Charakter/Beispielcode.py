from machine import Pin, I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


def arrows():
    lcd.custom_char(0, bytearray([
        0x00,
        0x00,
        0x04,
        0x06,
        0x1F,
        0x06,
        0x04,
        0x00
    ]))

    lcd.custom_char(1, bytearray([
        0x00,
        0x00,
        0x04,
        0x0C,
        0x1F,
        0x0C,
        0x04,
        0x00
    ]))


lcd.clear()
lcd.move_to(4, 0)
lcd.putstr("ERFOLG!!")
lcd.move_to(6, 1)
lcd.putstr("Mehr")
arrows()
lcd.move_to(1, 1)
lcd.putchar(chr(0))
lcd.move_to(14, 1)
lcd.putchar(chr(1))

##################
#     ERFOLG!!   #
# ->   Mehr   <- #
##################