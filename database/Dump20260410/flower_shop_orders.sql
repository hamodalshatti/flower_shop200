-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: flower_shop
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Recipient_name` varchar(100) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `address` text,
  `payment_method` varchar(50) DEFAULT NULL,
  `status` varchar(30) DEFAULT 'Pending',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,295.00,'2026-04-01 20:28:55','4s_mk Senior','00962776114062','سسسسسسسسسسسسسسس','paypal','Pending'),(2,1,295.00,'2026-04-01 20:29:08','4s_mk Senior','00962776114062','سسسسسسسسسسسسسسس','paypal','Pending'),(3,1,295.00,'2026-04-01 20:31:43','4s_mk Senior','00962776114062','سسسسسسسسسسسسسسس','paypal','Pending'),(4,1,30.00,'2026-04-04 16:16:58','4s_mk Senior','00962776114062','dddddddd','cash','Pending'),(5,1,30.00,'2026-04-06 21:12:59','4s_mk Senior','00962776114062','sssssssssss','cash','Pending'),(6,1,80.00,'2026-04-07 07:04:32','mosaab','776114062','4356457678....mmmmmm','paypal','Pending'),(7,1,60.00,'2026-04-07 07:52:16','fdgfdgfdgfd','fdgfdgfdgfd','fdgdfgfd','cash','Pending'),(8,1,165.00,'2026-04-07 08:15:31','4s_mk Senior','+962 7 7820 9790','hhhh','cash','Pending'),(9,1,260.00,'2026-04-08 18:21:44','4s_mk Senior','00962776114062','eddx','cash','Pending'),(10,1,130.00,'2026-04-08 22:04:04','4s_mk Senior','00962776114062','ddd','cash','Pending'),(11,1,45.00,'2026-04-08 22:29:26','4s_mk Senior','00962776114062','wwwwwwww','cash','Pending'),(12,1,45.00,'2026-04-08 22:40:01','4s_mk Senior','+962 7 7820 9790','ss','cash','Pending'),(13,1,45.00,'2026-04-08 22:59:41','4s_mk Senior','00962776114062','xxxx','cash','Pending'),(14,1,50.00,'2026-04-09 10:04:52','4s_mk Senior','+962 7 7820 9790','bbv','cash','Pending'),(15,1,45.00,'2026-04-09 10:06:08','4s_mk Senior','00962776114062','ff','cash','Pending'),(16,1,30.00,'2026-04-09 10:10:06','mohammad alshatti','00962776114062','اربددددددددددددددددددددددددددددد','card','Pending'),(17,1,45.00,'2026-04-09 13:20:32','4s_mk Senior','00962776114062','اربدددددددددددددددددددددددددددددد','cash','Pending'),(18,1,30.00,'2026-04-10 00:57:23',NULL,'00962776114062','sss','cash','Pending'),(19,1,45.00,'2026-04-10 01:25:29','qqqq','00962776114062','we','cash','Pending'),(20,1,45.00,'2026-04-10 01:29:47','qqqq','00962776114062','xc ','cash','Pending'),(21,1,45.00,'2026-04-10 01:30:46','x xcvv','00962776114062','vvvv','paypal','Pending'),(22,1,45.00,'2026-04-10 01:33:18','alshatti','00962776114062','sd','cash','Pending'),(23,1,80.00,'2026-04-10 01:36:02','alshatti','00962776114062','cd','cash','Pending');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-10 17:38:59
