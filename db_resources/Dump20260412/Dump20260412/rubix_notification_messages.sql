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
-- Table structure for table `notification_messages`
--

DROP TABLE IF EXISTS `notification_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subject` varchar(255) DEFAULT NULL,
  `message` text,
  `suggestion_team` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  `class` text,
  `notification_date` varchar(50) DEFAULT NULL,
  `customer_feedback` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification_messages`
--

LOCK TABLES `notification_messages` WRITE;
/*!40000 ALTER TABLE `notification_messages` DISABLE KEYS */;
INSERT INTO `notification_messages` VALUES (1,NULL,'{\"message\": \"Your IIT-JEE & NEET weekly test is ready (Cycle 7).\", \"action_text\": \"Start Weekly Test\", \"action_url\": \"/exam_weekly?cycle=7\", \"cycle\": 7}',NULL,NULL,NULL,NULL,NULL,NULL,'2025-10-01 08:08:11','2026-02-10 16:02:44'),(2,NULL,'hello ,this is important note that is ,there is some internal issue please fix it quicky',NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-05 10:31:37','2026-02-10 16:02:44'),(3,NULL,'hello,gather all to the team meeting',NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-10 10:00:15','2026-02-10 16:02:44'),(4,NULL,'hello ,good evening',NULL,'Mahesh','admin,employee,student,parent',NULL,NULL,NULL,'2026-02-10 10:32:44','2026-02-10 16:02:44'),(5,NULL,'how are you all?',NULL,'Mahesh','student',NULL,NULL,NULL,'2026-02-10 10:34:44','2026-02-10 16:04:44'),(6,NULL,'join the meeting by 4\'o clock',NULL,'Mahesh','employee',NULL,NULL,NULL,'2026-02-10 10:35:40','2026-02-10 16:05:40'),(7,NULL,'hello, good morning to all,today we have metting',NULL,'Mahesh','employee',NULL,NULL,NULL,'2026-02-11 03:54:03','2026-02-11 09:24:03'),(8,NULL,'good morning',NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-11 04:53:04','2026-02-11 10:23:04'),(9,NULL,'Dear Parent, your child\'s progress report for February is now available. Please check the reports section for details.',NULL,'Academic Team','parent',NULL,NULL,NULL,'2026-02-14 04:48:58','2026-02-14 10:18:58'),(10,NULL,'The school will be closed on Monday for a public holiday.',NULL,'School Office','everyone',NULL,NULL,NULL,'2026-02-14 04:48:58','2026-02-14 10:18:58'),(11,NULL,'today we have special talent exam test',NULL,NULL,NULL,NULL,NULL,NULL,'2026-03-26 06:32:04','2026-03-26 12:02:04'),(12,NULL,'our app provide ,wonderfull opportunity to all students to expose they talent in the chess champion',NULL,'Mahesh','admin,employee,student,parent',NULL,NULL,NULL,'2026-03-26 06:59:58','2026-03-26 12:29:58'),(13,NULL,'Thank you for supporting us. All parents are grateful to you.',NULL,'Mahesh','parent',NULL,NULL,NULL,'2026-03-26 07:27:59','2026-03-26 12:57:59'),(14,NULL,'today ,we have chess competition',NULL,'Super Admin-Mahesh','admin,employee,student,parent',NULL,NULL,NULL,'2026-03-26 07:42:10','2026-03-26 13:12:10'),(15,'parents meeting','today evening we have parents meeting ,please join the link',NULL,'Super Admin-Mahesh','admin,employee,student,parent',NULL,NULL,NULL,'2026-03-31 07:04:19','2026-03-31 12:34:18'),(16,'App updates','In our website we added wonderfull features,please once click on the link given in the notification and follow that steps to update your individual accounts.\nthanking you all\nyours supportive management team',NULL,'Super Admin-Mahesh','admin,employee,student,parent',NULL,NULL,NULL,'2026-04-01 04:20:08','2026-04-01 09:50:07'),(17,'Exam alert','Tommorrow Maths MCQ\'S exams on circles chapter',NULL,'Super Admin-Mahesh','admin,employee,student,parent',NULL,NULL,NULL,'2026-04-01 08:41:58','2026-04-01 14:11:58'),(19,'Regarding Talent test','This sunday our management is conducting the talent test for all classes ,so please take the test and proove yourself',NULL,'Super Admin-Mahesh','admin,employee,student,parent','All Classes','04-04-2026',NULL,'2026-04-04 06:28:27','2026-04-04 11:58:27'),(20,'Chess competition','this wednesday we are conducting chess competition, who are insterested those can join in these chess competition',NULL,'Super Admin-Mahesh','admin,employee,student,parent','7th, 8th, 10th, 9th','04-04-2026',NULL,'2026-04-04 06:33:44','2026-04-04 12:03:44'),(22,'Mock Test','this saturday ,we are conducting mock test\nso please attend all,to showcase your skills.',NULL,'Super Admin-fahid0009','admin,employee,student,parent','All Classes','10-04-2026',NULL,'2026-04-09 12:15:09','2026-04-09 17:45:09'),(23,'Talent Test','Tommor all students attend the talent test',NULL,'Super Admin-kamal0008','admin,employee,student,parent','All Classes','10-04-2026',NULL,'2026-04-09 12:20:32','2026-04-09 17:50:32');
/*!40000 ALTER TABLE `notification_messages` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-12 22:53:56
