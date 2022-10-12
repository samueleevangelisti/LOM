#ifndef LOM_HTTP_H
#define LOM_HTTP_H

void http_handler() {
  switch(http_webServer.method()) {
    case HTTP_GET:
      http_webServer.send(200, "application/json", String("{")
        + String("\"gatewayUrl\":\"") + HTTP_GATEWAY_URL + String("\"")
      + String("}"));
      break;
    case HTTP_PATCH:
      json_deserialize(http_webServer.arg(0));
      if(json_deserializationError) {
        http_webServer.send(200, "application/json", String("{")
          + String("\"success\":false,")
          + String("\"error\":\"") + json_deserializationError.c_str() + String("\"")
        + String("}"));
      } else {
        if(json_document["gatewayUrl"]) {
          HTTP_GATEWAY_URL = String((const char *) json_document["gatewayUrl"]);
        }
        if(json_document["action"]) {
          changeMode(9);
          lcd_refresh();
          buzzer_beep();
          changeMode(0);
          lcd_refresh();
        }
        http_webServer.send(200, "application/json", String("{")
          + String("\"success\":true")
        + String("}"));
      }
      break;
    default:
      break;
  }
}

void http_init() {
  http_webServer.on("/", http_handler);
  http_webServer.begin();
}

void http_loop() {
  http_webServer.handleClient();
}

bool http_post(String method, String json) {
  http_client.begin(HTTP_GATEWAY_URL + String("/") + method);
  http_client.addHeader("Content-type", "application/json");
  http_responseCode = http_client.POST(json);
  if(http_responseCode == 200) {
    json_deserialize(http_client.getString());
    http_client.end();
    return true;
  } else {
    http_client.end();
    return false;
  }
}

#endif
