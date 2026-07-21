"""
Lonely Binary 1602 I2C LCD - 03: Counting, and the Ghost Digit Bug
------------------------------------------------------------------
What you'll learn:
  - How to update a changing number on screen
  - The #1 beginner LCD bug: leftover "ghost" digits
  - The fix, shown SIDE BY SIDE on the two rows
  - Using ticks_ms() instead of sleep() so the loop stays responsive

Watch the display as the countdown crosses 100 -> 99:

  Top row (wrong):    "Bad:  990"   <- the old '0' never got erased!
  Bottom row (right): "Good:  99"

An LCD has no concept of "erasing" - printing only overwrites the
characters you actually print. A 2-digit number written over a 3-digit
number leaves the last digit behind.

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

lcd.clear()

count = 105                 # start above 100 so you see the bug
INTERVAL_MS = 400           # milliseconds between updates
last_update = time.ticks_ms()

while True:
    # ticks_diff() is the safe way to compare times in MicroPython - it
    # copes with the millisecond counter wrapping back around to zero.
    if time.ticks_diff(time.ticks_ms(), last_update) < INTERVAL_MS:
        continue
    last_update = time.ticks_ms()

    # --- The WRONG way ------------------------------------------------
    # No padding. When count drops from 100 to 99 we write only two
    # characters over a three character number, so the stale third
    # digit stays on screen forever.
    lcd.set_cursor(0, 0)
    lcd.putstr("Bad:  " + str(count))

    # --- The RIGHT way ------------------------------------------------
    # "%3d" always produces exactly three characters, padding with
    # spaces, so shorter numbers overwrite the leftovers.
    lcd.set_cursor(0, 1)
    lcd.putstr("Good: %3d" % count)

    count -= 1
    if count < 0:
        count = 105
        lcd.clear()  # tidy up before the next run
