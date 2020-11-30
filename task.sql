/*
 Navicat Premium Data Transfer

 Source Server         : s70-mysql
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : s70:3306
 Source Schema         : python-tool

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 30/11/2020 14:20:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `em` varchar(50) DEFAULT '' COMMENT 'em',
  `city` varchar(50) DEFAULT '' COMMENT '城市',
  `room` varchar(50) DEFAULT '' COMMENT '房间',
  `date` date DEFAULT NULL COMMENT '预订的日期',
  `start_time` time DEFAULT NULL COMMENT '开始时间',
  `end_time` time DEFAULT NULL COMMENT '结束时间',
  `pwd` varchar(50) DEFAULT '' COMMENT '密码',
  `account` varchar(50) DEFAULT '' COMMENT '账号',
  `status_text` varchar(255) DEFAULT '未开始',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `status_text` (`status_text`),
  KEY `em` (`em`)
) ENGINE=InnoDB AUTO_INCREMENT=371 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
