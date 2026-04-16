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
-- Table structure for table `overall_performance`
--

DROP TABLE IF EXISTS `overall_performance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `overall_performance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `parent_id` int NOT NULL,
  `daywise_overall_performance` longtext,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `daywise_overall_performance_continuation_2` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `overall_performance`
--

LOCK TABLES `overall_performance` WRITE;
/*!40000 ALTER TABLE `overall_performance` DISABLE KEYS */;
INSERT INTO `overall_performance` VALUES (1,16,15,'10/01/2024 -\nday_maths: 45\nday_science: 30\nday_social: 20\nday_iit: 25\nday_games: 30\nday_hobbies: 10\nquiz_lesson_name: Real Numbers (Maths)\nquiz_marks: 8/10\niit_lesson_name: Algebra Foundations (Maths)\niit_marks: 14/20\n----------------------------------\n\n10/02/2024 -\nday_maths: 50\nday_science: 40\nday_social: 25\nday_iit: 35\nday_games: 20\nday_hobbies: 15\nquiz_lesson_name: Fractions and Decimals (Maths)\nquiz_marks: 9/10\niit_lesson_name: Quadratic Warmup (Maths)\niit_marks: 16/20\n----------------------------------\n\n10/03/2024 -\nday_maths: 30\nday_science: 55\nday_social: 15\nday_iit: 20\nday_games: 25\nday_hobbies: 20\nquiz_lesson_name: Cell Structure (Science)\nquiz_marks: 7/10\niit_lesson_name: Atomic Bonds (Science)\niit_marks: 13/20\n----------------------------------\n\n10/04/2024 -\nday_maths: 60\nday_science: 35\nday_social: 30\nday_iit: 40\nday_games: 15\nday_hobbies: 10\nquiz_lesson_name: Triangles Review (Maths)\nquiz_marks: 10/10\niit_lesson_name: Coordinate Practice (Maths)\niit_marks: 18/20\n----------------------------------\n\n10/05/2024 -\nday_maths: 25\nday_science: 45\nday_social: 40\nday_iit: 15\nday_games: 35\nday_hobbies: 25\nquiz_lesson_name: Water Cycle (Science)\nquiz_marks: 8/10\niit_lesson_name: Climate Impact (Science)\niit_marks: 14/20\n----------------------------------\n\n10/06/2024 -\nday_maths: 55\nday_science: 30\nday_social: 20\nday_iit: 45\nday_games: 20\nday_hobbies: 10\nquiz_lesson_name: Integers Drill (Maths)\nquiz_marks: 8/10\niit_lesson_name: Number Theory Sprint (Maths)\niit_marks: 17/20\n----------------------------------\n\n10/07/2024 -\nday_maths: 20\nday_science: 25\nday_social: 60\nday_iit: 10\nday_games: 40\nday_hobbies: 30\nquiz_lesson_name: Ancient Civilizations (Social)\nquiz_marks: 9/10\niit_lesson_name: Cultural Analysis (Social)\niit_marks: 15/20\n----------------------------------\n\n10/08/2024 -\nday_maths: 65\nday_science: 50\nday_social: 15\nday_iit: 35\nday_games: 25\nday_hobbies: 15\nquiz_lesson_name: Linear Equations (Maths)\nquiz_marks: 9/10\niit_lesson_name: Algebraic Reasoning (Maths)\niit_marks: 19/20\n----------------------------------\n\n10/09/2024 -\nday_maths: 35\nday_science: 60\nday_social: 20\nday_iit: 25\nday_games: 30\nday_hobbies: 20\nquiz_lesson_name: Plant Systems (Science)\nquiz_marks: 8/10\niit_lesson_name: Ecology Lab (Science)\niit_marks: 16/20\n----------------------------------\n\n10/10/2024 -\nday_maths: 40\nday_science: 30\nday_social: 55\nday_iit: 20\nday_games: 20\nday_hobbies: 15\nquiz_lesson_name: Government Basics (Social)\nquiz_marks: 7/10\niit_lesson_name: Civic Case Study (Social)\niit_marks: 12/20\n----------------------------------\n\n10/11/2024 -\nday_maths: 70\nday_science: 45\nday_social: 25\nday_iit: 50\nday_games: 15\nday_hobbies: 15\nquiz_lesson_name: Exponents Practice (Maths)\nquiz_marks: 10/10\niit_lesson_name: Polynomial Workshop (Maths)\niit_marks: 20/20\n----------------------------------\n\n10/12/2024 -\nday_maths: 30\nday_science: 55\nday_social: 35\nday_iit: 15\nday_games: 40\nday_hobbies: 25\nquiz_lesson_name: Human Body Systems (Science)\nquiz_marks: 9/10\niit_lesson_name: Biology Challenge (Science)\niit_marks: 17/20\n----------------------------------\n\n10/13/2024 -\nday_maths: 45\nday_science: 25\nday_social: 60\nday_iit: 30\nday_games: 35\nday_hobbies: 20\nquiz_lesson_name: Medieval Europe (Social)\nquiz_marks: 8/10\niit_lesson_name: Trade Route Analysis (Social)\niit_marks: 14/20\n----------------------------------\n\n10/14/2024 -\nday_maths: 60\nday_science: 40\nday_social: 20\nday_iit: 45\nday_games: 25\nday_hobbies: 10\nquiz_lesson_name: Geometry Constructions (Maths)\nquiz_marks: 9/10\niit_lesson_name: Spatial Reasoning (Maths)\niit_marks: 18/20\n----------------------------------\n\n10/15/2024 -\nday_maths: 35\nday_science: 65\nday_social: 25\nday_iit: 20\nday_games: 30\nday_hobbies: 25\nquiz_lesson_name: Chemical Equations (Science)\nquiz_marks: 8/10\niit_lesson_name: Reaction Rates (Science)\niit_marks: 15/20\n----------------------------------\n\n10/16/2024 -\nday_maths: 50\nday_science: 30\nday_social: 45\nday_iit: 35\nday_games: 20\nday_hobbies: 20\nquiz_lesson_name: Indian Constitution (Social)\nquiz_marks: 9/10\niit_lesson_name: Policy Simulation (Social)\niit_marks: 16/20\n----------------------------------\n','2025-11-19 07:43:44','10/17/2024 -\nday_maths: 55\nday_science: 45\nday_social: 30\nday_iit: 40\nday_games: 25\nday_hobbies: 15\nquiz_lesson_name: Probability Basics (Maths)\nquiz_marks: 8/10\niit_lesson_name: Statistics Drill (Maths)\niit_marks: 17/20\n----------------------------------\n\n10/18/2024 -\nday_maths: 25\nday_science: 60\nday_social: 35\nday_iit: 15\nday_games: 35\nday_hobbies: 30\nquiz_lesson_name: Electricity Fundamentals (Science)\nquiz_marks: 9/10\niit_lesson_name: Circuit Reasoning (Science)\niit_marks: 18/20\n----------------------------------\n\n10/19/2024 -\nday_maths: 40\nday_science: 30\nday_social: 65\nday_iit: 20\nday_games: 30\nday_hobbies: 25\nquiz_lesson_name: World Geography (Social)\nquiz_marks: 7/10\niit_lesson_name: Map Interpretation (Social)\niit_marks: 12/20\n----------------------------------\n\n10/20/2024 -\nday_maths: 70\nday_science: 50\nday_social: 25\nday_iit: 45\nday_games: 20\nday_hobbies: 10\nquiz_lesson_name: Algebraic Expressions (Maths)\nquiz_marks: 10/10\niit_lesson_name: Inequality Quest (Maths)\niit_marks: 19/20\n----------------------------------\n\n10/21/2024 -\nday_maths: 30\nday_science: 55\nday_social: 40\nday_iit: 15\nday_games: 40\nday_hobbies: 20\nquiz_lesson_name: Mixtures and Solutions (Science)\nquiz_marks: 8/10\niit_lesson_name: Lab Techniques (Science)\niit_marks: 14/20\n----------------------------------\n\n10/22/2024 -\nday_maths: 45\nday_science: 35\nday_social: 60\nday_iit: 30\nday_games: 25\nday_hobbies: 25\nquiz_lesson_name: Renaissance Europe (Social)\nquiz_marks: 9/10\niit_lesson_name: Historical Inquiry (Social)\niit_marks: 15/20\n----------------------------------\n\n10/23/2024 -\nday_maths: 60\nday_science: 40\nday_social: 20\nday_iit: 50\nday_games: 20\nday_hobbies: 15\nquiz_lesson_name: Coordinate Geometry (Maths)\nquiz_marks: 9/10\niit_lesson_name: Vector Sprint (Maths)\niit_marks: 18/20\n----------------------------------\n\n10/24/2024 -\nday_maths: 35\nday_science: 65\nday_social: 30\nday_iit: 25\nday_games: 30\nday_hobbies: 20\nquiz_lesson_name: Photosynthesis Lab (Science)\nquiz_marks: 8/10\niit_lesson_name: Energy Conversion (Science)\niit_marks: 16/20\n----------------------------------\n\n10/25/2024 -\nday_maths: 50\nday_science: 30\nday_social: 55\nday_iit: 35\nday_games: 25\nday_hobbies: 25\nquiz_lesson_name: Economics Basics (Social)\nquiz_marks: 9/10\niit_lesson_name: Market Simulation (Social)\niit_marks: 17/20\n----------------------------------\n\n10/26/2024 -\nday_maths: 65\nday_science: 45\nday_social: 20\nday_iit: 40\nday_games: 20\nday_hobbies: 15\nquiz_lesson_name: Trigonometry Warmup (Maths)\nquiz_marks: 8/10\niit_lesson_name: Angle Mastery (Maths)\niit_marks: 16/20\n----------------------------------\n\n10/27/2024 -\nday_maths: 30\nday_science: 60\nday_social: 35\nday_iit: 15\nday_games: 35\nday_hobbies: 30\nquiz_lesson_name: Weather Patterns (Science)\nquiz_marks: 7/10\niit_lesson_name: Data Interpretation (Science)\niit_marks: 13/20\n----------------------------------\n\n10/28/2024 -\nday_maths: 55\nday_science: 25\nday_social: 65\nday_iit: 30\nday_games: 40\nday_hobbies: 20\nquiz_lesson_name: Colonial India (Social)\nquiz_marks: 10/10\niit_lesson_name: Policy Debate (Social)\niit_marks: 18/20\n----------------------------------\n\n10/29/2024 -\nday_maths: 45\nday_science: 50\nday_social: 25\nday_iit: 45\nday_games: 20\nday_hobbies: 15\nquiz_lesson_name: Algebra Word Problems (Maths)\nquiz_marks: 9/10\niit_lesson_name: Logical Reasoning (Maths)\niit_marks: 17/20\n----------------------------------\n\n10/30/2024 -\nday_maths: 35\nday_science: 55\nday_social: 40\nday_iit: 20\nday_games: 30\nday_hobbies: 25\nquiz_lesson_name: Matter States (Science)\nquiz_marks: 8/10\niit_lesson_name: Particle Motion (Science)\niit_marks: 15/20\n----------------------------------\n\n10/31/2024 -\nday_maths: 60\nday_science: 35\nday_social: 50\nday_iit: 30\nday_games: 25\nday_hobbies: 20\nquiz_lesson_name: Modern World History (Social)\nquiz_marks: 9/10\niit_lesson_name: Comparative Study (Social)\niit_marks: 16/20\n----------------------------------\n');
/*!40000 ALTER TABLE `overall_performance` ENABLE KEYS */;
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
