CREATE TABLE Users (
  id BIGINT NOT NULL AUTO_INCREMENT,
  level INT NOT NULL,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  pin VARCHAR(255),
  rfid VARCHAR(255),
  PRIMARY KEY (id),
  UNIQUE (username),
  UNIQUE (pin),
  UNIQUE (rfid)
);
