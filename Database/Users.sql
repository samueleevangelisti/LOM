CREATE TABLE Users (
  id BIGINT NOT NULL AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  pin VARCHAR(255),
  rfid VARCHAR(255),
  level INT NOT NULL,
  active BOOLEAN NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (username),
  UNIQUE (pin),
  UNIQUE (rfid)
);
