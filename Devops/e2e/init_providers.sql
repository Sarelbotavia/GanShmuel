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
) ENGINE=MyISAM  AUTO_INCREMENT=10001 ;

DROP TABLE IF EXISTS `Products`;
CREATE TABLE `Products` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(45) NOT NULL,
  `rate` int(11) NOT NULL,
  `scope` varchar(45) NOT NULL DEFAULT 'ALL',
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `id_UNIQUE` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1000001 ;

DROP TABLE IF EXISTS `Trucks`;
CREATE TABLE IF NOT EXISTS `Trucks` (
  `truck_id` varchar(11) NOT NULL,
  `provider_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`truck_id`),
  FOREIGN KEY (`provider_id`) REFERENCES `Providers`(`provider_id`)
) ENGINE=MyISAM ;
-- -------------------------------------------------------------------------------
-- for Providers

INSERT INTO Providers (provider_name,payment_timing) VALUES ('test1','m');
INSERT INTO Providers (provider_name,payment_timing) VALUES ('Tapuzina','m');


-- for Rates
INSERT INTO Products (product_name,rate,scope) VALUES ('test2',2,'ALL');
INSERT INTO Products (product_name,rate,scope) VALUES ('Blood',122,'ALL');


-- for Trucks

INSERT INTO Trucks (truck_id,provider_id) VALUES ('test3',3);
INSERT INTO Trucks (truck_id,provider_id) VALUES ('777774',10004);

