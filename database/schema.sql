CREATE DATABASE housingmexico;
USE housingmexico;
CREATE TABLE `houses` (
  `id` int(9) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `link` varchar(255) NOT NULL,
  `zone` varchar(100) NOT NULL,
  `city_hall` varchar(100) NOT NULL,
  `latitude` decimal(10, 8),
  `longitude` decimal(11, 8),
  `price` int(12),
  `size` int(9),
  `built` int(9),
  `fullbathrooms` int(9),
  `halfbathrooms` int(9),
  `parking` int(9),
  `bedrooms` int(9),
  `years` int(9),
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
