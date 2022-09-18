#ifndef LOM_RC522_H
#define LOM_RC522_H

void rc522_init() {
  SPI.begin();
  rc522.PCD_Init();
}

void rc522_read() {
  if(rc522.PICC_IsNewCardPresent() && rc522.PICC_ReadCardSerial()) {
    changeMode(1);
    rfid = "";
    for(int i = 0; i < rc522.uid.size; i++) {
      rfidByte = "0" + String(rc522.uid.uidByte[i], HEX);
      rfid += rfidByte.substring(rfidByte.length() - 2);
    }
    rc522.PICC_HaltA();
    rc522.PCD_StopCrypto1();
    is_changed = true;
    is_beep = true;
  }
}

#endif
