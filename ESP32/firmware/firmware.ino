#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>
#include <SPI.h>
#include <MFRC522.h>
#include <ArduinoJson.h>
#include <WebServer.h>
#include <HTTPClient.h>

#include "Globals.h"
#include "Wifi.h"
#include "Lcd.h"
#include "Buzzer.h"
#include "Keypad.h"
#include "Rc522.h"
#include "Json.h"
#include "Http.h"

void setup()
{
  Serial.begin(9600);
  lcd_init();
  lcd_print("[INIT] WIFI", "##");
  Serial.println("[INIT] WIFI");
  delay(500);
  wifi_connect(WIFI_SSID, WIFI_PASSWORD);
  lcd_print("[ OK ] WIFI", "####");
  Serial.println("[ OK ] WIFI");
  delay(500);
  lcd_print("[INIT] BUZZER", "######");
  Serial.println("[INIT] BUZZER");
  delay(500);
  buzzer_init();
  lcd_print("[ OK ] BUZZER", "########");
  Serial.println("[ OK ] BUZZER");
  delay(500);
  lcd_print("[INIT] RFID", "##########");
  Serial.println("[INIT] RFID");
  delay(500);
  rc522_init();
  lcd_print("[ OK ] RFID", "############");
  Serial.println("[ OK ] RFID");
  delay(500);
  lcd_print("[INIT] HTTP", "##############");
  Serial.println("[INIT] HTTP");
  delay(500);
  http_init();
  lcd_print("[ OK ] HTTP", "################");
  Serial.println("[ OK ] HTTP");
  delay(500);
}


void loop()
{
  http_loop();
  
  keypad_read();
  
  rc522_read();

  lcd_refresh();
}
