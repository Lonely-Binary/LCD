"""
Lonely Binary 1602 I2C LCD - 02: Cursor, Blink and Backlight
------------------------------------------------------------
What you'll learn:
  - cursor_on()    / cursor_off()    -> the underline cursor
  - blink_on()     / blink_off()     -> the blinking block
  - display_on()   / display_off()   -> hide the TEXT (light stays on)
  - backlight_on() / backlight_off() -> hide the LIGHT (text stays put)
  - home() vs clear()

The demo walks through each mode and names the function it is showing
on the bottom row. Press Ctrl-C in the shell to stop.

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


def show_label(label):
    """Print a label on the bottom row, wiping what was there before.

    Writing 16 spaces clears one row without the whole-screen flicker
    that clear() causes.
    """
    lcd.set_cursor(0, 1)
    lcd.putstr(" " * 16)
    lcd.set_cursor(0, 1)
    lcd.putstr(label)


lcd.clear()
lcd.set_cursor(0, 0)
lcd.putstr("Lonely Binary")

while True:
    # --- 1. The underline cursor -------------------------------------
    # It appears wherever the next character would be printed.
    lcd.blink_off()
    lcd.cursor_on()
    show_label("cursor_on()")
    time.sleep(3)

    # --- 2. The blinking block ---------------------------------------
    lcd.cursor_off()
    lcd.blink_on()
    show_label("blink_on()")
    time.sleep(3)

    # --- 3. Both at once ---------------------------------------------
    lcd.cursor_on()
    lcd.blink_on()
    show_label("cursor + blink")
    time.sleep(3)

    # --- 4. Neither --------------------------------------------------
    lcd.cursor_off()
    lcd.blink_off()
    show_label("no cursor")
    time.sleep(3)

    # --- 5. Hide the text, keep the light ----------------------------
    # The text is remembered, not erased - it comes straight back.
    show_label("display_off()")
    time.sleep(1.5)
    lcd.display_off()
    time.sleep(1.5)
    lcd.display_on()

    # --- 6. Hide the light, keep the text ----------------------------
    show_label("backlight_off()")
    time.sleep(1.5)
    lcd.backlight_off()
    time.sleep(1.5)
    lcd.backlight_on()

    # --- 7. clear() wipes everything ---------------------------------
    show_label("clear()")
    time.sleep(2)
    lcd.clear()  # erases the screen AND sends the cursor to (0,0)
    time.sleep(1)

    # home() only moves the cursor back to (0,0); it erases nothing.
    lcd.home()
    lcd.putstr("Lonely Binary")
    time.sleep(1)
