"""
Lonely Binary 1602 I2C LCD - 07: Progress Bar  [CAPSTONE]
---------------------------------------------------------
Combines what you learned in 05 (custom characters) with a little
arithmetic to build something genuinely useful.

THE TRICK
A row is only 16 characters wide, which would give a very chunky bar.
But each character is 5 pixels wide, so if we design characters that
are 1, 2, 3, 4 and 5 columns full, we can fill the row one PIXEL at a
time instead of one CHARACTER at a time:

    16 characters x 5 pixels = 80 steps of resolution

So for any percentage we work out how many pixel columns to light,
then draw: a run of completely full cells, one partial cell, and
spaces for the rest.

Made with love by Lonely Binary - From Zeros to Heroes, One Bit at a Time.
"""

from machine import Pin, I2C
from lcd_i2c import LcdI2C
import time

SDA_PIN = 8
SCL_PIN = 9
LCD_ADDR = 0x27

LCD_WIDTH = 16
PIXELS_PER_CHAR = 5
TOTAL_PIXELS = LCD_WIDTH * PIXELS_PER_CHAR  # 80

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=100000)
lcd = LcdI2C(i2c, LCD_ADDR, 16, 2)

# Five characters: 1 column full, 2 columns full, ... 5 columns full.
# Each is solid top to bottom, so they line up into a continuous bar.
BLOCKS = (
    [0b10000] * 8,
    [0b11000] * 8,
    [0b11100] * 8,
    [0b11110] * 8,
    [0b11111] * 8,
)

for slot, bitmap in enumerate(BLOCKS):
    lcd.create_char(slot, bitmap)


def draw_bar(percent, row):
    """Draw a bar for percent (0-100) on the given row."""
    percent = max(0, min(100, percent))

    # How many pixel columns should be lit in total?
    lit_pixels = percent * TOTAL_PIXELS // 100

    full_cells = lit_pixels // PIXELS_PER_CHAR   # completely filled characters
    remainder = lit_pixels % PIXELS_PER_CHAR     # leftover columns in next cell

    lcd.set_cursor(0, row)
    for cell in range(LCD_WIDTH):
        if cell < full_cells:
            lcd.putchar(4)                # the fully filled block
        elif cell == full_cells and remainder > 0:
            lcd.putchar(remainder - 1)    # slot 0..3 = 1..4 columns
        else:
            lcd.putstr(" ")               # empty, and erases the old bar


lcd.clear()

while True:
    # Fill up 0 -> 100%
    for percent in range(101):
        lcd.set_cursor(0, 0)
        lcd.putstr("Loading... %3d%%" % percent)
        draw_bar(percent, 1)
        time.sleep(0.06)

    lcd.set_cursor(0, 0)
    lcd.putstr("Complete!      ")
    time.sleep(2)

    # Drain back down again so the demo loops.
    for percent in range(100, -1, -1):
        lcd.set_cursor(0, 0)
        lcd.putstr("Unloading  %3d%%" % percent)
        draw_bar(percent, 1)
        time.sleep(0.03)
    time.sleep(1)
