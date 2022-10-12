#ifndef LOM_LCD_H
#define LOM_LCD_H

void lcd_init() {
  lcd.init();
  lcd.backlight();
}

void lcd_print(String line1, String line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

void lcd_refresh() {
  switch(mode) {
    case 0:
      lcd_print("Enter PIN/RFID", pinDisplay);
      break;
    case 11:
      lcd_print("Enter RFID   [A]", "");
      break;
    case 12:
      lcd_print("Enter PIN    [A]", pinDisplay);
      break;
    case 21:
      lcd_print("Enter PIN    [D]", pinDisplay);
      break;
    case 3:
      lcd_print("Done", "");
      break;
    case 4:
      lcd_print("Error", "");
      break;
    case 71:
      lcd_print("WiFi IP", wifi_localIp());
      break;
    case 81:
      lcd_print("Checking PIN", "");
      break;
    case 82:
      lcd_print("Checking RFID", "");
      break;
    case 9:
      lcd_print("Access granted", "");
      break;
    case 99:
      lcd_print("Access denied", "");
      break;
    default:
      break;
  }
}

#endif
