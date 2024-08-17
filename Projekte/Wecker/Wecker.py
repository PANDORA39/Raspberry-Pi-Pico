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
I2C_i_ROWS = 2
I2C_i_COLS = 16

i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_i_ROWS, I2C_i_COLS)

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

#Function that outputs the pressed button 
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

#Output current time and date
def show_datetime():
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

#List of the alarm sounds and the saved sound
sounds = [" Chalet ", "Arpeggio", "Breaking", " Sencha ", " Summit "]

#Select your alarm sound from the available options
def alarm_sounds():
    saved_sound = []
    i = 1
    player.setVolume(30)
    
    custom_characters()
    lcd.move_to(0,0)
    lcd.putchar(chr(2))
    lcd.move_to(15,0)
    lcd.putchar(chr(2))
    lcd.move_to(0,1)
    lcd.putchar(chr(2))
    lcd.move_to(15,1)
    lcd.putchar(chr(2))
    lcd.move_to(3,0)
    lcd.putstr("Select the")
    lcd.move_to(3,1)
    lcd.putstr("alarm tone")
    sleep(2)
    lcd.clear()
    lcd.move_to(5,0)
    lcd.putstr("Select")
    lcd.move_to(0,1)
    lcd.putchar(chr(0))
    lcd.move_to(15,1)
    lcd.putchar(chr(1))
    lcd.move_to(5,1)
    lcd.putstr("Chalet")
    player.playTrack(2,1)
    while player.is_running():
        sleep(0.2)
        if button_3.value() == 1 and i != 5:
            player.pause()
            player.playTrack(2,(i+1))
            lcd.move_to(4,1)
            lcd.putstr(sounds[i])
            i += 1
        if button_3.value() == 1 and i == 5:
            player.pause()
            player.playTrack(2,1)
            lcd.move_to(4,1)
            lcd.putstr(sounds[0])
            i = 1
        if button_1.value() == 1 and i != 1:
            player.pause()
            player.playTrack(2, (i-1))
            lcd.move_to(4,1)
            lcd.putstr(sounds[i-2])
            i -= 1
        if button_1.value() == 1 and i == 1:
            player.pause()
            player.playTrack(2, 5)
            lcd.move_to(4,1)
            lcd.putstr(sounds[4])
            i = 5
        if button_2.value() == 1:
            saved_sound = [i, sounds[i-1]]
            player.pause()
            lcd.clear()
            rgb.color = (0, 255, 0)
            lcd.move_to(1,0)
            lcd.putstr("Sound selected")
            lcd.move_to(4,1)
            lcd.putstr(saved_sound[1])
            lcd.move_to(12,1)
            lcd.putchar(chr(3))
            sleep(3)
            rgb.color = (0, 0, 0)
            lcd.clear()

#Set up an alarm clock
def set_alarm():
    (Y, M, D, day, hr, m, s) = ds.date_time()
    if m < 10:
        m = "0" + str(m)
    if hr < 10:
        hr = "0" + str(hr)
    
    set_time = []
    counter = 0
    
    custom_characters()
    lcd.move_to(0,0)
    lcd.putchar(chr(2))
    lcd.move_to(15,0)
    lcd.putchar(chr(2))
    lcd.move_to(0,1)
    lcd.putchar(chr(2))
    lcd.move_to(15,1)
    lcd.putchar(chr(2))
    lcd.move_to(2,0)
    lcd.putchar(chr(5))
    lcd.move_to(13,0)
    lcd.putchar(chr(5))
    lcd.move_to(5,0)
    lcd.putstr("Set up")
    lcd.move_to(3,1)
    lcd.putstr("your alarm")
    sleep(2)
    lcd.clear()
    lcd.putchar(chr(6))
    lcd.move_to(2,0)
    lcd.putstr("Hour:")
    lcd.move_to(8, 0)
    lcd.putchar(chr(0))
    lcd.move_to(10,0)
    lcd.putstr(str(hr))
    lcd.move_to(13,0)
    lcd.putchar(chr(1))
    lcd.move_to(0,1)
    lcd.putchar(chr(6))
    lcd.move_to(2,1)
    lcd.putstr("Minute:")
    lcd.move_to(10, 1)
    lcd.putchar(chr(0))
    lcd.move_to(12, 1)
    lcd.putstr(str(m))
    lcd.move_to(15,1)
    lcd.putchar(chr(1))
    while counter != 2:
        while len(set_time) != 1:
            sleep(0.2)
            if button_3.value() == 1 and hr != 24:
                lcd.move_to(10,0)
                lcd.putstr(str(hr+1))
                hr += 1
                if hr < 10:
                    lcd.move_to(10,0)
                    lcd.putstr("0" + str(hr))
            if button_3.value() == 1 and hr == 24:
                lcd.move_to(10,0)
                lcd.putstr("01")
                hr = 1
            if button_1.value() == 1 and hr != 0:
                lcd.move_to(10,0)
                lcd.putstr(str(hr-1))
                hr -= 1
                if hr < 10:
                    lcd.move_to(10,0)
                    lcd.putstr("0" + str(hr))
            if button_1.value() == 1 and hr == 0:
                lcd.move_to(10,0)
                lcd.putstr("24")
                hr = 24
            if button_2.value() == 1:
                set_time.append(str(hr))
                counter += 1
        while len(set_time) != 2:
            sleep(0.2)
            if button_3.value() == 1 and m != 60:
                lcd.move_to(12,1)
                lcd.putstr(str(m+1))
                m += 1
                if m < 10:
                    lcd.move_to(12,1)
                    lcd.putstr("0" + str(m))
            if button_3.value() == 1 and m == 60:
                lcd.move_to(12,1)
                lcd.putstr("01")
                m = 1
            if button_1.value() == 1 and m != 0:
                lcd.move_to(12,1)
                lcd.putstr(str(m-1))
                m -= 1
                if m < 10:
                    lcd.move_to(12,1)
                    lcd.putstr("0" + str(m))
            if button_1.value() == 1 and m == 0:
                lcd.move_to(12,1)
                lcd.putstr("59")
                m = 59
            if button_2.value() == 1:
                set_time.append(str(m))
                counter += 1
                sleep(0.5)
                lcd.clear()
    if counter == 2:
        rgb.color = (0, 255, 0)
        lcd.move_to(1,0)
        lcd.putstr("Time selected:")
        lcd.move_to(5,1)
        if len(set_time[0]) == 1:
            set_time[0] = "0" + str(set_time[0])
        if len(set_time[1]) == 1:
            set_time[1] = "0" + str(set_time[1])
        lcd.putstr(f"{set_time[0]}:{set_time[1]}")
        lcd.move_to(12,1)
        lcd.putchar(chr(3))
        sleep(3)
        lcd.clear()
        rgb.color = (0, 0, 0)
                   
#Create custom characters for LCD
def custom_characters():
    #Character '<'
    lcd.custom_char(0, bytearray([
        0x03,
        0x06,
        0x0C,
        0x18,
        0x18,
        0x0C,
        0x06,
        0x03
    ]))
    
    #Character '>'
    lcd.custom_char(1, bytearray([
        0x18,
        0x0C,
        0x06,
        0x03,
        0x03,
        0x06,
        0x0C,
        0x18
    ]))
    
    #Character '▮'
    lcd.custom_char(2, bytearray([
        0x1F,
        0x1F,
        0x1F,
        0x1F,
        0x1F,
        0x1F,
        0x1F,
        0x1F
    ]))
    
    #Character '✓'
    lcd.custom_char(3, bytearray([
        0x00,
        0x01,
        0x03,
        0x16,
        0x1C,
        0x08,
        0x00,
        0x00
    ]))
    
    #Character '♪'
    lcd.custom_char(4, bytearray([
        0x01,
        0x03,
        0x05,
        0x09,
        0x09,
        0x0B,
        0x1B,
        0x18
    ]))
    
    #Character '🔔'
    lcd.custom_char(5, bytearray([
        0x04,
        0x0E,
        0x0E,
        0x0E,
        0x1F,
        0x00,
        0x04,
        0x00
    ]))
    
    #Character '•'
    lcd.custom_char(6, bytearray([
        0x00,
        0x0E,
        0x1F,
        0x1F,
        0x1F,
        0x1F,
        0x0E,
        0x00
    ]))

       
while True:
    set_alarm()