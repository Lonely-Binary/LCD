/*
 * Lonely Binary 1602 I2C LCD — 02: Cursor, Blink and Backlight
 * ------------------------------------------------------------
 * What you'll learn:
 *   - cursor()    / noCursor()    -> show or hide the underline cursor
 *   - blink()     / noBlink()     -> show or hide the blinking block
 *   - display()   / noDisplay()   -> hide the TEXT (backlight stays on)
 *   - backlight() / noBacklight() -> hide the LIGHT (text stays put)
 *   - home() vs clear()
 *
 * The demo walks through each mode, one every 3 seconds, and names the
 * function it is currently demonstrating on the bottom row.
 *
 * Made with love by Lonely Binary — From Zeros to Heroes, One Bit at a Time.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Print a label on the bottom row, wiping whatever was there before.
// Printing 16 spaces is a quick way to erase a single row without the
// full-screen flicker that lcd.clear() causes.
void showLabel(const char *label) {
  lcd.setCursor(0, 1);
  lcd.print("                ");  // exactly 16 spaces
  lcd.setCursor(0, 1);
  lcd.print(label);
}

void setup() {
  // ESP32-S3? Uncomment and set your GPIOs. Must come before lcd.init().
  // Wire.begin(8, 9);

  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Lonely Binary");
}

void loop() {
  // --- 1. The underline cursor -------------------------------------
  // It appears wherever the next character would be printed.
  lcd.noBlink();
  lcd.cursor();
  showLabel("cursor()");
  delay(3000);

  // --- 2. The blinking block ---------------------------------------
  lcd.noCursor();
  lcd.blink();
  showLabel("blink()");
  delay(3000);

  // --- 3. Both at once ---------------------------------------------
  lcd.cursor();
  lcd.blink();
  showLabel("cursor + blink");
  delay(3000);

  // --- 4. Neither --------------------------------------------------
  lcd.noCursor();
  lcd.noBlink();
  showLabel("no cursor");
  delay(3000);

  // --- 5. Hide the text, keep the light ----------------------------
  // noDisplay() blanks the characters but the backlight stays on, so
  // the screen glows empty. The text is remembered, not erased.
  showLabel("noDisplay()");
  delay(1500);
  lcd.noDisplay();
  delay(1500);
  lcd.display();  // the text comes straight back

  // --- 6. Hide the light, keep the text ----------------------------
  showLabel("noBacklight()");
  delay(1500);
  lcd.noBacklight();
  delay(1500);
  lcd.backlight();

  // --- 7. clear() wipes everything ---------------------------------
  showLabel("clear()");
  delay(2000);
  lcd.clear();  // erases the screen AND sends the cursor to (0,0)
  delay(1000);

  // home() only moves the cursor back to (0,0); it erases nothing.
  lcd.home();
  lcd.print("Lonely Binary");
  delay(1000);
}
