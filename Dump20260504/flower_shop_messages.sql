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
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `message` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `subject` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,'ةحمد','ssmk2060@gmail.com','السلم عليكم ','2026-03-16 02:58:54',NULL),(2,'4s_mk Senior','ssmk2060@gmail.com','مصعب محترم جداؤؤؤؤ','2026-03-25 19:25:50',NULL),(3,'4s_mk Senior','ssmk2060@gmail.com','ggggggggggggggg','2026-04-06 07:25:59',NULL),(4,'4s_mk Senior','ssmk2060@gmail.com','asxsad','2026-04-06 15:06:05',NULL),(5,'4s_mk Senior','ssmk2060@gmail.com','ggggggggg','2026-04-07 08:11:32',NULL),(6,'4s_mk Senior','ssmk2060@gmail.com','ddddd','2026-04-12 19:26:29',NULL),(7,'4s_mk Senior','ssmk2060@gmail.com','jkhkgf','2026-04-14 09:55:19',NULL),(8,'4s_mk Senior','ssmk2060@gmail.com','dddd','2026-04-22 10:38:39',NULL),(9,'4s_mk Senior','ssmk2060@gmail.com','dddd','2026-04-22 10:39:06',NULL),(10,'4s_mk Senior','ssmk2060@gmail.com','sss','2026-04-22 10:39:27',NULL),(11,'mohammad','ssmk2060@gmail.com','halw ','2026-04-28 17:38:20',NULL),(12,'mohammad','ssmk2060@gmail.com','halw ','2026-04-28 17:47:31',NULL),(13,'mohammad','ssmk2060@gmail.com','halw ','2026-04-28 17:47:38',NULL),(14,'mohammad','ssmk2060@gmail.com','halw ','2026-04-28 17:49:16',NULL),(15,'mohammad','ssmk2060@gmail.com','halw ','2026-04-28 17:49:20',NULL),(16,'mohammad','ssmk2060@gmail.com','halw ','2026-04-28 17:50:36',NULL),(17,'4s_mk Senior','ssmk2060@gmail.com','mohamadddddddddddddddddd','2026-05-01 19:53:25',NULL),(18,'4s_mk Senior','ssmk2060@gmail.com','ddddd','2026-05-03 19:48:42',NULL),(19,'4s_mk Senior','ssmk2060@gmail.com','ddddd','2026-05-03 19:50:41',NULL),(20,'4s_mk Senior','ssmk2060@gmail.com','welcom musaab','2026-05-04 14:27:42',NULL),(21,'4s_mk Senior','ssmk2060@gmail.com','cccccccccccccccccccc','2026-05-04 14:31:55',NULL),(22,'aliiiiiiiiiiiiiiii','ali@gmail.com','PYTHON','2026-05-04 14:41:45',''),(23,'4s_mk Senior','TALA@gmail.com','CXCXCXCXCXBBB','2026-05-04 14:45:04',''),(24,'alshatti','alshatti@gmail.com','mohamad alshatti welcom','2026-05-04 14:51:41',NULL),(25,'4s_mk Senior','ssmk2060@gmail.com','x','2026-05-04 14:54:41','hyyy');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
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
