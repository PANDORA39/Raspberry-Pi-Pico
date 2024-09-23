from machine import Pin, I2C
from picozero import RGBLED
from utime import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from Driver import DFPlayer
from ds1302 import DS1302
from threading import Thread
from random import randint, choice
from operator import add, sub, mul

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

i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=600000)
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

# Loop to assign GPIO pins and setup input and outputs
for x in range(0, 4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)

global entered
entered = []

#Function that outputs the pressed button 
def scankeys():
    global row
    global col
    
    for row in range(4):
        for col in range(4):
            row_pins[row].high()
            key = None
            
            if col_pins[col].value() == 1:
                entered.append(matrix_keys[row][col])
                sleep(0.1)
                if matrix_keys[row][col] == "A":
                    print("A")
                    player.pause()
                    main_func()
                elif matrix_keys[row][col] == "B":
                    print("B")
                    player.pause()
                    funcs[1]()
                elif matrix_keys[row][col] == "C":
                    print("C")
                    player.pause()
                    funcs[2]()

        row_pins[row].low()
    return entered
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

#Get red or green light
def RGB(color_ID, t=1):
    if color_ID == 0:
        rgb.color = (255, 0, 0)
        sleep(t)
        rgb.color = (0, 0, 0)
    elif color_ID == 1:
        rgb.color = (0, 255, 0)
        sleep(t)
        rgb.color = (0, 0, 0)
        
#Select your alarm sound from the available options
def alarm_sounds():
    lcd.clear()
    global saved_sound
    saved_sound = []
    i = 1
    player.setVolume(5)
    
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
    while True:
        print("alarm_sounds")
        if scankeys()[-1] != 'B' or scankeys().count('B') > 1:
            print("return alarm_sounds")
            return
        sleep(0.1)
        if button_3.value() == 1 and i != 5:
            lcd.move_to(4,1)
            lcd.putstr(sounds[i])
            player.playTrack(2,(i+1))
            i += 1
        elif button_3.value() == 1 and i == 5:
            lcd.move_to(4,1)
            lcd.putstr(sounds[0])
            player.playTrack(2,1)
            i = 1
        elif button_1.value() == 1 and i != 1:
            lcd.move_to(4,1)
            lcd.putstr(sounds[i-2])
            player.playTrack(2, (i-1))
            i -= 1
        elif button_1.value() == 1 and i == 1:
            lcd.move_to(4,1)
            lcd.putstr(sounds[4])
            player.playTrack(2, 5)
            i = 5
        elif button_2.value() == 1:
            saved_sound = [i, sounds[i-1]]
            player.pause()
            lcd.clear()
            lcd.move_to(1,0)
            lcd.putstr("Sound selected")
            lcd.move_to(4,1)
            lcd.putstr(saved_sound[1])
            lcd.move_to(12,1)
            lcd.putchar(chr(3))
            RGB(1, 3)
            lcd.clear()
            break

#Set up an alarm clock
def set_alarm():
    lcd.clear()
    (Y, M, D, day, hr, m, s) = ds.date_time()
    if m < 10:
        m = "0" + str(m)
    if hr < 10:
        hr = "0" + str(hr)
    
    global set_time
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
            print("set_alarm 1")
            if scankeys()[-1] != 'C' or scankeys().count('C') > 1:
                print("return set_alarm")
                return
            sleep(0.1)
            if button_3.value() == 1 and hr != 24:
                lcd.move_to(10,0)
                lcd.putstr(str(hr+1))
                hr += 1
                if hr < 10:
                    lcd.move_to(10,0)
                    lcd.putstr("0" + str(hr))
            elif button_3.value() == 1 and hr == 24:
                lcd.move_to(10,0)
                lcd.putstr("01")
                hr = 1
            elif button_1.value() == 1 and hr != 0:
                lcd.move_to(10,0)
                lcd.putstr(str(hr-1))
                hr -= 1
                if hr < 10:
                    lcd.move_to(10,0)
                    lcd.putstr("0" + str(hr))
            elif button_1.value() == 1 and hr == 0:
                lcd.move_to(10,0)
                lcd.putstr("24")
                hr = 24
            elif button_2.value() == 1:
                set_time.append(str(hr))
                counter += 1
        while len(set_time) != 2:
            print("set_alarm 2")
            scankeys()
            sleep(0.1)
            if button_3.value() == 1 and m != 60:
                lcd.move_to(12,1)
                lcd.putstr(str(m+1))
                m += 1
                if m < 10:
                    lcd.move_to(12,1)
                    lcd.putstr("0" + str(m))
            elif button_3.value() == 1 and m == 60:
                lcd.move_to(12,1)
                lcd.putstr("01")
                m = 1
            elif button_1.value() == 1 and m != 0:
                lcd.move_to(12,1)
                lcd.putstr(str(m-1))
                m -= 1
                if m < 10:
                    lcd.move_to(12,1)
                    lcd.putstr("0" + str(m))
            elif button_1.value() == 1 and m == 0:
                lcd.move_to(12,1)
                lcd.putstr("59")
                m = 59
            elif button_2.value() == 1:
                set_time.append(str(m))
                counter += 1
                sleep(0.5)
                lcd.clear()
    if counter == 2:
        lcd.move_to(1,0)
        lcd.putstr("Time selected:")
        lcd.move_to(5,1)
        if len(set_time[0]) == 1:
            set_time[0] = "0" + str(set_time[0])
        elif len(set_time[1]) == 1:
            set_time[1] = "0" + str(set_time[1])
        lcd.putstr(f"{set_time[0]}:{set_time[1]}")
        RGB(1, 3)
        lcd.clear()
        return
        

#Get random mathematical equation
def get_random_task(i):
    global solution
    counter = 0
    num_1 = randint(50,99)
    num_2 = randint(0, 49)
    operator = choice([add, sub, mul])
    solution = str(operator(num_1, num_2))
    op = ""
    
    if operator == add:
        op = "+"
    elif operator == sub:
        op = "-"
    else:
        op = "*"
        
    lcd.clear()
    scankeys()
    lcd.move_to(0,0)
    lcd.putstr(f"{i+1}. Do the math:")
    lcd.move_to(0,1)
    lcd.putstr(f"{num_1} {op} {num_2} =")
    
#Alarm gets activated --> deactivate an alarm
def deactivate_alarm():
    lcd.clear()
    global set_time
    global saved_sound
    global solution
    global entered
    score = 0
    (Y, M, D, day, hr, m, s) = ds.date_time()
    
    print("deactivate_alarm")
    if hr == int(set_time[0]) and m == int(set_time[1]):
        player.playTrack(2, int(saved_sound[0]))
        print("deactivate_alarm 1")
        while score < 3:
            print("deactivate_alarm 2")
            get_random_task(score)            
            while len(scankeys()) != len(solution):
                if player.is_playing() == False:
                    player.playTrack(2, int(saved_sound[0]))
                lcd.move_to(10,1)
                lcd.putstr(entered)
            if ''.join(entered) == solution:
                score += 1                
                lcd.move_to(10,1)
                lcd.putstr(entered)
                RGB(1)
                entered = []
            else:
                lcd.move_to(10,1)
                lcd.putstr(entered)
                RGB(0)
                entered = []
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Alarm turned off")
        sleep(3)
        lcd.clear()
        
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

funcs = [show_datetime, alarm_sounds, set_alarm, deactivate_alarm]

#Main function
def main_func():
    while True:
        print("main")
        funcs[0]()
        scankeys()

main_func()

#Problem 1: rechtzeitiger Aufruf von 'deactivate_alarm'
#Problem 2: B/C(nicht abgeschlossen) --> B/C(abgeschlossen) --> B/C statt A
