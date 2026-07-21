"""
Lonely Binary 1602 I2C LCD - MicroPython driver
-----------------------------------------------
A small, dependency-free driver for the Lonely Binary 1602 I2C LCD
(HD44780 controller behind a PCF8574-style I2C expander).

Copy this file to your board once, then use it from any script:

    from machine import Pin, I2C
    from lcd_i2c import LcdI2C

    i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100000)
    lcd = LcdI2C(i2c, 0x27, 16, 2)
    lcd.putstr("Hello!")

Made with love by Lonely Binary - From Zeros to Heroes, One Bit at a Time.
"""

import time

# --- How the I2C expander is wired to the LCD ---------------------------
_RS = 0x01          # 0 = command, 1 = character data
_RW = 0x02          # always 0 here: we only ever write
_EN = 0x04          # the "latch this nibble now" strobe
_BACKLIGHT = 0x08   # 1 = backlight on
# The upper four bits (0xF0) carry the data nibble.

# --- HD44780 instructions ------------------------------------------------
_CMD_CLEAR = 0x01
_CMD_HOME = 0x02
_CMD_ENTRY_MODE = 0x04
_CMD_DISPLAY_CTRL = 0x08
_CMD_SHIFT = 0x10
_CMD_FUNCTION_SET = 0x20
_CMD_SET_CGRAM = 0x40
_CMD_SET_DDRAM = 0x80

# Entry mode flags
_ENTRY_LEFT = 0x02
_ENTRY_SHIFT = 0x01

# Display control flags
_DISPLAY_ON = 0x04
_CURSOR_ON = 0x02
_BLINK_ON = 0x01

# Cursor/display shift flags
_SHIFT_DISPLAY = 0x08
_SHIFT_RIGHT = 0x04

# Start address of each row in the controller's memory
_ROW_OFFSETS = (0x00, 0x40, 0x14, 0x54)


class LcdI2C:
    """Drive an HD44780 character LCD over I2C."""

    def __init__(self, i2c, addr=0x27, cols=16, rows=2):
        self.i2c = i2c
        self.addr = addr
        self.cols = cols
        self.rows = rows

        self._backlight = _BACKLIGHT
        self._display_ctrl = _DISPLAY_ON      # display on, cursor off, blink off
        self._entry_mode = _ENTRY_LEFT        # left to right, no auto-shift

        self._init_display()

    # -- low level ------------------------------------------------------
    def _write_raw(self, value):
        self.i2c.writeto(self.addr, bytes([value & 0xFF]))

    def _pulse(self, value):
        """Latch one nibble by strobing the enable line."""
        self._write_raw(value | _EN)
        time.sleep_us(1)
        self._write_raw(value & ~_EN & 0xFF)
        time.sleep_us(50)

    def _send(self, value, mode):
        """Send one byte as two 4-bit nibbles, high nibble first."""
        base = mode | self._backlight
        self._pulse((value & 0xF0) | base)
        self._pulse(((value << 4) & 0xF0) | base)

    def command(self, value):
        """Send an instruction byte to the controller."""
        self._send(value, 0)

    def write_byte(self, value):
        """Send one character byte to the screen."""
        self._send(value, _RS)

    def _init_display(self):
        # The controller needs time to wake up after power is applied.
        time.sleep_ms(50)

        # Ask for 8-bit mode three times. This is the documented way to get
        # the controller into a known state no matter how it powered up.
        self._pulse(0x30 | self._backlight)
        time.sleep_ms(5)
        self._pulse(0x30 | self._backlight)
        time.sleep_us(150)
        self._pulse(0x30 | self._backlight)
        time.sleep_us(150)

        # Now switch it to 4-bit mode, which is all our 4 data lines allow.
        self._pulse(0x20 | self._backlight)
        time.sleep_us(150)

        self.command(_CMD_FUNCTION_SET | 0x08)  # 4-bit, 2 lines, 5x8 dots
        self.command(_CMD_DISPLAY_CTRL)         # display off while we set up
        self.clear()
        self.command(_CMD_ENTRY_MODE | self._entry_mode)
        self.command(_CMD_DISPLAY_CTRL | self._display_ctrl)

    # -- text -----------------------------------------------------------
    def clear(self):
        """Erase everything and move the cursor to the top left."""
        self.command(_CMD_CLEAR)
        time.sleep_ms(2)  # this instruction is slow

    def home(self):
        """Move the cursor to the top left. Erases nothing."""
        self.command(_CMD_HOME)
        time.sleep_ms(2)

    def set_cursor(self, col, row):
        """Move the cursor. Both col and row start counting at 0."""
        if row >= self.rows:
            row = self.rows - 1
        self.command(_CMD_SET_DDRAM | (col + _ROW_OFFSETS[row]))

    def putstr(self, text):
        """Print a string at the current cursor position."""
        for char in text:
            self.write_byte(ord(char))

    def putchar(self, slot):
        """Print one of your custom characters, by slot number (0-7)."""
        self.write_byte(slot)

    # -- backlight ------------------------------------------------------
    def backlight_on(self):
        self._backlight = _BACKLIGHT
        self._write_raw(self._backlight)

    def backlight_off(self):
        self._backlight = 0
        self._write_raw(0)

    # -- display, cursor, blink -----------------------------------------
    def _update_display_ctrl(self):
        self.command(_CMD_DISPLAY_CTRL | self._display_ctrl)

    def display_on(self):
        self._display_ctrl |= _DISPLAY_ON
        self._update_display_ctrl()

    def display_off(self):
        self._display_ctrl &= ~_DISPLAY_ON
        self._update_display_ctrl()

    def cursor_on(self):
        self._display_ctrl |= _CURSOR_ON
        self._update_display_ctrl()

    def cursor_off(self):
        self._display_ctrl &= ~_CURSOR_ON
        self._update_display_ctrl()

    def blink_on(self):
        self._display_ctrl |= _BLINK_ON
        self._update_display_ctrl()

    def blink_off(self):
        self._display_ctrl &= ~_BLINK_ON
        self._update_display_ctrl()

    # -- scrolling ------------------------------------------------------
    def scroll_display_left(self):
        self.command(_CMD_SHIFT | _SHIFT_DISPLAY)

    def scroll_display_right(self):
        self.command(_CMD_SHIFT | _SHIFT_DISPLAY | _SHIFT_RIGHT)

    def autoscroll_on(self):
        self._entry_mode |= _ENTRY_SHIFT
        self.command(_CMD_ENTRY_MODE | self._entry_mode)

    def autoscroll_off(self):
        self._entry_mode &= ~_ENTRY_SHIFT
        self.command(_CMD_ENTRY_MODE | self._entry_mode)

    # -- custom characters ----------------------------------------------
    def create_char(self, slot, bitmap):
        """
        Store a custom 5x8 character.

        slot   : 0-7, which of the eight custom slots to use
        bitmap : eight numbers, one per pixel row, lowest 5 bits used
        """
        slot &= 0x07
        self.command(_CMD_SET_CGRAM | (slot << 3))
        for row in bitmap:
            self.write_byte(row & 0x1F)
        # Leave the controller pointing back at the screen, not at CGRAM,
        # so the next putstr() lands where you expect.
        self.set_cursor(0, 0)
