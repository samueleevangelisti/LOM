#ifndef LOM_KEYPAD_H
#define LOM_KEYPAD_H

void keypad_read() {
  pinKey = keypad.getKey();
  if(pinKey) {
    changeMode(0);
    pin.concat(pinKey);
    pinDisplay.concat('*');
    if(pin.length() == pinLength) {
      pin = "";
      pinDisplay = "";
      is_beep = true;
    }
    is_changed = true;
    buzzer_beep_short();
  }
}

#endif
