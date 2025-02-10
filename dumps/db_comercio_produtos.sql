-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: db_comercio
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` text NOT NULL,
  `preco` decimal(15,2) NOT NULL,
  `estoque` int(11) NOT NULL,
  `categoria` enum('Bebidas','Doces','Salgados','Padaria','Mercearia') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
INSERT INTO `produtos` VALUES (1,'Coca Cola 2L',13.00,984,'Bebidas'),(2,'Conquista 2L',6.00,1000,'Bebidas'),(3,'Pão francês  (Uni.)',0.90,1000,NULL),(4,'Pão de forma panco (500g)',9.90,500,'Padaria'),(5,'Brahma lata 350ml (Uni.)',5.00,1000,'Bebidas'),(6,'Skol lata 350ml (Uni.)',5.00,999,'Bebidas'),(7,'Antártica lata 350ml (Uni.)',5.00,1000,'Bebidas'),(8,'Crystal lata 350ml (Uni.)',3.50,1000,'Bebidas'),(9,'Caixinha de Crystal (12x) ',42.00,1000,'Bebidas'),(10,'Caixinha de Brahma (12x) ',60.00,1000,'Bebidas'),(11,'Caixinha de Skol (12x) ',60.00,1000,'Bebidas'),(12,'Caixinha de Antártica (12x) ',60.00,1000,'Bebidas'),(13,'Leite 1L',6.50,1000,'Bebidas'),(14,'Sonho de padaria (Creme e outros)',4.50,1000,'Padaria'),(15,'Rosca doce (Creme e outros)',9.90,1000,'Doces'),(16,'Coxinha',6.00,1000,'Salgados'),(17,'Esfirra',6.00,1000,'Salgados');
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-10 12:46:25
