#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>
#include <SPI.h>
#include <MFRC522.h>

#include "Globals.h"
#include "Lcd.h"
#include "Buzzer.h"
#include "Keypad.h"
#include "Rc522.h"

void setup()
{
  Serial.begin(9600);
  lcd_init();
  lcd_print("[ OK ] LCD", "##");
  delay(500);
  lcd_print("[INIT] BUZZER", "####");
  delay(500);
  buzzer_init();
  lcd_print("[ OK ] BUZZER", "######");
  delay(500);
  lcd_print("[INIT] RFID", "########");
  delay(500);
  rc522_init();
  lcd_print("[ OK ] RFID", "################");
  delay(500);
}


void loop()
{
  keypad_read();
  
  rc522_read();

  lcd_refresh();

  buzzer_beep();
}
