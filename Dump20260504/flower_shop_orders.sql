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
  `phone_code` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (5,1,30.00,'2026-04-06 21:12:59','4s_mk Senior','00962776114062','sssssssssss','cash','Pending',NULL),(6,1,80.00,'2026-04-07 07:04:32','mosaab','776114062','4356457678....mmmmmm','paypal','Pending',NULL),(7,1,60.00,'2026-04-07 07:52:16','fdgfdgfdgfd','fdgfdgfdgfd','fdgdfgfd','cash','Pending',NULL),(8,1,165.00,'2026-04-07 08:15:31','4s_mk Senior','+962 7 7820 9790','hhhh','cash','Pending',NULL),(10,1,130.00,'2026-04-08 22:04:04','4s_mk Senior','00962776114062','ddd','cash','Pending',NULL),(11,1,45.00,'2026-04-08 22:29:26','4s_mk Senior','00962776114062','wwwwwwww','cash','Pending',NULL),(12,1,45.00,'2026-04-08 22:40:01','4s_mk Senior','+962 7 7820 9790','ss','cash','Pending',NULL),(13,1,45.00,'2026-04-08 22:59:41','4s_mk Senior','00962776114062','xxxx','cash','Pending',NULL),(14,1,50.00,'2026-04-09 10:04:52','4s_mk Senior','+962 7 7820 9790','bbv','cash','Pending',NULL),(15,1,45.00,'2026-04-09 10:06:08','4s_mk Senior','00962776114062','ff','cash','Pending',NULL),(16,1,30.00,'2026-04-09 10:10:06','mohammad alshatti','00962776114062','اربددددددددددددددددددددددددددددد','card','Pending',NULL),(17,1,45.00,'2026-04-09 13:20:32','4s_mk Senior','00962776114062','اربدددددددددددددددددددددددددددددد','cash','Pending',NULL),(18,1,30.00,'2026-04-10 00:57:23',NULL,'00962776114062','sss','cash','Pending',NULL),(19,1,45.00,'2026-04-10 01:25:29','qqqq','00962776114062','we','cash','Pending',NULL),(20,1,45.00,'2026-04-10 01:29:47','qqqq','00962776114062','xc ','cash','Pending',NULL),(21,1,45.00,'2026-04-10 01:30:46','x xcvv','00962776114062','vvvv','paypal','Pending',NULL),(22,1,45.00,'2026-04-10 01:33:18','alshatti','00962776114062','sd','cash','Pending',NULL),(23,1,80.00,'2026-04-10 01:36:02','alshatti','00962776114062','cd','cash','Pending',NULL),(24,1,45.00,'2026-04-11 00:46:38','qqqq','00962776114062','ccc','cash','Pending',NULL),(25,1,137.00,'2026-04-11 16:12:10','qqqq','00962776114062','fffffffffff','paypal','Pending',NULL),(26,1,90.00,'2026-04-12 22:26:10','alshatti','+962 776114062','اربددد','cash','Pending',NULL),(27,1,45.00,'2026-04-12 22:47:58',NULL,NULL,NULL,'card','Completed',NULL),(28,1,63.00,'2026-04-13 10:45:16',NULL,NULL,NULL,'cash','Pending',NULL),(29,1,45.00,'2026-04-13 12:04:49',NULL,NULL,NULL,'paypal','Pending',NULL),(30,7,45.00,'2026-04-14 09:40:40',NULL,NULL,NULL,'cash','Pending',NULL),(31,7,50.00,'2026-04-14 09:41:02',NULL,NULL,NULL,'cash','Pending',NULL),(32,7,45.00,'2026-04-14 10:22:32',NULL,NULL,NULL,'cash','Pending',NULL),(33,1,45.00,'2026-04-20 18:41:50',NULL,NULL,NULL,'cash','Pending',NULL),(34,1,45.00,'2026-04-20 19:47:53',NULL,NULL,NULL,'cash','Pending',NULL),(35,1,45.00,'2026-04-20 19:54:53',NULL,NULL,NULL,'cash','Pending',NULL),(36,1,45.00,'2026-04-20 19:56:13',NULL,NULL,NULL,'cash','Pending',NULL),(37,1,50.00,'2026-04-21 21:34:58',NULL,NULL,NULL,'cash','Pending',NULL),(38,1,90.00,'2026-04-22 12:21:28',NULL,NULL,NULL,'cash','Pending',NULL),(39,7,45.00,'2026-04-22 12:44:14',NULL,NULL,NULL,'cash','Pending',NULL),(40,7,31.50,'2026-04-22 12:54:14',NULL,NULL,NULL,'cash','Pending',NULL),(41,7,50.00,'2026-04-22 12:55:21',NULL,NULL,NULL,'cash','Completed',NULL),(42,7,45.00,'2026-04-22 13:22:54',NULL,NULL,NULL,'cash','Completed',NULL),(43,7,30.00,'2026-04-22 13:26:37',NULL,NULL,NULL,'cash','Shipped',NULL),(46,1,105.00,'2026-04-25 19:20:34',NULL,NULL,NULL,'cash','Completed',NULL),(48,1,90.00,'2026-04-25 22:36:59',NULL,NULL,NULL,'paypal','Pending',NULL),(49,1,45.00,'2026-05-01 18:40:47',NULL,NULL,NULL,'cash','Pending',NULL),(51,1,45.00,'2026-05-01 20:09:45',NULL,NULL,NULL,'cash','Pending',NULL),(52,1,45.00,'2026-05-01 20:22:04',NULL,NULL,NULL,'cash','Cancelled',NULL),(53,1,92.00,'2026-05-02 10:20:19',NULL,NULL,NULL,'paypal','Shipped',NULL),(54,14,60.00,'2026-05-03 19:03:41',NULL,NULL,NULL,'paypal','Pending',NULL),(55,14,135.00,'2026-05-04 12:53:26',NULL,NULL,NULL,'cash','Pending',NULL),(56,14,50.00,'2026-05-04 12:54:09',NULL,NULL,NULL,'cash','Pending',NULL),(57,14,45.00,'2026-05-04 13:35:20','4s_mk Senior','+962 345567776575','  ss','cash','Pending',NULL),(58,14,45.00,'2026-05-04 14:06:41','4s_mk Senior','+966 84848757575','  ssdv','paypal','Pending',NULL),(59,14,25.00,'2026-05-04 14:09:33','4s_mk Senior','+962 345567776575','  ww','paypal','Pending',NULL);
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

-- Dump completed on 2026-05-04 18:59:22
