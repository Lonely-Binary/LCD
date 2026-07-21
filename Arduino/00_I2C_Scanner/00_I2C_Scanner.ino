/*
 * Lonely Binary — I2C Scanner
 * ---------------------------
 * Scans the I2C bus and prints the address of every device that responds.
 * Use it to find the address of your 1602 I2C LCD (usually 0x27, sometimes 0x3F).
 *
 * Works on:
 *   - Arduino UNO / Nano / Mega  -> fixed SDA/SCL pins (UNO: A4 = SDA, A5 = SCL)
 *   - ESP32-S3 / ESP32 / ESP32-C3 -> any free GPIO, set below
 *
 * ⚠️ 3.3 V boards (ESP32-S3, Pico, ...): the LCD runs at 5 V and pulls SDA/SCL
 *    up to 5 V. Use a logic level converter on SDA/SCL to protect your MCU.
 *
 * Made with love by Lonely Binary — From Zeros to Heroes, One Bit at a Time.
 */

#include <Wire.h>

#if defined(ESP32)
// ---- ESP32 / ESP32-S3: pick ANY two free GPIOs ----
#define I2C_SDA_PIN 8
#define I2C_SCL_PIN 9
#endif

// I2C bus speed. 100000 (100 kHz) is the safest for character LCDs.
#define I2C_FREQUENCY 100000UL

void setup() {
#if defined(ESP32)
  Serial.begin(115200);
#else
  Serial.begin(9600);
#endif

  while (!Serial) {
    ; // wait for the USB serial port (needed on native-USB boards)
  }
  delay(500);

#if defined(ESP32)
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN, I2C_FREQUENCY);
  Serial.print("ESP32 I2C on SDA=GPIO");
  Serial.print(I2C_SDA_PIN);
  Serial.print(", SCL=GPIO");
  Serial.println(I2C_SCL_PIN);
#else
  Wire.begin();                  // UNO: SDA = A4, SCL = A5
  Wire.setClock(I2C_FREQUENCY);
  Serial.println("AVR I2C on the board's default SDA/SCL pins");
#endif

  Serial.println("Lonely Binary I2C Scanner");
  Serial.println("-------------------------");
}

void loop() {
  byte found = 0;

  Serial.println("Scanning...");

  for (byte address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("  Device found at 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.print(address, HEX);

      if (address == 0x27 || address == 0x3F) {
        Serial.print("  <- looks like a 1602 I2C LCD");
      }
      Serial.println();
      found++;
    } else if (error == 4) {
      Serial.print("  Unknown error at 0x");
      if (address < 16) {
        Serial.print("0");
      }
      Serial.println(address, HEX);
    }
  }

  if (found == 0) {
    Serial.println("  No I2C devices found — check VCC, GND, SDA and SCL wiring.");
  } else {
    Serial.print("  Done. ");
    Serial.print(found);
    Serial.println(" device(s) found.");
  }

  Serial.println();
  delay(5000);
}
