"""
Lonely Binary 1602 I2C LCD - 01: Hello World
--------------------------------------------
What you'll learn:
  - Setting up the I2C bus on the pins you chose
  - Creating the LcdI2C object
  - Placing text with set_cursor(column, row)

BEFORE YOU RUN THIS
  Copy lcd_i2c.py to your board first! In Thonny that is
  right-click the file -> "Upload to /".

WARNING: the LCD runs at 5 V and pulls SDA/SCL up to 5 V. On a 3.3 V
board put a logic level converter on SDA/SCL to protect the MCU.

Made with love by Lonely Binary - From Zeros to Heroes, One Bit at a Time.
"""

from machine import Pin, I2C
from lcd_i2c import LcdI2C

# ---- Change these to match your wiring -------------------------------
SDA_PIN = 8
SCL_PIN = 9
LCD_ADDR = 0x27  # run 00_i2c_scan.py if nothing appears

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=100000)

# 16 columns, 2 rows
lcd = LcdI2C(i2c, LCD_ADDR, 16, 2)

lcd.clear()

# set_cursor(column, row) - BOTH start counting at 0, not 1.
# Columns run 0..15 left to right. Rows run 0..1 top to bottom.
lcd.set_cursor(0, 0)  # first column, top row
lcd.putstr("Lonely Binary")

lcd.set_cursor(0, 1)  # first column, bottom row
lcd.putstr("Hello, World!")

print("Done - look at your LCD!")
