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
  if(isChanged) {
    switch(mode) {
      case 0:
        lcd_print("Enter PIN/RFID", pinDisplay);
        break;
      case 71:
        lcd_print("WiFi ip", wifi_localIp());
        delay(5000);
        changeMode(0);
        lcd_refresh();
        break;
      default:
        break;
    }
    isChanged = false;
  }
}

#endif
