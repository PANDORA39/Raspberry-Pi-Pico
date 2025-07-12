#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Blog: https://peppe8o.com
# Date: Apr 09th, 2022
# Version: 1.0

# import required modules
from machine import Pin
import utime

# define variables
#           Higher --------------Lower
led_list = [6,7,8,9,10,11,12,13,14,15] # GP ports used

# Convert led_list from a number list into a PIN objects list
n=0 # n is the list index
for pin_num in led_list:
  led_list[n] = Pin(pin_num, Pin.OUT)
  n+=1

# Function to show a user defined led configuration
def LedSegOut(array):
  for x in range(10): led_list[x].value(not(array[x]))

# Function to show leds turning in a cycle
def LedSegCycle():
  array = [0,0,0,0,0,0,0,0,0,1]
  while True:
    array = array[1:]+array[:1]
    LedSegOut(array)
    utime.sleep(0.05)

# Function to show a filling ercentage
def LedSegPerc(n):
  thresholds=[100,90,80,70,60,50,40,30,20,10]
  array=list(map(lambda x: (1,0)[x>n],thresholds))
  LedSegOut(array)

# Start the main loop
while True:
   # LedSegOut([0,0,0,0,0,1,1,1,1,1])
   LedSegCycle()
   # LedSegPerc(82)
