"""
Lonely Binary - I2C Scanner (MicroPython)
-----------------------------------------
Scans the I2C bus and prints the address of every device that responds.
Use it to find the address of your 1602 I2C LCD (usually 0x27, sometimes 0x3F).

Tested on ESP32-S3 / ESP32 / Raspberry Pi Pico.
Any two free GPIOs can be used for SDA and SCL - just change the pins below.

WARNING: the LCD runs at 5 V and pulls SDA/SCL up to 5 V. On a 3.3 V board
(ESP32-S3, Pico, ...) put a logic level converter on SDA/SCL to protect the MCU.

Made with love by Lonely Binary - From Zeros to Heroes, One Bit at a Time.
"""

from machine import Pin, I2C
import time

# ---- Change these to the GPIOs you wired the LCD to ----
SDA_PIN = 8
SCL_PIN = 9

# I2C bus speed. 100_000 (100 kHz) is the safest for character LCDs.
I2C_FREQ = 100_000

# I2C peripheral id: 0 on most boards. Use 1 if your pins belong to bus 1.
I2C_ID = 0

KNOWN_LCD_ADDRESSES = (0x27, 0x3F)


def scan(i2c):
    """Scan the bus and print every address that acknowledges."""
    print("Scanning...")
    devices = i2c.scan()

    if not devices:
        print("  No I2C devices found - check VCC, GND, SDA and SCL wiring.")
    else:
        for address in devices:
            note = "  <- looks like a 1602 I2C LCD" if address in KNOWN_LCD_ADDRESSES else ""
            print("  Device found at 0x{:02X} ({}){}".format(address, address, note))
        print("  Done. {} device(s) found.".format(len(devices)))

    print()
    return devices


def main():
    i2c = I2C(I2C_ID, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=I2C_FREQ)

    print("Lonely Binary I2C Scanner")
    print("-------------------------")
    print("SDA=GPIO{}, SCL=GPIO{}, freq={} Hz".format(SDA_PIN, SCL_PIN, I2C_FREQ))
    print()

    while True:
        scan(i2c)
        time.sleep(5)


if __name__ == "__main__":
    main()
