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
-- Table structure for table `study_plan`
--

DROP TABLE IF EXISTS `study_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `study_plan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `plan_date` date NOT NULL,
  `subject` varchar(100) NOT NULL,
  `lesson` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status_data` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_student_date` (`student_id`,`plan_date`),
  KEY `idx_student_date` (`student_id`,`plan_date`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `study_plan`
--

LOCK TABLES `study_plan` WRITE;
/*!40000 ALTER TABLE `study_plan` DISABLE KEYS */;
INSERT INTO `study_plan` VALUES (1,4,'2026-03-12','Maths','Polynomials','2026-03-12 06:00:39',NULL),(2,4,'2026-03-13','Science','Acids, Bases and Salts','2026-03-12 06:00:46',NULL),(3,4,'2026-03-14','Social','Gender , Religion And Caste','2026-03-12 06:00:54',NULL),(4,4,'2026-03-20','Science','Carbon and its Compounds','2026-03-20 07:33:24',NULL),(5,4,'2026-03-21','Social','Gender , Religion And Caste','2026-03-20 07:33:32',NULL),(6,4,'2026-03-24','Maths','Polynomials','2026-03-24 04:51:12',NULL),(7,4,'2026-03-25','Science','Life Processes','2026-03-24 04:51:21',NULL),(8,4,'2026-03-26','Social','Globalisation And The Indian Economy','2026-03-24 04:51:35',NULL),(9,4,'2026-03-27','English','Study Session','2026-03-24 04:51:58',NULL),(10,4,'2026-03-28','Telugu/Hindi','Study Session','2026-03-24 04:52:04',NULL),(11,42,'2026-03-30','Maths','Polynomials','2026-03-30 14:25:07',NULL),(14,42,'2026-04-02','Social','Globalisation And The Indian Economy','2026-03-30 14:26:54',NULL),(15,42,'2026-04-03','Telugu/Hindi','Study Session','2026-03-30 14:27:01',NULL),(16,42,'2026-04-04','IT/Computer','Study Session','2026-03-30 14:27:37',NULL),(17,42,'2026-03-31','English','Study Session','2026-03-31 03:50:56',NULL),(18,42,'2026-04-01','Science','Control and Coordination','2026-03-31 03:51:36',NULL),(19,4,'2026-04-06','Maths','Polynomials','2026-04-06 06:56:14',NULL),(20,4,'2026-04-07','Science','Life Processes','2026-04-06 06:56:23',NULL),(21,4,'2026-04-08','Social','Federalism','2026-04-06 06:56:32',NULL),(22,4,'2026-04-09','English','Study Session','2026-04-06 06:56:40',NULL),(23,4,'2026-04-10','Telugu/Hindi','Study Session','2026-04-06 06:57:00',NULL),(24,4,'2026-04-11','IT/Computer','Study Session','2026-04-06 06:57:06',NULL),(25,12,'2026-04-07','Maths','Polynomials','2026-04-07 05:07:10',NULL),(26,12,'2026-04-08','Science','Is Matter Around Us Pure','2026-04-07 05:07:19',NULL),(27,12,'2026-04-09','Social','drainage','2026-04-07 05:07:27',NULL),(28,12,'2026-04-10','English','Study Session','2026-04-07 05:07:32',NULL),(29,12,'2026-04-11','Telugu/Hindi','Study Session','2026-04-07 05:07:40',NULL),(30,48,'2026-04-08','Maths','Polynomials','2026-04-08 04:49:51',NULL),(33,48,'2026-04-11','IT/Computer','Study Session','2026-04-08 04:50:14',NULL),(34,48,'2026-04-09','Maths','Polynomials','2026-04-08 05:10:30',NULL),(35,48,'2026-04-10','Maths','Polynomials','2026-04-08 05:16:35',NULL),(36,2,'2026-04-13','English','Study Session','2026-04-12 16:52:51',NULL),(37,2,'2026-04-14','Science','Atoms And Molecules','2026-04-12 16:53:08',NULL);
/*!40000 ALTER TABLE `study_plan` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-12 22:53:59
