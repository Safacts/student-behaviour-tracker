-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: rubix
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `firstusers`
--

DROP TABLE IF EXISTS `firstusers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `firstusers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firstusers`
--

LOCK TABLES `firstusers` WRITE;
/*!40000 ALTER TABLE `firstusers` DISABLE KEYS */;
INSERT INTO `firstusers` VALUES (1,'xyzfgfhfgfhfg@gmail.com','2025-09-23 05:41:02'),(2,'hariprakashp61543@gmail.com','2025-09-23 05:41:11'),(3,'asrithapandi22@gmail.com','2025-09-23 05:44:45'),(4,'asrithapandi22@gmail.com','2025-09-25 06:48:44'),(5,'asrithapandi1@gmail.com','2025-09-25 06:57:05'),(6,'vinnubdhakarroy@gmail.com','2025-09-25 07:28:18'),(7,'wosile1873@cerisun.com','2025-09-25 07:46:40'),(8,'asrithapandi1@gmail.com','2025-10-07 05:26:52'),(9,'asri12345@gmail.com','2025-10-07 05:30:37'),(10,'vinnubdhakarroy@gmail.com','2025-10-10 13:03:21'),(11,'astothav@gmail.com','2025-10-10 13:04:11'),(12,'befiwer784@erynka.com','2025-10-18 05:15:33'),(13,'befiwer784@erynka.com','2025-10-18 05:20:16'),(14,'befiwer784@erynka.com','2025-10-18 05:49:22'),(15,'befiwer784@erynka.com','2025-10-18 05:52:38'),(16,'pra.subprime716@aleeas.com','2025-10-18 05:59:12'),(17,'pra.subprime716@aleeas.com','2025-10-18 06:08:58'),(18,'asri@gmail.com','2025-10-28 07:16:44'),(19,'asrt@gmail.com','2025-10-28 07:17:11'),(20,'asrt@gmail.com','2025-10-28 07:17:34'),(21,'hariprakashp61543@gmail.com','2025-10-28 07:26:56'),(22,'dhakar@gmial.com','2025-10-28 09:18:51'),(23,'vinnubdhakarroy@gmail.com','2025-10-28 09:19:17'),(24,'vinnubdhakarroy@gmail.com','2025-10-28 09:19:29'),(25,'vinnubdhakarroy@gmail.com','2025-10-28 09:21:01'),(26,'dummy@gmail.com','2025-10-28 09:21:27'),(27,'ammu@gmail.com','2025-10-28 14:07:26'),(28,'dudoo@gmail.com','2025-10-29 05:38:03'),(29,'dudoo@gmail.com','2025-10-29 05:38:53'),(30,'asrty@gmail.com','2025-12-15 04:51:40'),(31,'simplelogin-newsletter.popsicle101@simplelogin.com','2025-12-19 10:56:59'),(32,'test@example.com','2025-12-22 07:42:48'),(33,'testuser@example.com','2025-12-22 08:16:49'),(34,'dhakar@gmial.com','2025-12-27 09:01:57'),(35,'sr@gmail.com','2026-01-02 08:08:20'),(36,'dhakar@gmial.com','2026-01-10 07:40:04'),(37,'ganesh@gmail.com','2026-02-05 06:46:48'),(38,'ganesh@gmail.com','2026-02-05 06:50:10'),(39,'ganesh@gmail.com','2026-02-05 07:19:22'),(40,'dhakar@gmail.com','2026-02-05 09:42:46'),(41,'asrithap0906@gmail.com','2026-02-10 10:44:08'),(42,'vimall@gmail.com','2026-02-23 04:19:21'),(43,'asdref@gmail.com','2026-03-10 09:48:26'),(44,'xyz@gmail.com','2026-03-10 10:00:30'),(45,'xyz@gmail.com','2026-03-10 10:10:28'),(46,'neagy@gmail.com','2026-03-10 10:27:16'),(47,'asrithap096@gmail.com','2026-03-10 10:47:14'),(48,'asrithapandi202@gmail.com','2026-03-10 10:54:36'),(49,'asrithap0905@gmail.com','2026-03-10 11:09:00'),(50,'asrithap0908@gmail.com','2026-03-10 11:46:54'),(51,'asritha0906@gmail.com','2026-03-10 11:59:16'),(52,'asrithapandi202@gmail.com','2026-03-10 13:26:09'),(53,'xyas@gmail.com','2026-03-26 15:01:13'),(54,'parent@test.com','2026-03-30 03:23:23');
/*!40000 ALTER TABLE `firstusers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-12 22:53:58
