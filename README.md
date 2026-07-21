# Lonely Binary 1602 I2C LCD Display

Thank you for purchasing the **Lonely Binary Liquid Crystal Display Set**. This 16×2 character LCD ships with the I2C interface **built directly onto the board** — no bulky add-on backpack required — giving you a sleeker, lower-profile display that talks to your microcontroller over just two data wires.

This guide covers wiring, contrast adjustment, the recommended Arduino library, and a ready-to-run example sketch.

---

## Highlights

- **16×2 character display** (1602A) with a crisp, backlit screen
- **Built-in I2C interface** — the I2C controller is integrated on the PCB, not a separate soldered-on backpack
- **Only 4 wires** to connect: `VCC`, `GND`, `SDA`, `SCL`
- **On-board contrast trimmer** for fine-tuning readability
- Works great with Arduino, and with 3.3 V boards when paired with a logic level converter (see below)

---

## Integrated I2C — No Add-On Backpack

Unlike traditional character LCDs that require a separate I2C "backpack" module soldered to the 16-pin header, the Lonely Binary LCD has the **I2C function built right into the board**. The highlighted chip below is the on-board I2C controller — this is what keeps the module slim and easy to wire.

<p align="center">
  <img src="images/lcd-i2c-onboard-chip.png" alt="Lonely Binary 1602 LCD showing the on-board I2C controller chip highlighted" width="640">
</p>

---

## Wiring

The LCD exposes a simple 4-pin I2C header:

| LCD Pin | Connect To            | Notes                                  |
| :------ | :-------------------- | :------------------------------------- |
| `GND`   | Ground                | Common ground with your MCU            |
| `VCC`   | **5 V**               | The LCD is a 5 V device — see below    |
| `SDA`   | I2C data              | e.g. Arduino UNO `A4`                   |
| `SCL`   | I2C clock             | e.g. Arduino UNO `A5`                   |

### ⚠️ 5 V Operation & 3.3 V Microcontrollers

**This LCD is designed to run at 5 V.** On the board, the `SDA` and `SCL` lines are pulled up to 5 V.

If you are using a **3.3 V microcontroller** — such as an **ESP32, ESP32-S3, or Raspberry Pi Pico** — those 5 V signals can exceed what the MCU's GPIO pins are rated to accept. In the short term the board may appear to work fine, but over the long term the 5 V level on the I2C lines can **permanently damage** your ESP32-S3 or similar 3.3 V board.

To protect your microcontroller, we strongly recommend placing a **Lonely Binary 2-Channel Logic Level Converter** between the 3.3 V MCU and the 5 V LCD on the `SDA` and `SCL` lines.

> 🛒 **Lonely Binary 2CH Logic Level Converter:** https://www.amazon.com/dp/B0FFMLDYNY

<p align="center">
  <img src="images/lonely-binary-logic-level-converter.png" alt="Lonely Binary 2/4/6 Channel Bi-Directional Logic Level Converter" width="640">
</p>

---

## Contrast Adjustment (Fix Blank or "Block" Characters)

When you first power up the display, you may see **solid blocks**, extremely faint text, or nothing at all. This is almost always a **contrast** setting — not a fault.

<p align="center">
  <img src="images/lcd-contrast-blocks.png" alt="1602 LCD showing solid blocks instead of characters — contrast needs adjusting" width="640">
</p>

To fix it, use a small screwdriver to gently turn the **contrast potentiometer** (the tiny blue trimmer on the board) until the characters become clear.

> ⚠️ **Important:** The trimmer has a very limited travel of roughly **one turn only**. Turn it **slowly and gently** — do **not** force it past its stop. The pot is delicate and can be easily damaged by over-turning.

---

## Arduino IDE Setup

For the Arduino IDE, we recommend the **`LiquidCrystal I2C`** library by **Frank de Brabander**.

1. Open the Arduino IDE
2. Go to **Sketch → Include Library → Manage Libraries…** (or click the Library Manager icon)
3. Search for **`LiquidCrystal I2C`**
4. Select the library by **Frank de Brabander** and click **Install**

<p align="center">
  <img src="images/liquidcrystal-i2c-library.png" alt="LiquidCrystal I2C library by Frank de Brabander in the Arduino Library Manager" width="360">
</p>

---

## Example Sketch — Hello, World!

Once the library is installed, upload the sketch below. Most of these modules use I2C address **`0x27`** (some use `0x3F`).

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Set the LCD I2C address (0x27 is most common; try 0x3F if nothing shows)
// 16 columns, 2 rows
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init();        // initialize the LCD
  lcd.backlight();   // turn on the backlight

  lcd.setCursor(0, 0);
  lcd.print("Lonely Binary");
  lcd.setCursor(0, 1);
  lcd.print("Hello, World!");
}

void loop() {
  // nothing to do here
}
```

### Not sure of your I2C address?

If `0x27` doesn't work, run an **I2C scanner** sketch to discover the address, then update the value in `LiquidCrystal_I2C lcd(0x27, 16, 2);`.

```cpp
#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  while (!Serial);
  Serial.println("I2C Scanner");
}

void loop() {
  byte count = 0;
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("Found device at 0x");
      Serial.println(addr, HEX);
      count++;
    }
  }
  Serial.println(count ? "Done." : "No I2C devices found.");
  delay(5000);
}
```

---

## Troubleshooting

| Symptom                              | Likely Cause / Fix                                                                 |
| :----------------------------------- | :--------------------------------------------------------------------------------- |
| Solid blocks or blank screen         | Adjust the **contrast** trimmer (see above) — gently, ~1 turn max                  |
| Backlight on, but no text            | Wrong I2C address — run the **I2C scanner** and update the address in your sketch  |
| Nothing at all / no backlight        | Check `VCC` (5 V) and `GND` wiring                                                 |
| Garbled characters on a 3.3 V board  | Add a **logic level converter** on `SDA`/`SCL` (see 5 V Operation above)           |

---

## Specifications

| Item              | Detail                                  |
| :---------------- | :-------------------------------------- |
| Display           | 1602A, 16 characters × 2 lines          |
| Interface         | I2C (built-in, integrated on PCB)       |
| Operating voltage | 5 V                                     |
| I2C address       | 0x27 (typical) or 0x3F                   |
| Contrast          | On-board single-turn trimmer            |

---

## Support

Made with ❤️ by **Lonely Binary** — *From Zeros to Heroes, One Bit at a Time.*

If you run into any issues, double-check the wiring and contrast first, then reach out through your point of purchase for assistance.
