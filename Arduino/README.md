# Arduino Examples — Lonely Binary 1602 I2C LCD

**Thank you for purchasing the Lonely Binary Liquid Crystal Display Set!** 🎉

Your purchase is what funds tutorials like this one — every example here is written, wired up and tested on real hardware so you get working code instead of a guess. We genuinely appreciate your support.

← Back to the [main guide](../README.md) for wiring, contrast adjustment and troubleshooting.

---

## What's in here

A numbered, step-by-step tutorial series. Each sketch teaches **one new idea**, builds on the one before it, and is commented line by line. Start at `00` and work down.

| # | Sketch | What you'll learn |
| :-- | :--------------------------------------------- | :----------------------------------------------------------------------------- |
| 00 | [`00_I2C_Scanner`](00_I2C_Scanner)             | Find your display's I2C address — **run this first**                            |
| 01 | [`01_Hello_World`](01_Hello_World)             | `init()`, `backlight()`, and placing text with `setCursor(column, row)`         |
| 02 | [`02_Cursor_And_Blink`](02_Cursor_And_Blink)   | The underline cursor, the blinking block, hiding the text vs. the backlight     |
| 03 | [`03_Counter`](03_Counter)                     | Displaying changing numbers — and fixing the classic "ghost digit" bug          |
| 04 | [`04_Scrolling_Text`](04_Scrolling_Text)       | Three ways to scroll messages longer than 16 characters                         |
| 05 | [`05_Custom_Characters`](05_Custom_Characters) | Design your own 5×8 symbols — hearts, bells, degree signs                       |
| 06 | [`06_Serial_To_LCD`](06_Serial_To_LCD)         | Type in the Serial Monitor, watch it appear on the LCD                          |
| 07 | [`07_Progress_Bar`](07_Progress_Bar)           | **Capstone** — a smooth 80-step progress bar built from custom characters       |
| 08 | [`08_Digital_Clock`](08_Digital_Clock)         | **Capstone** — a flicker-free clock using `millis()` and `snprintf()`           |

---

## Before you start

**1. Install the library.** In the Arduino IDE go to **Sketch → Include Library → Manage Libraries…**, search for `LiquidCrystal I2C`, and install the one by **Frank de Brabander**.

**2. Run `00_I2C_Scanner`.** Every other sketch assumes address `0x27`. If your scan reports something different (`0x3F` is the other common one), change this line at the top of the sketch:

```cpp
LiquidCrystal_I2C lcd(0x27, 16, 2);   // <- your address here
```

**3. Nothing on screen?** Adjust the contrast trimmer before you suspect the code — see [Contrast Adjustment](../README.md#contrast-adjustment-fix-blank-or-block-characters). Turn it gently; it has about one turn of travel.

Sketches that print to the Serial Monitor use **9600** baud (the scanner uses 115200 on ESP32).

---

## Using an ESP32-S3

The tutorial sketches `01`–`08` are written for the Arduino UNO to keep them easy to read. Running them on an ESP32-S3 takes **two steps**.

### ⚠️ Step 1: Protect your board with a logic level converter

**This is not optional.** The LCD runs at 5 V and pulls `SDA` and `SCL` up to 5 V. The ESP32-S3 is a 3.3 V device — feeding 5 V into its GPIO pins can **permanently damage it**. It may appear to work at first, then fail later.

Put a **2-channel logic level converter** on the `SDA` and `SCL` lines, with the LV side to the ESP32-S3 (3.3 V) and the HV side to the LCD (5 V). Both sides need power and ground.

> 🛒 **Lonely Binary 2CH Logic Level Converter:** https://www.amazon.com/dp/B0FFMLDYNY

<p align="center">
  <img src="../images/lonely-binary-logic-level-converter.png" alt="Lonely Binary Bi-Directional Logic Level Converter" width="520">
</p>

### Step 2: Tell the sketch which GPIOs you used

The ESP32-S3 can use **almost any free GPIO** for I2C — you are not tied to fixed pins like the UNO's `A4`/`A5`. Open the sketch, find this block in `setup()`, and uncomment it with your own pin numbers:

```cpp
void setup() {
  // Using an ESP32-S3? Uncomment the next line and set your own GPIOs.
  // It MUST come before lcd.init(), or your pins will be ignored.
  Wire.begin(8, 9);        // <- your SDA, SCL

  lcd.init();
  lcd.backlight();
  ...
```

> **Why the order matters:** the `LiquidCrystal_I2C` library calls `Wire.begin()` internally with no pin arguments. If you start the bus *first* with your own pins, the library's call does nothing and your choice is kept. Do it the other way round and your GPIOs are silently ignored — you'll get a blank screen with no error message.

`00_I2C_Scanner` is the exception: it already detects the ESP32 at compile time. Just set the pins at the top of that file instead:

```cpp
#define I2C_SDA_PIN 8
#define I2C_SCL_PIN 9
```

### Quick reference

| | Arduino UNO | ESP32-S3 |
| :-- | :-- | :-- |
| SDA / SCL | Fixed: `A4` / `A5` | Any free GPIO (default in these examples: `8` / `9`) |
| Level converter | Not needed (5 V board) | **Required** |
| Code change | None | Uncomment `Wire.begin(SDA, SCL);` before `lcd.init()` |
| Serial Monitor | 9600 | 9600 (scanner: 115200) |

---

## Support

Made with ❤️ by **Lonely Binary** — *From Zeros to Heroes, One Bit at a Time.*

If a sketch doesn't behave, check the [Troubleshooting table](../README.md#troubleshooting) in the main guide first — the vast majority of issues are contrast, address, or wiring rather than code.
