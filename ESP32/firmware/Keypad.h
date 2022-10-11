#ifndef LOM_KEYPAD_H
#define LOM_KEYPAD_H

void keypad_read() {
  pinKey = keypad.getKey();
  if(pinKey) {
    switch(pinKey) {
      case '#':
        isChanged = true;
        changeMode(71);
        break;
      default:
        pin += pinKey;
        pinDisplay += '*';
        if(pin.length() == pinLength) {
          // TODODSE in questo punto bisogna comunicare lo sblocco
          changeMode(1);
        }
        break;
    }
    isChanged = true;
    buzzer_beep_short();
  }
}

#endif
