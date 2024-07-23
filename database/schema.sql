# CREATE DATABASE
CREATE DATABASE housingmexico;
use housingmexico
# CREATE TABLE
CREATE TABLE `houses` (
  `id` int(9) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `link` varchar(255) NOT NULL,
  `zone` varchar(100) NOT NULL,
  `city_hall` varchar(100) NOT NULL,
  `latitude` DOUBLE,
  `longitude` DOUBLE,
  `price` int(12) unsigned,
  `size` int(9) unsigned,
  `built` int(9) unsigned,
  `fullbathrooms` int(9) unsigned,
  `halfbathrooms` int(9) unsigned,
  `parking` int(9) unsigned,
  `bedrooms` int(9) unsigned,
  `years` int(9) unsigned,
  `description` text(550) unsigned,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
