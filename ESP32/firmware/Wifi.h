#ifndef LOM_WIFI_H
#define LOM_WIFI_H

void wifi_connect(String ssid, String password) {
  WiFi.disconnect();
  WiFi.begin(ssid.c_str(), password.c_str());
  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
}

String wifi_localIp() {
  return WiFi.localIP().toString();
}

#endif
