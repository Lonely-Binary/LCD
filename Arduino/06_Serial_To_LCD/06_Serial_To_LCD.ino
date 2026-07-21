/*
 * Lonely Binary 1602 I2C LCD — 06: Type on Your Computer, Show on the LCD
 * -----------------------------------------------------------------------
 * What you'll learn:
 *   - Reading a line of text from the Serial Monitor
 *   - Displaying it on the LCD, wrapped across both rows
 *   - Clearing stale text properly
 *
 * HOW TO USE
 *   1. Upload the sketch
 *   2. Open Tools -> Serial Monitor and set the baud rate to 9600
 *   3. Make sure the line ending box says "Newline"
 *   4. Type something, press Enter, and watch it appear on the LCD
 *
 * Text longer than 32 characters is truncated — that is all a 1602 can
 * show at once (16 columns x 2 rows).
 *
 * Made with love by Lonely Binary — From Zeros to Heroes, One Bit at a Time.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int LCD_WIDTH = 16;
const int LCD_ROWS = 2;

void setup() {
  Serial.begin(9600);

  // ESP32-S3? Uncomment and set your GPIOs. Must come before lcd.init().
  // Wire.begin(8, 9);

  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Type in Serial");
  lcd.setCursor(0, 1);
  lcd.print("Monitor @9600");

  Serial.println("Ready — type a message and press Enter.");
}

void loop() {
  // Nothing to do until the user sends something.
  if (!Serial.available()) {
    return;
  }

  // Read everything up to the Enter key.
  String text = Serial.readStringUntil('\n');
  text.trim();  // drop stray spaces and the carriage return

  if (text.length() == 0) {
    return;
  }

  Serial.print("Showing: ");
  Serial.println(text);

  // clear() is the right tool here: the new message may be shorter than
  // the old one, and we want no leftovers anywhere on the screen.
  lcd.clear();

  // Fill row 0 with the first 16 characters, row 1 with the next 16.
  for (int row = 0; row < LCD_ROWS; row++) {
    int start = row * LCD_WIDTH;
    if (start >= (int)text.length()) {
      break;  // message was short enough to fit on one row
    }
    lcd.setCursor(0, row);
    lcd.print(text.substring(start, start + LCD_WIDTH));
  }
}
