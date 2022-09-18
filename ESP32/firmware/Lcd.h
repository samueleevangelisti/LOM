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
  if(is_changed) {
    switch(mode) {
      case 0:
        lcd_print("PIN:", pinDisplay);
        break;
      case 1:
        lcd_print("RFID:", rfid);
        break;
      default:
        break;
    }
    is_changed = false;
  }
}

#endif
