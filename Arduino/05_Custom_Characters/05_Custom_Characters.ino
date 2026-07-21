/*
 * Lonely Binary 1602 I2C LCD — 05: Custom Characters
 * --------------------------------------------------
 * What you'll learn:
 *   - Designing your own 5x8 pixel characters
 *   - Loading them with createChar()
 *   - Printing them with lcd.write(byte(n))
 *
 * HOW IT WORKS
 * Every character cell is 5 pixels wide and 8 pixels tall. You describe
 * one as 8 rows of binary, where a 1 lights a pixel. Only the lowest 5
 * bits of each row are used, so B00000 to B11111. Written out in binary
 * you can literally see the picture in your source code:
 *
 *     B00000        . . . . .
 *     B01010        . # . # .
 *     B11111        # # # # #
 *     B11111        # # # # #     <- a heart
 *     B11111        # # # # #
 *     B01110        . # # # .
 *     B00100        . . # . .
 *     B00000        . . . . .
 *
 * TWO LIMITS TO REMEMBER
 *   1. You get 8 custom characters at a time, in slots 0 to 7.
 *   2. To print slot 0 use lcd.write(byte(0)). A plain lcd.write(0) is
 *      ambiguous to the compiler, and lcd.print(0) prints the digit "0".
 *
 * Made with love by Lonely Binary — From Zeros to Heroes, One Bit at a Time.
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

byte heart[8] = {
  B00000,
  B01010,
  B11111,
  B11111,
  B11111,
  B01110,
  B00100,
  B00000
};

byte bell[8] = {
  B00100,
  B01110,
  B01110,
  B01110,
  B11111,
  B00000,
  B00100,
  B00000
};

byte degree[8] = {
  B01100,
  B10010,
  B10010,
  B01100,
  B00000,
  B00000,
  B00000,
  B00000
};

byte arrow[8] = {
  B00000,
  B00100,
  B00110,
  B11111,
  B11111,
  B00110,
  B00100,
  B00000
};

byte battery[8] = {
  B01110,
  B11011,
  B10001,
  B10001,
  B11111,
  B11111,
  B11111,
  B00000
};

byte note[8] = {
  B00010,
  B00011,
  B00010,
  B00010,
  B01110,
  B11110,
  B01100,
  B00000
};

byte smiley[8] = {
  B00000,
  B01010,
  B01010,
  B00000,
  B10001,
  B01110,
  B00000,
  B00000
};

byte lock[8] = {
  B01110,
  B10001,
  B10001,
  B11111,
  B11011,
  B11011,
  B11111,
  B00000
};

void setup() {
  // ESP32-S3? Uncomment and set your GPIOs. Must come before lcd.init().
  // Wire.begin(8, 9);

  lcd.init();
  lcd.backlight();

  // Load each design into one of the 8 available slots.
  lcd.createChar(0, heart);
  lcd.createChar(1, bell);
  lcd.createChar(2, degree);
  lcd.createChar(3, arrow);
  lcd.createChar(4, battery);
  lcd.createChar(5, note);
  lcd.createChar(6, smiley);
  lcd.createChar(7, lock);

  lcd.setCursor(0, 0);
  lcd.print("Custom chars:");

  // Print all 8, separated by a space.
  lcd.setCursor(0, 1);
  for (byte slot = 0; slot < 8; slot++) {
    lcd.write(byte(slot));
    lcd.print(" ");
  }
}

void loop() {
  // Custom characters mix freely with ordinary text.
  delay(4000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("We ");
  lcd.write(byte(0));  // heart
  lcd.print(" Arduino");
  lcd.setCursor(0, 1);
  lcd.print("Temp: 24");
  lcd.write(byte(2));  // degree symbol
  lcd.print("C");

  delay(4000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Lonely Binary");
  lcd.setCursor(0, 1);
  for (byte slot = 0; slot < 8; slot++) {
    lcd.write(byte(slot));
    lcd.print(" ");
  }
}
