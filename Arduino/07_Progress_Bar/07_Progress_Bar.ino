/*
 * Lonely Binary 1602 I2C LCD — 07: Progress Bar  [CAPSTONE]
 * ---------------------------------------------------------
 * Combines what you learned in 05 (custom characters) with a little
 * arithmetic to build something genuinely useful.
 *
 * THE TRICK
 * A row is only 16 characters wide, which would give a very chunky bar.
 * But each character is 5 pixels wide, so if we design characters that
 * are 1, 2, 3, 4 and 5 columns full, we can fill the row one PIXEL at
 * a time instead of one CHARACTER at a time:
 *
 *     16 characters x 5 pixels = 80 steps of resolution
 *
 * So for any percentage we work out how many pixel columns to light,
 * then draw: a run of completely full cells, one partial cell, and
 * spaces for the rest.
 *
 * Made with love by Lonely Binary — From Zeros to Heroes, One Bit at a Time.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int LCD_WIDTH = 16;
const int PIXELS_PER_CHAR = 5;
const int TOTAL_PIXELS = LCD_WIDTH * PIXELS_PER_CHAR;  // 80

// Five characters: 1 column full, 2 columns full, ... 5 columns full.
// Each is solid top to bottom, so they line up into a continuous bar.
byte block1[8] = { B10000, B10000, B10000, B10000, B10000, B10000, B10000, B10000 };
byte block2[8] = { B11000, B11000, B11000, B11000, B11000, B11000, B11000, B11000 };
byte block3[8] = { B11100, B11100, B11100, B11100, B11100, B11100, B11100, B11100 };
byte block4[8] = { B11110, B11110, B11110, B11110, B11110, B11110, B11110, B11110 };
byte block5[8] = { B11111, B11111, B11111, B11111, B11111, B11111, B11111, B11111 };

char buffer[17];

// Draw a bar for `percent` (0-100) on the given row.
void drawBar(int percent, int row) {
  percent = constrain(percent, 0, 100);

  // How many pixel columns should be lit in total?
  // The (long) cast keeps 100 * 80 from overflowing a 16-bit int on the UNO.
  int litPixels = (int)((long)percent * TOTAL_PIXELS / 100);

  int fullCells = litPixels / PIXELS_PER_CHAR;   // completely filled characters
  int remainder = litPixels % PIXELS_PER_CHAR;   // leftover columns in the next cell

  lcd.setCursor(0, row);
  for (int cell = 0; cell < LCD_WIDTH; cell++) {
    if (cell < fullCells) {
      lcd.write(byte(4));                 // block5 — completely full
    } else if (cell == fullCells && remainder > 0) {
      lcd.write(byte(remainder - 1));     // slot 0..3 = block1..block4
    } else {
      lcd.print(' ');                     // empty, and erases the old bar
    }
  }
}

void setup() {
  // ESP32-S3? Uncomment and set your GPIOs. Must come before lcd.init().
  // Wire.begin(8, 9);

  lcd.init();
  lcd.backlight();

  // Slots 0..4 hold our five partial-block designs.
  lcd.createChar(0, block1);
  lcd.createChar(1, block2);
  lcd.createChar(2, block3);
  lcd.createChar(3, block4);
  lcd.createChar(4, block5);
}

void loop() {
  // Fill up 0 -> 100%
  for (int percent = 0; percent <= 100; percent++) {
    snprintf(buffer, sizeof(buffer), "Loading... %3d%%", percent);
    lcd.setCursor(0, 0);
    lcd.print(buffer);

    drawBar(percent, 1);
    delay(60);
  }

  lcd.setCursor(0, 0);
  lcd.print("Complete!      ");
  delay(2000);

  // Drain back down again so the demo loops.
  for (int percent = 100; percent >= 0; percent--) {
    snprintf(buffer, sizeof(buffer), "Unloading  %3d%%", percent);
    lcd.setCursor(0, 0);
    lcd.print(buffer);

    drawBar(percent, 1);
    delay(30);
  }
  delay(1000);
}
