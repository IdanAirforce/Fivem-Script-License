CREATE DATABASE IF NOT EXISTS `license`
USE `license`;

CREATE TABLE IF NOT EXISTS `licenses` (
  `ip_address` varchar(255) DEFAULT NULL,
  `license_key` varchar(255) DEFAULT NULL,
  `resource_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;