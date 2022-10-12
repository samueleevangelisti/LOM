#ifndef LOM_KEYPAD_H
#define LOM_KEYPAD_H

void keypad_read() {
  pinKey = keypad.getKey();
  if(pinKey) {
    buzzer_beep_short();
    switch(pinKey) {
      case '#':
        changeMode(71);
        lcd_refresh();
        delay(5000);
        changeMode(0);
        lcd_refresh();
        break;
      case 'A':
        changeMode(11);
        lcd_refresh();
        break;
      case 'C':
        changeMode(0);
        lcd_refresh();
        break;
      case 'D':
        changeMode(21);
        lcd_refresh();
        break;
      case 'B':
      case '*':
        break;
      default:
        pin += pinKey;
        pinDisplay += '*';
        lcd_refresh();
        if(pin.length() == pinLength) {
          switch(mode) {
            case 0:
              changeMode(81);
              lcd_refresh();
              if(http_post("actionPin", String("{")
                + String("\"pin\":\"") + pin + String("\"")
              + String("}"))) {
                if((bool) json_document["success"]) {
                  changeMode(9);
                  lcd_refresh();
                  buzzer_beep();
                  changeMode(0);
                  lcd_refresh();
                } else {
                  changeMode(99);
                  lcd_refresh();
                  buzzer_beep_tree();
                  changeMode(0);
                  lcd_refresh();
                }
              } else {
                changeMode(4);
                lcd_refresh();
                buzzer_beep_tree();
                changeMode(0);
                lcd_refresh();
              }
              break;
            case 12:
              changeMode(81);
              lcd_refresh();
              if(http_post("addRfid", String("{")
                + String("\"pin\":\"" + pin + String("\","))
                + String("\"rfid\":\"" + rfid + String("\""))
              + String("}"))) {
                if((bool) json_document["success"]) {
                  changeMode(3);
                  lcd_refresh();
                  buzzer_beep();
                  changeMode(0);
                  lcd_refresh();
                } else {
                  changeMode(4);
                  lcd_refresh();
                  buzzer_beep_tree();
                  changeMode(0);
                  lcd_refresh();
                }
              } else {
                changeMode(4);
                lcd_refresh();
                buzzer_beep_tree();
                changeMode(0);
                lcd_refresh();
              }
              break;
            case 21:
              changeMode(81);
              lcd_refresh();
              if(http_post("deleteRfid", String("{")
                + String("\"pin\":\"" + pin + String("\""))
              + String("}"))) {
                if((bool) json_document["success"]) {
                  changeMode(3);
                  lcd_refresh();
                  buzzer_beep();
                  changeMode(0);
                  lcd_refresh();
                } else {
                  changeMode(4);
                  lcd_refresh();
                  buzzer_beep_tree();
                  changeMode(0);
                  lcd_refresh();
                }
              } else {
                changeMode(4);
                lcd_refresh();
                buzzer_beep_tree();
                changeMode(0);
                lcd_refresh();
              }
              break;
            default:
              break;
          }
        }
        break;
    }
  }
}

#endif
