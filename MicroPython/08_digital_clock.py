"""
Lonely Binary 1602 I2C LCD - 08: Digital Clock  [CAPSTONE]
----------------------------------------------------------
What you'll learn:
  - Turning a millisecond counter into hours, minutes and seconds
  - Formatting fixed-width text with "%02d"
  - Redrawing ONLY when something changed, to kill flicker

A NOTE ON ACCURACY
This clock counts from the moment the script started, and it drifts
because it runs off the board's oscillator rather than a real time
source. It is a great exercise, not a wristwatch. For real timekeeping
add an RTC module such as a DS3231.

Made with love by Lonely Binary - From Zeros to Heroes, One Bit at a Time.
"""

from machine import Pin, I2C
from lcd_i2c import LcdI2C
import time

SDA_PIN = 8
SCL_PIN = 9
LCD_ADDR = 0x27

# Set these to the current time and the clock will start from there.
START_HOUR = 9
START_MINUTE = 30
START_SECOND = 0

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=100000)
lcd = LcdI2C(i2c, LCD_ADDR, 16, 2)

start_offset = START_HOUR * 3600 + START_MINUTE * 60 + START_SECOND
started_at = time.ticks_ms()
last_drawn_second = -1

lcd.clear()
lcd.set_cursor(0, 0)
lcd.putstr("Lonely Binary")

while True:
    elapsed_ms = time.ticks_diff(time.ticks_ms(), started_at)
    total_seconds = start_offset + elapsed_ms // 1000

    # Only redraw when the second actually ticks over. Without this
    # guard we would rewrite the screen thousands of times per second,
    # which both flickers and hammers the I2C bus for no reason.
    current_second = total_seconds % 60
    if current_second == last_drawn_second:
        continue
    last_drawn_second = current_second

    hours = (total_seconds // 3600) % 24
    minutes = (total_seconds // 60) % 60
    seconds = total_seconds % 60

    # "%02d" means: at least 2 digits, padded with a leading zero.
    # That is what turns 9:5:3 into a tidy 09:05:03.
    lcd.set_cursor(0, 1)
    lcd.putstr("   %02d:%02d:%02d   " % (hours, minutes, seconds))

    # Every 10 seconds, swap the top row between a greeting and uptime.
    if seconds % 10 == 0:
        up_minutes = elapsed_ms // 60000
        lcd.set_cursor(0, 0)
        if (seconds // 10) % 2 == 0:
            lcd.putstr("Lonely Binary   ")
        else:
            lcd.putstr("Up: %d min      " % up_minutes)
