/*
 * Lonely Binary 1602 I2C LCD — 04: Scrolling Text
 * -----------------------------------------------
 * What you'll learn:
 *   - Why a 1602 can hold more text than it can show
 *   - Method 1: scroll a long message yourself, one window at a time
 *   - Method 2: scrollDisplayLeft() / scrollDisplayRight()
 *   - Method 3: autoscroll()
 *
 * THE KEY IDEA
 * A 1602 has 40 characters of memory per row, but only a 16 character
 * window is visible. Scrolling does not move your text — it slides the
 * window across the memory. Anything past column 39 is simply lost.
 *
 * Made with love by Lonely Binary — From Zeros to Heroes, One Bit at a Time.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// A message far longer than the 16 visible columns.
const char message[] = "From Zeros to Heroes, One Bit at a Time.   ";

const int LCD_WIDTH = 16;

void setup() {
  // ESP32-S3? Uncomment and set your GPIOs. Must come before lcd.init().
  // Wire.begin(8, 9);

  lcd.init();
  lcd.backlight();
}

void loop() {
  // ================================================================
  // METHOD 1 — scroll it yourself
  // We keep the text in a normal C string and print a different
  // 16-character slice of it each time. This is the most flexible
  // approach and works for text of any length.
  // ================================================================
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("1: manual window");

  int len = strlen(message);
  for (int start = 0; start <= len - LCD_WIDTH; start++) {
    lcd.setCursor(0, 1);
    for (int i = 0; i < LCD_WIDTH; i++) {
      lcd.print(message[start + i]);
    }
    delay(250);
  }
  delay(500);

  // ================================================================
  // METHOD 2 — let the LCD slide the window for you
  // scrollDisplayLeft() shifts the visible window one column at a
  // time. The text must already fit inside the 40 character row.
  // ================================================================
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("2: scrollDisplay");
  lcd.setCursor(0, 1);
  lcd.print("Lonely Binary");
  delay(1000);

  for (int i = 0; i < 16; i++) {
    lcd.scrollDisplayLeft();
    delay(200);
  }
  for (int i = 0; i < 16; i++) {
    lcd.scrollDisplayRight();  // and slide it back
    delay(200);
  }
  delay(500);

  // ================================================================
  // METHOD 3 — autoscroll
  // With autoscroll on, the display shifts itself every time you
  // print a character, so new text appears to push the old text
  // along. Handy for a right-aligned ticker.
  // ================================================================
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("3: autoscroll");

  lcd.setCursor(15, 1);  // park at the right edge
  lcd.autoscroll();
  for (int i = 0; i < 12; i++) {
    lcd.print(i % 10);
    delay(300);
  }
  lcd.noAutoscroll();  // ALWAYS turn it back off, or later prints misbehave
  delay(1000);
}
