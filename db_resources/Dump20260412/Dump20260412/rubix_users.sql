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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `role` varchar(10) NOT NULL,
  `parent_id` int DEFAULT NULL,
  `class` varchar(10) DEFAULT NULL,
  `school` varchar(100) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `syllabus` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `parent_address` varchar(255) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `first_login` tinyint(1) NOT NULL DEFAULT '1',
  `camera_enabled` tinyint(1) NOT NULL DEFAULT '1',
  `rewards_points` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'P90101','P90101','Mahendra','hariprakashp61543@gmail.com','9858563214','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,0,0),(2,'S90101','S90101','Hari',NULL,NULL,'student',1,'9th','UCEN-JNTUK','boy','CBSE','Salem',NULL,'KA',1,1,135),(3,'P100101','P100101','raja','asrithapandi22@gmail.com','9440319380','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(4,'S100101','S100101','lakshmi',NULL,NULL,'student',3,'10th','UCEN-JNTUK','girl','CBSE','Salem',NULL,'KA',1,0,1060),(5,'P80101','vinnu@2002','Dhakar','asrithapandi1@gmail.com','973864804','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(6,'S80101','S80101','drithi',NULL,NULL,'student',5,'8th','VBR','girl','CBSE','Salem',NULL,'KA',1,0,0),(7,'P70101','VislxFUuS','Amrutha','vinnubdhakarroy@gmail.com','95051 26364','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(8,'S70101','S70101','Sunny',NULL,NULL,'student',7,'7th','Delhi public school','boy','CBSE','elluru',NULL,'MH',1,1,0),(9,'P60101','P60101','Puitha','wosile1873@cerisun.com','91823 18632','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(10,'S60101','S60101','kamal',NULL,NULL,'student',9,'6th','Delhi public school','boy','CBSE','Salem',NULL,'KA',1,0,0),(11,'P90102','0VRR3HYPu','vimal','asri12345@gmail.com','9874563210','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(12,'S90102','S90102','Kailash',NULL,NULL,'student',11,'9th','vignaya high school','boy','CBSE','katak',NULL,'KL',1,0,50),(13,'P100102','7XW3gv7IS','vimal','astothav@gmail.com','9874544210','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(14,'S100102','Cwn49MF5G','Kailash',NULL,NULL,'student',13,'10th','vignaya high school','girl','CBSE','katak',NULL,'KL',1,0,0),(15,'P60102','P60102','kailash','dummy@gmail.com','9440319380','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,0,0),(16,'S60102','S60102','deepu',NULL,NULL,'student',15,'6th','UCEN-JNTUK','girl','CBSE','Bangalore',NULL,'MN',1,0,0),(17,'P70102','UTdUuB4rb','Dhakar','ammu@gmail.com','9440319380','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(18,'S70102','Vtzel7S6y','Deepu',NULL,NULL,'student',17,'7th','UCEN-JNTUK','boy','CBSE','Bangalore',NULL,'MN',1,0,0),(19,'P90103','P90103','Dhakar','dudoo@gmail.com','9440319380','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(20,'S90103','WpAsLSxng','dude',NULL,NULL,'student',19,'9th','UCEN-JNTUK','boy','CBSE','Bangalore',NULL,'MN',1,0,0),(21,'P90104','P90104','hjrf','asrty@gmail.com','9632087417','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(22,'S90104','S90104','ase',NULL,NULL,'student',21,'9th','wer','girl','CBSE','nell',NULL,'ML',1,0,0),(23,'P9th0101','P9th0101','Lakshmi','simplelogin-newsletter.popsicle101@simplelogin.com','9635147285','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(24,'S9th0101','S9th0101','roy',NULL,NULL,'student',23,'9th','Delhi public school','boy','CBSE','Hi Tech city',NULL,'CG',1,1,0),(25,'P10th0101','P10th0101','dhakar','dhakar@gmial.com','9632580147','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(26,'S10th0101','S10th0101','vimmu',NULL,NULL,'student',25,'10th','vignaya high school','boy','CBSE','Bangalore',NULL,'MN',1,0,0),(27,'P10th0102','12345','ganesh','ganesh@gmail.com','9807654323','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,1,0),(28,'S10th0102','user@123','Shiva',NULL,NULL,'student',27,'10th','VLS school','boy','CBSE','Nellore',NULL,'AP',0,0,0),(29,'P100103','lErqOSasg','Dhakar','Rai143@gmail.com','9568741023','parent',NULL,NULL,NULL,NULL,NULL,'Salem','Kalivelapalem Village','KL',1,1,0),(30,'S100103','tftCVfSPP','Asri',NULL,NULL,'student',29,'10','PRAGATI','girl','CBSE','Salem',NULL,'KL',1,1,0),(31,'P90105','H1SA7HYtD','Dhakar rai','Royroy@gmail.com','9658741230','parent',NULL,NULL,NULL,NULL,NULL,'Salem','Kalivelapalem Village','RJ',1,1,0),(32,'S90105','AOby54H7b','Ramya sri',NULL,NULL,'student',31,'9','PRAGATI','girl','CBSE','Salem',NULL,'RJ',1,1,0),(33,'P10th0103','P10th0103','kailash','vimall@gmail.com','9087612345','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(34,'S10th0103','S10th0103','siddik',NULL,NULL,'student',33,'10th','VRS','boy','CBSE','Salem',NULL,'KA',1,0,0),(35,'P9th0102','$2b$12$OjwED.r7IlKHVWeczHM8ieekR3X4lJxh.W7xiw3ncBWOSpunLxanC','laskh','neagy@gmail.com','9784561240','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(36,'S9th0102','$2b$12$SZ51vg9exohP5cxPHx/jlu0btVWW5/T1ukL4CyuQxaQylN73esJB2','lucky',NULL,NULL,'student',35,'9th','BNR high school','girl','CBSE','nellore',NULL,'KA',1,1,0),(37,'P10th0104','$2b$12$N.5vemTJUrY0HiDosdfXJeu6hDHE5ReebHq5jya6IG2hrZzpGbmnK','venky','asrithap06@gmail.com','9784561249','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(38,'S10th0104','$2b$12$f/wBeACW/./9CfEHJlOUCevql61Rnwbe1c4XwaEb5NLN9QlO4Hm1C','lucky',NULL,NULL,'student',37,'10th','BNR high school','boy','CBSE','nellore',NULL,'KA',1,1,0),(39,'P10th0105','$2b$12$D8K9TpxLdczP9BtYDqf9zu1ylCWJPrvqNSTQkfatkpFz63dYtiJS6','venky','asrithapandi22@gmail.com','9784561255','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(40,'S10th0105','$2b$12$7K05l8B22gZtPn8t6G6EDeMKtkO6mCctZEBdqmf9dhBNcQANab/aG','lucky',NULL,NULL,'student',39,'10th','BNR high school','girl','CBSE','nellore',NULL,'KA',1,1,0),(41,'P10th0106','P10th0106','venky','asrithap0905@gmail.com','9784561258','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(42,'S10th0106','S10th0106','lucky',NULL,NULL,'student',41,'10th','BNR high school','girl','CBSE','nellore',NULL,'KA',1,0,0),(43,'P9th0103','$2b$12$224n40pK6Z./rDtpnwxlr.LZPAd3kMSt9TtZqfY7rT1x34oCEmItu','Lakshmi','asrithap06@gmail.com','9784561259','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(44,'S9th0103','$2b$12$FenN5AgGu5c4N9SAS3U..O4.YLHZGCc8ppkbYMtoo4fjxdYchHePy','lucky',NULL,NULL,'student',43,'9th','BNR high school','girl','CBSE','nellore',NULL,'KA',1,1,0),(45,'P9th0104','$2b$12$PiPQXTF2bqxVZ2zANlRIB.Xv7BIPTcAt.A1ECff.NjDGxoBhzkPpa','krish','asrithap0906@gmail.com','9784561242','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(46,'S9th0104','$2b$12$zR9.T4VyvF46QA/D5qQCCOGqWkKoyuMW/6w4xzsrqr7Xvd6YIouPy','bhaskar',NULL,NULL,'student',45,'9th','BNR high school','boy','CBSE','nellore',NULL,'NL',1,1,0),(47,'P10th0107','P10th0107','mahen','asrithapandi202@gmail.com','9852347166','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(48,'S10th0107','S10th0107','bhaskar',NULL,NULL,'student',47,'10th','BNR high school','boy','CBSE','nellore',NULL,'NL',1,0,190),(49,'P9th0105','$2b$12$CkZ2Nwc9.MbZ7KXWb9ORw.ck4qjs7Ur6CRPIPcDrC5AhpvWD3MWDu','yaksh','xyas@gmail.com','9658741123','parent',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,0),(50,'S9th0105','S9th0105','Vaibhav',NULL,NULL,'student',49,'9th','BNR high school','boy','CBSE','nellore',NULL,'NL',1,1,0),(52,'P80102','$2b$12$VQp7eHmbdvF9Q/oZYi2zdOuSOpSeNW1bABN.18hNi8js78wKoLmnW','yaksh','asrithapandi2002@gmail.com','9658740123','parent',NULL,NULL,NULL,NULL,NULL,'nellore',NULL,'TN',1,1,0),(53,'S80102','$2b$12$IfGvSicZT5FAIAFU8TsAgOF9cmPQ545bP.63YM58Ue/xtwikk9uvO','Vaibhav',NULL,NULL,'student',52,'8','BNR high school','boy','CBSE','nellore',NULL,'TN',1,1,0),(54,'P70103','$2b$12$xD3lwD25.eG0sU.FxIsknuf/M6nSWnCIgLtyh7jdjfNKaJyQLLJbO','Shajid','sajid@gmail.com','9845763210','parent',NULL,NULL,NULL,NULL,NULL,'nellore',NULL,'TG',1,1,0),(55,'S70103','$2b$12$G7bRDOHjv1Q2sxnCgtQ4F.zg/axwmbumJ.cgSEN90CaQTbJ2CIjsG','Farih',NULL,NULL,'student',54,'7','BNR high school','boy','CBSE','nellore',NULL,'TG',1,1,0),(56,'P80103','$2b$12$uQBc76A9FmLwsQyjNoufLuhVh7o8Zotip3wmp6UXSu.20yWjFjluC','Kavya','kavya@gmail.com','9368745124','parent',NULL,NULL,NULL,NULL,NULL,'nellore',NULL,'TN',1,1,0),(57,'S80103','$2b$12$/F0pCZvGQzApvYMiDJcXE.8JwLD0uuYJHox5pLaVJtSid8SOR3reu','Divay',NULL,NULL,'student',56,'8','BNR high school','girl','CBSE','nellore',NULL,'TN',1,1,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
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
