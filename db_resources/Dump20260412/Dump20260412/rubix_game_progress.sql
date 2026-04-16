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
-- Table structure for table `game_progress`
--

DROP TABLE IF EXISTS `game_progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_progress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `game_name` varchar(255) NOT NULL,
  `level` int DEFAULT '1',
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`game_name`),
  CONSTRAINT `game_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=291 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_progress`
--

LOCK TABLES `game_progress` WRITE;
/*!40000 ALTER TABLE `game_progress` DISABLE KEYS */;
INSERT INTO `game_progress` VALUES (1,4,'Memory Match',11,'2025-12-02 12:17:51'),(4,4,'Word Puzzle',1,'2025-12-02 09:22:35'),(7,4,'MATHIONAIRE',1,'2025-09-29 06:10:00'),(17,4,'Sudoku Puzzle',1,'2025-12-02 12:29:04'),(50,2,'Memory Match',19,'2025-12-09 10:56:29'),(62,2,'MATHIONAIRE',1,'2025-09-30 12:31:19'),(65,2,'Sudoku Puzzle',1,'2025-10-28 06:57:48'),(74,2,'Word Puzzle',5,'2026-04-12 17:05:16'),(129,2,'Equation Builder',7,'2025-10-28 06:48:53'),(196,8,'Memory Match',12,'2025-10-08 07:04:58'),(205,3,'Word Puzzle',1,'2025-10-07 11:42:36'),(231,16,'Memory Match',7,'2025-10-28 13:02:55'),(233,16,'Equation Builder',4,'2025-10-28 12:10:32'),(240,16,'Word Puzzle',3,'2025-10-28 12:21:26'),(242,16,'Sudoku Puzzle',2,'2025-10-28 13:07:25'),(243,18,'Memory Match',5,'2025-10-29 02:57:32'),(245,20,'Word Puzzle',4,'2025-10-29 06:46:48'),(250,4,'Equation Builder',1,'2025-12-02 08:38:29'),(260,22,'Memory Match',16,'2025-12-24 10:17:12'),(263,22,'Equation Builder',3,'2025-12-24 06:51:47'),(265,22,'Word Puzzle',3,'2025-12-17 05:22:53'),(268,24,'Memory Match',3,'2025-12-19 17:28:12'),(269,24,'Equation Builder',1,'2025-12-19 17:29:40'),(276,26,'Memory Match',9,'2026-01-29 16:21:26'),(279,26,'Equation Builder',5,'2026-02-07 05:56:55'),(280,26,'Word Puzzle',2,'2026-02-05 07:29:12');
/*!40000 ALTER TABLE `game_progress` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-12 22:53:54
