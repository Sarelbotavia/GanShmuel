
CREATE DATABASE  IF NOT EXISTS `weight_db`;
USE `weight_db`;


DROP TABLE IF EXISTS `containers`;
CREATE TABLE `containers` (
  `id` varchar(45) NOT NULL,
  `weight` float NOT NULL,
  `unit` enum('kg','lbs') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(45) NOT NULL,
  `rate` int(11) NOT NULL,
  `scope` varchar(45) NOT NULL DEFAULT 'ALL',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `trucks`;
CREATE TABLE `trucks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `truckid` varchar(45) NOT NULL,
  `providerid` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `unit` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `containers_has_sessions`;
DROP TABLE IF EXISTS `sessions`;
CREATE TABLE `sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `direction` enum('in','out','none') DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `bruto` float DEFAULT NULL,
  `neto` float DEFAULT NULL,
  `trucks_id` int(11) DEFAULT NULL,
  `products_id` int(11) DEFAULT NULL,
  `containers_id` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `containers_has_sessions` (
  `containers_id` varchar(45) NOT NULL,
  `sessions_id` int(11) NOT NULL,
  PRIMARY KEY (`containers_id`,`sessions_id`),
  KEY `fk_containers_has_sessions_sessions1_idx` (`sessions_id`),
  KEY `fk_containers_has_sessions_containers1_idx` (`containers_id`),
  CONSTRAINT `fk_containers_has_sessions_containers1` FOREIGN KEY (`containers_id`) REFERENCES `containers` (`id`),
  CONSTRAINT `fk_containers_has_sessions_sessions1` FOREIGN KEY (`sessions_id`) REFERENCES `sessions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO containers (id,weight,unit) VALUES ('K-8263',666,'lbs');
INSERT INTO containers (id,weight,unit) VALUES ('K-7854',854,'lbs');
INSERT INTO containers (id,weight,unit) VALUES ('K-6523',741,'kg');
INSERT INTO containers (id,weight,unit) VALUES ('K-2369',120,'kg');
INSERT INTO containers (id,weight,unit) VALUES ('K-7845',999,'lbs');

INSERT INTO containers (id,weight,unit) VALUES ('K-1234',123,'kg');


INSERT INTO products (product_name,rate,scope) VALUES ('Blood',122,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Mandarin',103,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Navel',97,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Blood',102,'1');
INSERT INTO products (product_name,rate,scope) VALUES ('Clementine',100,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Tangerine',80,'ALL');
INSERT INTO products (product_name,rate,scope) VALUES ('Clementine',90,'2');

INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('77777',2,666,'lbs');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('66666',2,120,'kg');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('99888',1,999,'lbs');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('66321',3,741,'kg');
INSERT INTO trucks (truckid,providerid,weight,unit) VALUES ('12365',4,854,'lbs');



INSERT INTO sessions (direction, date, bruto, neto, trucks_id, products_id) VALUES ('in', '20181218181512', 999, 800, 77777, 2);
INSERT INTO sessions (direction, date, bruto, neto, trucks_id, products_id) VALUES ('in', '20181221141414', 800, 500, 77777, 1);
INSERT INTO sessions (direction, date, bruto, neto, trucks_id, products_id) VALUES ('in', '20181220151515', 700, 600, 77777, 3);
INSERT INTO sessions (direction, date, bruto, neto, trucks_id, products_id) VALUES ('in', '20161218181512', 120, 100, 99888, 1);
INSERT INTO sessions (direction, date, bruto, neto, trucks_id, products_id) VALUES ('out', '20170920102017', 741, 650, 12365, 3);

INSERT INTO containers_has_sessions (containers_id, sessions_id) VALUES ('K-8263',1);
INSERT INTO containers_has_sessions (containers_id, sessions_id) VALUES ('K-7854',2);
INSERT INTO containers_has_sessions (containers_id, sessions_id) VALUES ('K-6523',3);
INSERT INTO containers_has_sessions (containers_id, sessions_id) VALUES ('K-2369',1);
INSERT INTO containers_has_sessions (containers_id, sessions_id) VALUES ('K-7845',2);
INSERT INTO containers_has_sessions (containers_id, sessions_id) VALUES ('K-1234',3);

