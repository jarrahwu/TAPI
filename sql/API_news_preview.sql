CREATE DATABASE  IF NOT EXISTS `API` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `API`;
-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: API
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `news_preview`
--

DROP TABLE IF EXISTS `news_preview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news_preview` (
  `_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `favor_count` int(11) DEFAULT NULL,
  `comment_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news_preview`
--

LOCK TABLES `news_preview` WRITE;
/*!40000 ALTER TABLE `news_preview` DISABLE KEYS */;
INSERT INTO `news_preview` VALUES (6,'与帅哥合影尽显妩媚','balalal','http://img5.hao123.com/data/3_96e98bfc90b20ae4d9170960b5bc35e5_430',20,50),(7,'这发型谁驾驭得了','balalal','http://img4.hao123.com/data/3_23e6a8bef08f978b56a81b7fb8a12237_430',20,50),(8,'人分两种类型！','balalal','http://img5.hao123.com/data/3_01cfe397bffe316251b3a5a2892f7c33_430',20,50),(9,'与帅哥合影尽显妩媚','balalal','http://img5.hao123.com/data/3_96e98bfc90b20ae4d9170960b5bc35e5_430',20,50),(10,'这发型谁驾驭得了','balalal','http://img4.hao123.com/data/3_23e6a8bef08f978b56a81b7fb8a12237_430',20,50),(11,'人分两种类型！','balalal','http://img5.hao123.com/data/3_01cfe397bffe316251b3a5a2892f7c33_430',20,50),(12,'毕业确实是分手季，今天见一位学长把女朋友卖了','balalal','http://img2.hao123.com/data/3_fc1ed98bc3ecfbad1425023caf076524_430',20,50),(13,'刷新世界观的吃法！瞬间高大上！','asdasda','http://img2.hao123.com/data/3_fc1ed98bc3ecfbad1425023caf076524_430',10,20),(14,'穿越了吗？','asdasda','http://img2.hao123.com/data/3_fc1ed98bc3ecfbad1425023caf076524_430',10,20),(15,'感觉自己萌萌哒！！！！！！！！！','asdasda','http://img1.hao123.com/data/3_542a7d3f4f1891732e5d1453bfa4cbd3_430',10,20),(16,'蜡笔小新离家出走了！','asdasda','http://img6.hao123.com/data/3_b3ec69d8493fc9c54f03c04698ca0d88_0',10,20),(17,'一个纯正的屌丝鉴定完毕','asdasda','http://img2.hao123.com/data/3_631d727ad502c57bc7968e68ec5254df_430',10,20),(18,'姑娘你在干嘛呢！！','asdasda','http://img6.hao123.com/data/3_c7291f60eb30e52ffa956d948c11e7fd_0',10,20),(19,'与帅哥合影尽显妩媚','balalal','http://img5.hao123.com/data/3_96e98bfc90b20ae4d9170960b5bc35e5_430',20,50),(20,'这发型谁驾驭得了','balalal','http://img4.hao123.com/data/3_23e6a8bef08f978b56a81b7fb8a12237_430',20,50),(21,'人分两种类型！','balalal','http://img5.hao123.com/data/3_01cfe397bffe316251b3a5a2892f7c33_430',20,50),(22,'毕业确实是分手季，今天见一位学长把女朋友卖了','balalal','http://img2.hao123.com/data/3_fc1ed98bc3ecfbad1425023caf076524_430',20,50),(23,'刷新世界观的吃法！瞬间高大上！','asdasda','http://img2.hao123.com/data/3_fc1ed98bc3ecfbad1425023caf076524_430',10,20),(24,'穿越了吗？','asdasda','http://img2.hao123.com/data/3_fc1ed98bc3ecfbad1425023caf076524_430',10,20),(25,'感觉自己萌萌哒！！！！！！！！！','asdasda','http://img1.hao123.com/data/3_542a7d3f4f1891732e5d1453bfa4cbd3_430',10,20),(26,'蜡笔小新离家出走了！','asdasda','http://img6.hao123.com/data/3_b3ec69d8493fc9c54f03c04698ca0d88_0',10,20),(27,'一个纯正的屌丝鉴定完毕','asdasda','http://img2.hao123.com/data/3_631d727ad502c57bc7968e68ec5254df_430',10,20),(28,'姑娘你在干嘛呢！！','asdasda','http://img6.hao123.com/data/3_c7291f60eb30e52ffa956d948c11e7fd_0',10,20),(29,'test','test','http://192.168.2.122:8888/image/1d68c6c2-5a8a-4ffe-a7ec-a98371dbce3f.jpg',NULL,NULL),(30,'test','test','http://192.168.2.122:8888/image/f3e31e29-53e5-49bd-b6d7-de5c884328ce.jpg',NULL,NULL),(31,'test','test','http://192.168.2.122:8888/image/ce751272-2e1b-449f-ae3b-c8df89657ea3.jpg',NULL,NULL),(32,'test','test','http://192.168.2.122:8888/image/60f655ca-37b5-4e0b-a383-491d110c7579.jpg',NULL,NULL),(33,'test','test','http://192.168.2.122:8888/image/2fe61c66-ffc2-4bc2-b9a0-c6b9b343d4bb.jpg',NULL,NULL),(34,'test','test','http://192.168.2.122:8888/image/b9d87aa7-a680-45c8-898f-23e70859d044.jpg',NULL,NULL),(35,'test','test','http://192.168.2.122:8888/image/575e502b-ace3-47bb-bbfd-0e88d038fa7a.jpg',NULL,NULL),(36,'test','test','http://192.168.2.122:8888/image/80e2247c-4699-4c68-82d9-3b082aafefbc.jpg',NULL,NULL),(37,'test','test','http://192.168.2.122:8888/image/4edb6304-3694-4b90-9a21-58ec2854fc48.jpg',NULL,NULL),(38,'test','test','http://192.168.2.122:8888/image/5afa4b50-d15e-45a1-8e71-424f3964d270.jpg',NULL,NULL);
/*!40000 ALTER TABLE `news_preview` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-06-01 18:31:22
