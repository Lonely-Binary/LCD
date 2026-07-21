/*
 * Lonely Binary 1602 I2C LCD — 03: Counting, and the Ghost Digit Bug
 * ------------------------------------------------------------------
 * What you'll learn:
 *   - How to update a changing number on screen
 *   - The #1 beginner LCD bug: leftover "ghost" digits
 *   - Two ways to fix it, shown SIDE BY SIDE on the two rows
 *   - Using millis() instead of delay() so the sketch stays responsive
 *
 * Watch the display as the countdown crosses 100 -> 99:
 *
 *   Top row (wrong):  "Bad:  990"   <- the old '0' never got erased!
 *   Bottom row (right): "Good:  99"
 *
 * An LCD has no concept of "erasing" — printing only overwrites the
 * characters you actually print. A 2-digit number written over a
 * 3-digit number leaves the last digit behind.
 *
 * Made with love by Lonely Binary — From Zeros to Heroes, One Bit at a Time.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

int count = 105;                    // start above 100 so you see the bug
unsigned long lastUpdate = 0;       // when we last redrew the screen
const unsigned long INTERVAL = 400; // milliseconds between updates

char buffer[17];                    // 16 characters + the string terminator

void setup() {
  // ESP32-S3? Uncomment and set your GPIOs. Must come before lcd.init().
  // Wire.begin(8, 9);

  lcd.init();
  lcd.backlight();
}

void loop() {
  // millis() returns how long the board has been running. Comparing it
  // like this lets us "wait" without freezing the whole sketch the way
  // delay() would — loop() keeps running and could read a button too.
  if (millis() - lastUpdate < INTERVAL) {
    return;
  }
  lastUpdate = millis();

  // --- The WRONG way ------------------------------------------------
  // We print the number with no padding. When count drops from 100 to
  // 99 we only write two characters over a three character number, so
  // the stale third digit stays on screen forever.
  lcd.setCursor(0, 0);
  lcd.print("Bad:  ");
  lcd.print(count);

  // --- The RIGHT way ------------------------------------------------
  // snprintf builds a fixed-width string. "%3d" always produces exactly
  // three characters, padding with spaces, so shorter numbers overwrite
  // the leftovers. Same idea as printing trailing spaces yourself:
  //     lcd.print(count); lcd.print("   ");
  snprintf(buffer, sizeof(buffer), "Good: %3d", count);
  lcd.setCursor(0, 1);
  lcd.print(buffer);

  // Count down, then start over so the bug repeats every cycle.
  count--;
  if (count < 0) {
    count = 105;
    lcd.clear();  // tidy up before the next run
  }
}
