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
-- Table structure for table `employee_details`
--

DROP TABLE IF EXISTS `employee_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `contact` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `doj` date DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  `qualification` varchar(255) DEFAULT NULL,
  `designation` varchar(255) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `profile_completed` tinyint(1) NOT NULL DEFAULT '0',
  `date_of_birth` date DEFAULT NULL,
  `fresher` tinyint(1) DEFAULT NULL,
  `experienced` tinyint(1) DEFAULT NULL,
  `marital_status` varchar(20) DEFAULT NULL,
  `spouse_name` varchar(100) DEFAULT NULL,
  `spouse_contact` varchar(15) DEFAULT NULL,
  `father_name` varchar(100) DEFAULT NULL,
  `father_contact` varchar(15) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `street_address` text,
  `pincode` varchar(10) DEFAULT NULL,
  `pan_number` varchar(10) DEFAULT NULL,
  `aadhar_number` varchar(20) DEFAULT NULL,
  `resume` longblob,
  `educational_documents` longblob,
  `experienced_certificates` longblob,
  `pan_card` longblob,
  `aadhar_card` longblob,
  `role` varchar(100) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Active',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_details`
--

LOCK TABLES `employee_details` WRITE;
/*!40000 ALTER TABLE `employee_details` DISABLE KEYS */;
INSERT INTO `employee_details` VALUES (1,'John Doe','9876543210','john@example.com','2026-02-11',NULL,'B.Tech','Senior Developer',NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Admin','Active'),(2,'Asritha','951742380','asrithap0906@gmail.com',NULL,NULL,'M.Tech','Software developer','asrith0002','5e!M94KtVX@v',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Active'),(3,'dhakar','951742380','asrithapandi2002@gmail.com',NULL,NULL,'b tech','software developer','dhakar0003','F6@xZpDh$YvA',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Active'),(4,'HARIPRAKASH','09440319380','asrithapandi200261543@gmail.com',NULL,NULL,'B.Tech','Software','haripr0004','HSK%JGT4oZCG',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Active'),(5,'Lakshmi','9857641230','lakshmi@gmail.com','2026-04-04',500000.00,'B.Tech in Computer Science','Working as Python Developer','lakshm0005','$2b$12$fihJZPFOahLKMQ.HXUnx9uSFUUj9AJDXYWBXCULfDy3mRMGLBqk7i',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Active'),(6,'Vikram','9687451320','vikram@gmail.com',NULL,NULL,'B.Tech in Computer Science','Working as Python Developer','vikram0006','$2b$12$vH1w33IQcMAguK4xr.J8FeX.IM1Mhi.84RULdVoeR.k4tvFArFSZq',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Agent','Active'),(7,'Sharma','6547891234','sharma@gmail.com',NULL,NULL,'MTech','Python Developer','sharma0007','$2b$12$azWWqTm03CfjDyY/7/uHvOSgj00lLF0eyTKGc5KWr5Dc571cOL3g.',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Active'),(8,'Kamal','8745961204','kamal@gmail.com',NULL,NULL,'MTech','Python Developer','kamal0008','kamal0008',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'employee','Active'),(9,'Fahid','8576954123','Fahid@gmail.com','2000-02-09',3000000.00,'Degree','Marketing','fahid0009','fahid0009',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Admin','Active'),(10,'Priya','8974563210','priya@gmail.com','2000-06-17',504502.00,'B.Tech','Python Developer','priya0010','$2b$12$gMGq.Pjq7WQMWcRkCwMoOOfXqy8sjkOW9vosNVHKaEqa4EXVIrEEq',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'agent','Active'),(11,'Asritha Pandi','9491510499','asrithapandi22@gmail.com','2002-06-09',12000000.00,'Btech','Python Developer','asrith0011','$2b$12$PAGxBspinOsmsGcw2/eZkuq2oPCE6EgTAC9xOfwPGWEABhWD4iv7a',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'employee','Active');
/*!40000 ALTER TABLE `employee_details` ENABLE KEYS */;
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
