#ifndef LOM_RC522_H
#define LOM_RC522_H

void rc522_init() {
  SPI.begin();
  rc522.PCD_Init();
}

void rc522_read() {
  if(rc522.PICC_IsNewCardPresent() && rc522.PICC_ReadCardSerial()) {
    rfid = "";
    for(int i = 0; i < rc522.uid.size; i++) {
      rfidByte = "0" + String(rc522.uid.uidByte[i], HEX);
      rfid += rfidByte.substring(rfidByte.length() - 2);
    }
    rc522.PICC_HaltA();
    rc522.PCD_StopCrypto1();
    buzzer_beep_short();
    switch(mode) {
      case 0:
        changeMode(82);
        lcd_refresh();
        if(http_post("actionRfid", String("{")
          + String("\"rfid\":\"") + rfid + String("\"")
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
      case 11:
        changeMode(12);
        lcd_refresh();
        break;
      default:
        break;  
    }
  }
}

#endif
