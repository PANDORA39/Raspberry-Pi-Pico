from machine import Pin, ADC, PWM
from picozero import RGBLED
from utime import sleep

pot = ADC(26)

rgb = RGBLED(red = 6, green = 7, blue = 8)

display_list = [17,16,14,13,12,18,19] 
dotPin = 15
display_obj = []

for seg in display_list:
    display_obj.append(Pin(seg, Pin.OUT))   
dot_obj=Pin(dotPin, Pin.OUT)
arrSeg = [[1,1,1,1,1,1,0],
          [0,1,1,0,0,0,0], 
          [1,1,0,1,1,0,1], 
          [1,1,1,1,0,0,1], 
          [0,1,1,0,0,1,1], 
          [1,0,1,1,0,1,1], 
          [1,0,1,1,1,1,1], 
          [1,1,1,0,0,0,0], 
          [1,1,1,1,1,1,1], 
          [1,1,1,1,0,1,1]]

def SegDisplay(toDisplay):
    numDisplay = int(toDisplay.replace(".", ""))
    for a in range(7):
        display_obj[a].value(arrSeg[numDisplay][a])
    if toDisplay.count(".") == 1:
        dot_obj.value(1)
    else:
        dot_obj.value(0)
        
def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min)

while True:
    pot_value = pot.read_u16()
    percentage = map(pot_value, 288, 65535,0, 100)
    
    numbers = [i for i in range(0, 10)]
    percents = [i for i in range(0, 101, 10)]
    colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0),
              (0, 255, 0), (0, 0, 255), (255, 255, 0),
              (0, 255, 255), (12, 10, 110), (6, 150, 57),
              (252, 8, 187)]
    
    for num, per, col in zip(numbers, percents, colors):
        if per-10 < percentage <= per:
            SegDisplay(str(num))
            rgb.color = (col)
            
    