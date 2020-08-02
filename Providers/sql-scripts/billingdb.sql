--
-- Database: `billdb`
--

CREATE DATABASE IF NOT EXISTS `billdb`;
USE `billdb`;

-- --------------------------------------------------------------------------------

-- Table structure

DROP TABLE IF EXISTS `Providers`;
CREATE TABLE IF NOT EXISTS `Providers` (
  `provider_id` int(11) NOT NULL AUTO_INCREMENT,
  `provider_name` varchar(255) DEFAULT NULL,
  `payment_timing` varchar(1) DEFAULT 'd',
  PRIMARY KEY (`provider_id`)
  UNIQUE KEY (`provider_name`)
) ENGINE=MyISAM  AUTO_INCREMENT=10001 ;

DROP TABLE IF EXISTS `Products`;
CREATE TABLE `Products` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(45) NOT NULL,
  `rate` int(11) NOT NULL,
  `scope` varchar(45) NOT NULL DEFAULT 'ALL',
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `id_UNIQUE` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;

DROP TABLE IF EXISTS `Trucks`;
CREATE TABLE IF NOT EXISTS `Trucks` (
  `truck_id` varchar(11) NOT NULL,
  `provider_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`truck_id`),
  UNIQUE KEY `id_UNIQUE` (`truck_id`)
  FOREIGN KEY (`provider_id`) REFERENCES `Providers`(`provider_id`)
) ENGINE=MyISAM ;
-- -------------------------------------------------------------------------------
-- for Providers

INSERT INTO Providers (provider_name,payment_timing) VALUES ('Tapuzina','m');
INSERT INTO Providers (provider_name,payment_timing) VALUES ('Herut','w');
INSERT INTO Providers (provider_name,payment_timing) VALUES ('Hasamba','m');
INSERT INTO Providers (provider_name,payment_timing) VALUES ('Hazorea','w');
INSERT INTO Providers (provider_name,payment_timing) VALUES ('Yonatan','m');
INSERT INTO Providers (provider_name) VALUES ('HadNes');
INSERT INTO Providers (provider_name) VALUES ('Mishmeret');
INSERT INTO Providers (provider_name) VALUES ('KfarHess');


-- for Rates
INSERT INTO Products (product_name,rate,scope) VALUES ('Blood',122,'ALL');
INSERT INTO Products (product_name,rate,scope) VALUES ('Mandarin',103,'ALL');
INSERT INTO Products (product_name,rate,scope) VALUES ('Navel',97,'ALL');
INSERT INTO Products (product_name,rate,scope) VALUES ('Blood',102,'10004');
INSERT INTO Products (product_name,rate,scope) VALUES ('Clementine',100,'ALL');
INSERT INTO Products (product_name,rate,scope) VALUES ('Tangerine',80,'ALL');
INSERT INTO Products (product_name,rate,scope) VALUES ('Clementine',90,'10001');
INSERT INTO Products (product_name,rate,scope) VALUES ('Blueberries',158,'ALL');
INSERT INTO Products (product_name,rate,scope) VALUES ('Grapefruit',97,'ALL');
INSERT INTO Products (product_name,rate,scope) VALUES ('Grapefruit',93,'10008');
INSERT INTO Products (product_name,rate,scope) VALUES ('Mango',120,'ALL');
INSERT INTO Products (product_name,rate,scope) VALUES ('Mango',111,'10006');
INSERT INTO Products (product_name,rate,scope) VALUES ('Mango',109,'10002');
INSERT INTO Products (product_name,rate,scope) VALUES ('Pomegranate',143,'ALL');

-- for Trucks

INSERT INTO Trucks (truck_id,provider_id) VALUES ('777774',10004);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('666664',10004);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('998884',10004);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('663215',10005);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('123655',10005);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('123456',10006);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('121216',10006);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('234512',10002);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('211222',10002);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('134221',10001);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('123221',10001);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('666663',10003);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('922883',10003);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('644418',10008);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('123657',10007);
