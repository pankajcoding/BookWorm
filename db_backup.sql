-- MySQL dump 10.13  Distrib 8.0.17, for Linux (x86_64)
--
-- Host: localhost    Database: bookworm
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `edition` int(11) DEFAULT NULL,
  `subject` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `owner` varchar(255) DEFAULT NULL,
  `originalprice` double DEFAULT NULL,
  `price` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'uhui',7,'hghj','hjg',NULL,'123@gmail.com',78,78),(2,'sds',2,'maths','dsd',NULL,'123@gmail.com',21,32),(3,'sdsdsds',2,'science','dsd',NULL,'123@gmail.com',21,32),(4,'sdsdsds',2,'Mathematics','dsd',NULL,'123@gmail.com',21,32),(5,'hj',8,'Medicine','kjl',NULL,'123@gmail.com',90,90),(6,'book1',2,'Education','sda',NULL,'123@gmail.com',32,78),(7,'weq',32,'Computer Science','sada dsasd',NULL,'123@gmail.com',324,2),(8,'3',2,'Medicine','2',NULL,'123@gmail.com',3,2),(9,'43',4,'Computer Science','4',NULL,'123@gmail.com',4,4),(10,'r',5,'Computer Science','6','Screenshot_from_2019-07-22_22-39-42.png','123@gmail.com',7,8),(11,'4',4,'Computer Science','3','SNY01993.jpg','123@gmail.com',3,2),(12,'new',8,'Business & Finance','jkhjkhkjh jkhgjhk','book.jpeg','123@gmail.com',89,787),(13,'abc book',5,'Humanities','fgh ghf','0ozxixf6u9931.jpg','abc@gmail.com',45,40);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `user2` int(11) DEFAULT NULL,
  `user2name` varchar(255) DEFAULT NULL,
  `user2college` varchar(255) DEFAULT NULL,
  `user2phone` varchar(255) DEFAULT NULL,
  `seen` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` VALUES (1,'Business & Finance','business_finanace'),(2,'Computer Science','computer_science'),(3,'Medicine','med'),(4,'Social Science','social'),(5,'Humanities','humanities'),(6,'Mathematics','maths'),(7,'Education','education');
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `college` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'pankaj','123@gmail.com',NULL,'kjkhjk','$5$rounds=535000$9hextBhuFH/gcSZz$SosdERPsSHhAuS1VhJz3n.2EL9aUTS71CrMYjxMxRwB'),(2,'yutyutyu','uytuy@uyt.com','5555555555','hgfds','$5$rounds=535000$5ina6zp1yaMTYHwt$En58E2GzYVXfl/i/e0IAKKN29iKTPEVOu35HviaEIO.'),(3,'random user','abc@gmail.com','9898989898','iit k','$5$rounds=535000$e1Wqc8fCFRgZ22W8$6hIkBRDTuxmTXS8D0svqB6uIqjsR8vM8szX07p6/Eg3');
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

-- Dump completed on 2019-08-18 23:17:31
