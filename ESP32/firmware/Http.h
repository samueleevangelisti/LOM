#ifndef LOM_HTTP_H
#define LOM_HTTP_H

WebServer http_web_server(HTTP_PORT);
HTTPClient http_client;

void http_handler() {
  switch(http_web_server.method()) {
      case HTTP_GET:
        http_web_server.send(200, "application/json", String("{")
          + String("\"gatewayUrl\":\"") + HTTP_GATEWAY_URL + String("\"")
        + String("}"));
        break;
      case HTTP_PATCH:
        json_deserialize(http_web_server.arg(0));
        if(json_deserialization_error) {
        http_web_server.send(200, "application/json", String("{")
          + String("\"success\":false")
        + String("}"));
      } else {
        Serial.println(json_document["gatewayUrl"]);
        Serial.println(json_document["action"]);
      }
        break;
      default:
        break;
  }
}

void http_init() {
  http_web_server.on("/", http_handler);
}

void http_loop() {
  http_web_server.handleClient();
}

#endif
