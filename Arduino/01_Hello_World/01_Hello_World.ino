/*
 * Lonely Binary 1602 I2C LCD — 01: Hello World
 * --------------------------------------------
 * What you'll learn:
 *   - Starting the LCD and turning on the backlight
 *   - Placing the cursor with setCursor(column, row)
 *   - Printing text
 *
 * Wiring (Arduino UNO):
 *   LCD VCC -> 5V     LCD SDA -> A4
 *   LCD GND -> GND    LCD SCL -> A5
 *
 * Blank screen? Adjust the contrast trimmer first (gently, ~1 turn max).
 * Backlight on but no text? Run 00_I2C_Scanner to find your real address.
 *
 * Made with love by Lonely Binary — From Zeros to Heroes, One Bit at a Time.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// 0x27 is the most common address; try 0x3F if nothing shows up.
// The 16 and 2 are the size of the display: 16 columns, 2 rows.
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  // Using an ESP32-S3? Uncomment the next line and set your own GPIOs.
  // It MUST come before lcd.init(), or your pins will be ignored.
  // Wire.begin(8, 9);

  lcd.init();       // wake the LCD up
  lcd.backlight();  // turn the backlight on

  // setCursor(column, row) — BOTH start counting at 0, not 1.
  // Columns run 0..15 left to right. Rows run 0..1 top to bottom.
  lcd.setCursor(0, 0);  // first column, top row
  lcd.print("Lonely Binary");

  lcd.setCursor(0, 1);  // first column, bottom row
  lcd.print("Hello, World!");
}

void loop() {
  // Everything was drawn once in setup(), so there is nothing to repeat.
  // Whatever you print stays on screen until you overwrite or clear it.
}
