"""
Lonely Binary 1602 I2C LCD - 06: Type in Thonny, Show on the LCD
----------------------------------------------------------------
What you'll learn:
  - Reading a line of text with input()
  - Displaying it on the LCD, wrapped across both rows
  - Clearing stale text properly

HOW TO USE
  1. Press the Run button in Thonny
  2. Click into the Shell panel at the bottom
  3. Type something, press Enter, and watch it appear on the LCD
  4. Type  quit  to stop

Text longer than 32 characters is truncated - that is all a 1602 can
show at once (16 columns x 2 rows).

Made with love by Lonely Binary - From Zeros to Heroes, One Bit at a Time.
"""

from machine import Pin, I2C
from lcd_i2c import LcdI2C

SDA_PIN = 8
SCL_PIN = 9
LCD_ADDR = 0x27

LCD_WIDTH = 16
LCD_ROWS = 2

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=100000)
lcd = LcdI2C(i2c, LCD_ADDR, 16, 2)

lcd.clear()
lcd.set_cursor(0, 0)
lcd.putstr("Type in the")
lcd.set_cursor(0, 1)
lcd.putstr("Thonny shell...")

print("Type a message and press Enter. Type 'quit' to stop.")

while True:
    text = input("> ").strip()

    if text == "quit":
        print("Bye!")
        break

    if not text:
        continue

    # clear() is the right tool here: the new message may be shorter
    # than the old one, and we want no leftovers anywhere on screen.
    lcd.clear()

    # Fill row 0 with the first 16 characters, row 1 with the next 16.
    for row in range(LCD_ROWS):
        start = row * LCD_WIDTH
        if start >= len(text):
            break  # message was short enough to fit on one row
        lcd.set_cursor(0, row)
        lcd.putstr(text[start:start + LCD_WIDTH])
