from Driver import DFPlayer
from machine import Pin, freq
from ir_rx.print_error import print_error
from ir_rx.nec import NEC_8

UART_INSTANCE = 0 
TX_PIN = 16
RX_PIN = 17
BUSY_PIN = 6

pin_ir = Pin(8, Pin.IN)
player = DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)

def decodeKeyValue(data):
    if data == 0x0C:
        player.playTrack(1,1)
    if data == 0x18:
        player.playTrack(1,2)
    if data == 0x5E:
        return "3"
    if data == 0x08:
        return "4"
    if data == 0x1C:
        return "5"
    if data == 0x5A:
        return "6"
    if data == 0x42:
        return "7"
    if data == 0x52:
        return "8"
    if data == 0x4A:
        return "9"
    if data == 0x09:
        return "+"
    if data == 0x15:
        player.increaseVolume()
    if data == 0x7:
        player.decreaseVolume()
    if data == 0x0D:
        return "U/SD"
    if data == 0x19:
        return "CYCLE"
    if data == 0x44:
        pass
    counter = 0
    if data == 0x43 and counter%2 == 0:
        player.pause()
        counter += 1
    elif data == 0x43 and counter%2 != 0:
        player.resume()
        counter += 1
    if data == 0x40:
        pass
    if data == 0x45:
        return "POWER"
    if data == 0x47:
        return "MUTE"
    if data == 0x46:
        return "MODE"
    return "ERROR"

# User callback
def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        print(decodeKeyValue(data))

ir = NEC_8(pin_ir, callback)  # Instantiate receiver
ir.error_function(print_error)  # Show debug information







