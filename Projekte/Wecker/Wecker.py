from machine import Pin, I2C
from picozero import RGBLED
from utime import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from Driver import DFPlayer
from ds1302 import DS1302
from threading import Thread

button_1 = Pin(9, Pin.IN)
button_2 = Pin(8, Pin.IN)
button_3 = Pin(5, Pin.IN)

rgb = RGBLED(red=11, green=12, blue=13)

UART_INSTANCE = 0
TX_PIN = 16
RX_PIN = 17
BUSY_PIN = 6

player = DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)

I2C_ADDR = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

ds = DS1302(Pin(0), Pin(1), Pin(2))

matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'B'],
               ['7', '8', '9', 'C'],
               ['*', '0', '#', 'D']]

# PINs according to schematic - Change the pins to match with your connections
keypad_rows = [18, 19, 20, 21]
keypad_columns = [22, 26, 27, 28]

# Create two empty lists to set up pins ( Rows output and columns input )
col_pins = []
row_pins = []


def scankeys():
    for row in range(4):
        for col in range(4):
            row_pins[row].high()
            key = None

            if col_pins[col].value() == 1:
                print("You have pressed:", matrix_keys[row][col])
                key_press = matrix_keys[row][col]
                sleep(0.3)

        row_pins[row].low()


# Loop to assign GPIO pins and setup input and outputs
for x in range(0, 4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)
    

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