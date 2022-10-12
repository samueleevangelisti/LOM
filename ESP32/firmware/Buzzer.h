#ifndef LOM_BUZZER_H
#define LOM_BUZZER_H

void buzzer_init() {
  ledcSetup(BUZZER_CHANNEL, BUZZER_FREQUENCY, BUZZER_RESOLUTION);
  ledcAttachPin(BUZZER_PIN, BUZZER_CHANNEL);
}

void buzzer_beep(int channel, int frequency, int duration) {
  ledcWriteTone(channel, frequency);
  delay(duration);
  ledcWriteTone(channel, 0);
}

void buzzer_beep() {
  buzzer_beep(BUZZER_CHANNEL, BUZZER_FREQUENCY, BUZZER_DELAY);
}

void buzzer_beep_short() {
  buzzer_beep(BUZZER_CHANNEL, BUZZER_FREQUENCY_SHORT, BUZZER_DELAY_SHORT);
}

void buzzer_beep_tree() {
  buzzer_beep(BUZZER_CHANNEL, BUZZER_FREQUENCY, BUZZER_DELAY);
  delay(500);
  buzzer_beep(BUZZER_CHANNEL, BUZZER_FREQUENCY, BUZZER_DELAY);
  delay(500);
  buzzer_beep(BUZZER_CHANNEL, BUZZER_FREQUENCY, BUZZER_DELAY);
}

#endif
