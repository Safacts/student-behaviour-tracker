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
-- Table structure for table `parent_student_messages`
--

DROP TABLE IF EXISTS `parent_student_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parent_student_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `parent_username` varchar(50) DEFAULT NULL,
  `student_username` varchar(50) DEFAULT NULL,
  `message` text,
  `sender_role` enum('parent','student') DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parent_student_messages`
--

LOCK TABLES `parent_student_messages` WRITE;
/*!40000 ALTER TABLE `parent_student_messages` DISABLE KEYS */;
INSERT INTO `parent_student_messages` VALUES (1,'P90101','S90101','hii son','parent','2025-10-19 11:52:50'),(2,'P90101','S90101','how are you?','parent','2025-10-19 11:53:03'),(3,'P100101','S100101','hii daddy','student','2025-12-02 11:57:13'),(4,'P100101','S100101','hello daddy,where are you?','student','2025-12-02 12:13:25'),(5,'P90104','S90104','hii dad','student','2025-12-15 11:34:46'),(6,'P90104','S90104','where are you ?','student','2025-12-15 11:34:58'),(7,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:06'),(8,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:06'),(9,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:06'),(10,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:07'),(11,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:07'),(12,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:07'),(13,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:07'),(14,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:07'),(15,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:07'),(16,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:07'),(17,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:07'),(18,'P10th0101','S10th0101','hello daddy','student','2026-01-07 12:25:08'),(19,'P10th0101','S10th0101','hi pappa','student','2026-01-07 12:49:31'),(20,'P10th0101','S10th0101','when did you come to home ?','student','2026-01-07 12:49:52'),(21,'P10th0101','S10th0101','dad please bring chocolates for me','student','2026-01-07 13:00:07'),(22,'P10th0101','S10th0101','hello son','parent','2026-01-19 15:11:52'),(23,'P10th0101','S10th0101','what are you doing?','parent','2026-01-19 15:12:01'),(24,'P10th0101','S10th0101','i am coming ,donot wait for me ?','parent','2026-01-19 15:20:11'),(25,'P10th0101','S10th0101','hello dad','student','2026-01-19 15:20:54'),(26,'P10th0101','S10th0101','hello dad','student','2026-01-19 15:20:57'),(27,'P10th0101','S10th0101','hello dad','student','2026-01-19 15:20:59'),(28,'P10th0101','S10th0101','hello dad','student','2026-01-19 15:20:59'),(29,'P10th0101','S10th0101','hello dad','student','2026-01-19 15:21:00'),(30,'P10th0101','S10th0101','hello dad','student','2026-01-19 15:21:00'),(31,'P10th0101','S10th0101','hello daddy,where are you ?','student','2026-02-01 00:13:49'),(32,'P10th0101','S10th0101','hello daddy','parent','2026-02-09 10:23:03'),(33,'P10th0103','S10th0103','what are you doing dad ?','student','2026-02-23 12:06:38'),(34,'P100101','S100101','hello daddy, how are you ?','student','2026-03-20 10:06:32'),(35,'P100101','S100101','where are you ? come fast','student','2026-03-20 10:07:22'),(36,'P100101','S100101','hello ,please bring snacks daddy .','student','2026-03-20 12:14:57'),(37,'P100101','S100101','bring ,india maps','student','2026-03-20 12:38:22'),(38,'P90101','S90101','hi dad','student','2026-04-12 22:37:23'),(39,'P90101','S90101','please come early today.','student','2026-04-12 22:37:49'),(40,'P90101','S90101','ok beta','parent','2026-04-12 22:44:52');
/*!40000 ALTER TABLE `parent_student_messages` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-12 22:53:57
