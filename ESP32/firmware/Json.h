#ifndef LOM_JSON_H
#define LOM_JSON_H

void json_deserialize(String jsonString) {
  json_deserializationError = deserializeJson(json_document, jsonString);
}

#endif
