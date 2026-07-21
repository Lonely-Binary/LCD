"""
Lonely Binary 1602 I2C LCD - 04: Scrolling Text
-----------------------------------------------
What you'll learn:
  - Why a 1602 can hold more text than it can show
  - Method 1: scroll a long message yourself, one window at a time
  - Method 2: scroll_display_left() / scroll_display_right()
  - Method 3: autoscroll_on()

THE KEY IDEA
A 1602 has 40 characters of memory per row, but only a 16 character
window is visible. Scrolling does not move your text - it slides the
window across the memory. Anything past column 39 is simply lost.

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

LCD_WIDTH = 16

# A message far longer than the 16 visible columns.
message = "From Zeros to Heroes, One Bit at a Time.   "

while True:
    # ================================================================
    # METHOD 1 - scroll it yourself
    # Keep the text in a normal string and show a different 16
    # character slice each time. Most flexible, works for any length.
    # ================================================================
    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.putstr("1: manual window")

    for start in range(len(message) - LCD_WIDTH + 1):
        lcd.set_cursor(0, 1)
        lcd.putstr(message[start:start + LCD_WIDTH])
        time.sleep(0.25)
    time.sleep(0.5)

    # ================================================================
    # METHOD 2 - let the LCD slide the window for you
    # Each call shifts the visible window by one column. The text must
    # already fit inside the 40 character row.
    # ================================================================
    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.putstr("2: scroll_disp")
    lcd.set_cursor(0, 1)
    lcd.putstr("Lonely Binary")
    time.sleep(1)

    for _ in range(16):
        lcd.scroll_display_left()
        time.sleep(0.2)
    for _ in range(16):
        lcd.scroll_display_right()  # and slide it back
        time.sleep(0.2)
    time.sleep(0.5)

    # ================================================================
    # METHOD 3 - autoscroll
    # With autoscroll on, the display shifts itself every time you
    # print a character, so new text pushes the old text along.
    # ================================================================
    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.putstr("3: autoscroll")

    lcd.set_cursor(15, 1)  # park at the right edge
    lcd.autoscroll_on()
    for i in range(12):
        lcd.putstr(str(i % 10))
        time.sleep(0.3)
    lcd.autoscroll_off()  # ALWAYS turn it back off, or later prints misbehave
    time.sleep(1)
