# CREATE DATABASE
CREATE DATABASE HousingMexico;

# CREATE TABLE
CREATE TABLE `houses` (
  `id` int(9) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `link` varchar(255) NOT NULL,
  `size` int(9) unsigned NOT NULL,
  `built` int(9) unsigned NOT NULL,
  `fullbathrooms` int(9) unsigned NOT NULL,
  `halfbathrooms` int(9) unsigned NOT NULL,
  `parking` int(9) unsigned NOT NULL,
  `bedrooms` int(9) unsigned NOT NULL,
  `years` int(9) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;