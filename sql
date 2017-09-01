CREATE TABLE `osu_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` char(13) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `pc` char(15) DEFAULT NULL,
  `ranked_score` char(15) DEFAULT NULL,
  `total_score` char(15) DEFAULT NULL,
  `pp_rank` char(10) DEFAULT NULL,
  `level` float(10,4) DEFAULT NULL,
  `pp_raw` float(10,4) DEFAULT NULL,
  `acc` float(10,4) DEFAULT NULL,
  `country` char(5) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`username`),
  KEY `idx_pp` (`pp_raw`)
) ENGINE=InnoDB AUTO_INCREMENT=279086 DEFAULT CHARSET=utf8
