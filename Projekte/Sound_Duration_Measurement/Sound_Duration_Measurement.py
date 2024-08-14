from machine import Pin
from utime import sleep

sound_sensor = Pin(20, Pin.IN)
button = Pin(21, Pin.IN,  Pin.PULL_UP)

display_list = [17,16,14,13,12,18,19]
dotPin=15
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
        
SegDisplay(str(1))
    
while True:
    for i in range(0, 10, 1):
        if sound_sensor.value() == 1:
            SegDisplay(str(i))
            sleep(1)
        else:
            break
        
    if button.value() == 0:
        SegDisplay("0")

                
            
        
        
