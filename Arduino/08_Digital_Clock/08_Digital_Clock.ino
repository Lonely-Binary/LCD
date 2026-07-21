/*
 * Lonely Binary 1602 I2C LCD — 08: Digital Clock  [CAPSTONE]
 * ----------------------------------------------------------
 * What you'll learn:
 *   - Turning millis() into hours, minutes and seconds
 *   - Formatting fixed-width text with snprintf and "%02d"
 *   - Redrawing ONLY when something changed, to kill flicker
 *
 * A NOTE ON ACCURACY
 * This clock counts from the moment the board powered up, and it drifts
 * because it runs off the on-board ceramic resonator rather than a real
 * time source. It is a great exercise, not a wristwatch. For real
 * timekeeping add an RTC module such as a DS3231.
 *
 * Made with love by Lonely Binary — From Zeros to Heroes, One Bit at a Time.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Set these to the current time and the clock will start from there.
const unsigned long START_HOUR   = 9;
const unsigned long START_MINUTE = 30;
const unsigned long START_SECOND = 0;

unsigned long startOffset = 0;   // where we begin counting, in seconds
long lastDrawnSecond = -1;       // -1 means "nothing drawn yet"

char buffer[17];

void setup() {
  // ESP32-S3? Uncomment and set your GPIOs. Must come before lcd.init().
  // Wire.begin(8, 9);

  lcd.init();
  lcd.backlight();

  startOffset = START_HOUR * 3600UL + START_MINUTE * 60UL + START_SECOND;

  lcd.setCursor(0, 0);
  lcd.print("Lonely Binary");
}

void loop() {
  // millis() counts milliseconds since power-up; /1000 gives seconds.
  unsigned long totalSeconds = startOffset + (millis() / 1000UL);

  // Only redraw when the second actually ticks over. Without this guard
  // we would rewrite the screen thousands of times per second, which
  // both flickers and hammers the I2C bus for no reason.
  long currentSecond = (long)(totalSeconds % 60);
  if (currentSecond == lastDrawnSecond) {
    return;
  }
  lastDrawnSecond = currentSecond;

  unsigned long hours   = (totalSeconds / 3600UL) % 24UL;
  unsigned long minutes = (totalSeconds / 60UL) % 60UL;
  unsigned long seconds = totalSeconds % 60UL;

  // "%02lu" means: an unsigned long, at least 2 digits, padded with a
  // leading zero. That is what turns 9:5:3 into a tidy 09:05:03.
  snprintf(buffer, sizeof(buffer), "   %02lu:%02lu:%02lu   ",
           hours, minutes, seconds);
  lcd.setCursor(0, 1);
  lcd.print(buffer);

  // Every 10 seconds, swap the top row between a greeting and uptime.
  if (seconds % 10 == 0) {
    unsigned long upMinutes = millis() / 60000UL;
    lcd.setCursor(0, 0);
    if ((seconds / 10) % 2 == 0) {
      lcd.print("Lonely Binary   ");
    } else {
      snprintf(buffer, sizeof(buffer), "Up: %lu min      ", upMinutes);
      lcd.print(buffer);
    }
  }
}
