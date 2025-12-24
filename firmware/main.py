import board
import time
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.scanners import DiodeOrientation
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.display import Display
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.extensions.display import TextEntry

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP27, board.GP28, board.GP29)
keyboard.row_pins = (board.GP2, board.GP1, board.GP0)
keyboard.diode_orientation = DiodeOrientation.ROWS


encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.GP3, board.GP4, None, False),)
keyboard.modules.append(encoder_handler)

# a funny macro that open a terminal that play a dancing parrot
PARROT = KC.MACRO(
    Press(KC.LGUI),     
    Tap(KC.R),         
    Release(KC.LGUI),

    KC.DELAY(300), 

    Tap(KC.C), Tap(KC.M), Tap(KC.D),  
    Tap(KC.ENTER),

    KC.DELAY(300),        

    Tap(KC.C), Tap(KC.U), Tap(KC.R), Tap(KC.LSPACE),
    Tap(KC.P), Tap(KC.A), Tap(KC.R), Tap(KC.R),
    Tap(KC.O), Tap(KC.T),
    Tap(KC.DOT),
    Tap(KC.L), Tap(KC.I), Tap(KC.V), Tap(KC.E),
    Tap(KC.ENTER),
)

keyboard.keymap = [
    [
        KC.A,          PARROT,        KC.MUTE,
        KC.LCTL(KC.T), KC.LCTL(KC.W) ,KC.LCTL(KC.SHIFT(KC.N)),
        KC.LCTL(KC.C), KC.LCTL(KC.V), KC.LCTL(KC.X),
    ]   
]

encoder_handler.map = [ ((KC.VOLU, KC.VOLD),) ]

#--

oled = Display(
    display=SSD1306(
        width=128,
        height=32,
        i2c=board.I2C(),
        device_address=0x3C,
    ),
)

keyboard.extensions.append(oled)

start_time = time.monotonic()

def display_text():
    elapsed = time.monotonic() - start_time

    if elapsed < 3:
        return "Ciao!"
    else:
        seconds = int(elapsed)
        minutes = seconds // 60
        hours = minutes // 60
        return f"Usage time:    {hours:02}:{minutes%60:02}:{seconds%60:02}"


oled.entries = [
    TextEntry(
        text=display_text,
        x=32,
        y=12,
    )
]


if __name__ == '__main__':
    keyboard.go()