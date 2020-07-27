
CREATE DATABASE provirders_db CHARACTER SET utf8 COLLATE utf8_bin;
use providers_db;

CREATE TABLE providers(
   PROVIDER_ID   INT              NOT NULL AUTO_INCREMENT,
   NAME TEXT     NOT NULL,       
   PRIMARY KEY (NAME)
);

CREATE TABLE rates(
   PROD_ID   INT              NOT NULL,
   RATE TEXT     NOT NULL,  
   SCOPE_PROVID_ID   INT              NOT NULL,    
   PRIMARY KEY (PROD_ID)
);

CREATE TABLE trucks(
   LICENCE   INT              NOT NULL,
   PROVIDER_ID   INT              NOT NULL,       
   PRIMARY KEY (PROVIDER_ID)
);


