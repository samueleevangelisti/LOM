#ifndef LOM_JSON_H
#define LOM_JSON_H

void json_deserialize(String json_string) {
  json_deserialization_error = deserializeJson(json_document, json_string);
}

#endif
