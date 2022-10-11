#ifndef LOM_GLOBALS_H
#define LOM_GLOBALS_H

const byte LCD_ADDRESS = 0x27;
const byte LCD_COLUMNS = 16;
const byte LCD_ROWS = 2;
LiquidCrystal_I2C lcd(LCD_ADDRESS, 16, 2);

const String WIFI_SSID = "TIM-32867173";
const String WIFI_PASSWORD = "rbRWGmRFlmsXN3GulwBXByaG";

const int BUZZER_FREQUENCY = 1500;
const int BUZZER_FREQUENCY_SHORT = 1000;
const int BUZZER_DELAY = 500;
const int BUZZER_DELAY_SHORT = 50;
const int BUZZER_CHANNEL = 0;
const int BUZZER_RESOLUTION = 8;
const int BUZZER_PIN = 2;

const byte KEYPAD_ROWS = 4;
const byte KEYPAD_COLUMNS = 4;
byte KEYPAD_ROW_PINS[KEYPAD_ROWS] = {32, 33, 25, 26};
byte KEYPAD_COLUMN_PINS[KEYPAD_COLUMNS] = {27, 14, 12, 13};
const char KEYPAD_KEYS[KEYPAD_ROWS][KEYPAD_COLUMNS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
Keypad keypad = Keypad(makeKeymap(KEYPAD_KEYS), KEYPAD_ROW_PINS, KEYPAD_COLUMN_PINS, KEYPAD_ROWS, KEYPAD_COLUMNS);

const int RC522_SS_PIN = 5;
const int RC522_RST_PIN = 4;
MFRC522 rc522{RC522_SS_PIN, RC522_RST_PIN};

int HTTP_PORT = 80;
String HTTP_GATEWAY_URL = String();

bool isSerial = false;
String serialInput = String();
String serialInputKey = String();
String serialInputValue = String();
WiFiClient wifi_client;
StaticJsonDocument<513> json_document;
DeserializationError json_deserialization_error;
int mode = 0; // 0: input, 1: update, 7: status, 8: checking, 9: done
bool isChanged = true;
bool isBeep = false;

int pinLength = 8;
int adminPinLength = 8;
char pinKey;
String pin = String();
String pinDisplay = String();

String rfidByte = String();
String rfid = String();

void changeMode(int newMode) {
  mode = newMode;
  switch(mode) {
    case 0: // inserimento input
      pin = "";
      pinDisplay = "";
      rfidByte = "";
      rfid = "";
      break;
    case 71: // wifi ip
      break;
    default:
      break;
  }
}

#endif
