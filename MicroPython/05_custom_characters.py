"""
Lonely Binary 1602 I2C LCD - 05: Custom Characters
--------------------------------------------------
What you'll learn:
  - Designing your own 5x8 pixel characters
  - Loading them with create_char()
  - Printing them with putchar()

HOW IT WORKS
Every character cell is 5 pixels wide and 8 pixels tall. You describe
one as 8 rows of binary, where a 1 lights a pixel. Only the lowest 5
bits of each row are used, so 0b00000 to 0b11111. Written out in
binary you can literally see the picture in your source code:

    0b00000        . . . . .
    0b01010        . # . # .
    0b11111        # # # # #
    0b11111        # # # # #     <- a heart
    0b11111        # # # # #
    0b01110        . # # # .
    0b00100        . . # . .
    0b00000        . . . . .

ONE LIMIT TO REMEMBER
You get 8 custom characters at a time, in slots 0 to 7.

Made with love by Lonely Binary - From Zeros to Heroes, One Bit at a Time.
"""

from machine import Pin, I2C
from lcd_i2c import LcdI2C
import time

SDA_PIN = 8
SCL_PIN = 9
LCD_ADDR = 0x27

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=100000)
lcd = LcdI2C(i2c, LCD_ADDR, 16, 2)

HEART = [0b00000, 0b01010, 0b11111, 0b11111, 0b11111, 0b01110, 0b00100, 0b00000]
BELL = [0b00100, 0b01110, 0b01110, 0b01110, 0b11111, 0b00000, 0b00100, 0b00000]
DEGREE = [0b01100, 0b10010, 0b10010, 0b01100, 0b00000, 0b00000, 0b00000, 0b00000]
ARROW = [0b00000, 0b00100, 0b00110, 0b11111, 0b11111, 0b00110, 0b00100, 0b00000]
BATTERY = [0b01110, 0b11011, 0b10001, 0b10001, 0b11111, 0b11111, 0b11111, 0b00000]
NOTE = [0b00010, 0b00011, 0b00010, 0b00010, 0b01110, 0b11110, 0b01100, 0b00000]
SMILEY = [0b00000, 0b01010, 0b01010, 0b00000, 0b10001, 0b01110, 0b00000, 0b00000]
LOCK = [0b01110, 0b10001, 0b10001, 0b11111, 0b11011, 0b11011, 0b11111, 0b00000]

# Load each design into one of the 8 available slots.
for slot, bitmap in enumerate(
    (HEART, BELL, DEGREE, ARROW, BATTERY, NOTE, SMILEY, LOCK)
):
    lcd.create_char(slot, bitmap)

lcd.clear()
lcd.set_cursor(0, 0)
lcd.putstr("Custom chars:")

# Print all 8, separated by a space.
lcd.set_cursor(0, 1)
for slot in range(8):
    lcd.putchar(slot)
    lcd.putstr(" ")

while True:
    # Custom characters mix freely with ordinary text.
    time.sleep(4)
    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.putstr("We ")
    lcd.putchar(0)  # heart
    lcd.putstr(" MicroPython")
    lcd.set_cursor(0, 1)
    lcd.putstr("Temp: 24")
    lcd.putchar(2)  # degree symbol
    lcd.putstr("C")

    time.sleep(4)
    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.putstr("Lonely Binary")
    lcd.set_cursor(0, 1)
    for slot in range(8):
        lcd.putchar(slot)
        lcd.putstr(" ")
