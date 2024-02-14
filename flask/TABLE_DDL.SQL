-- mydb.BOARD definition

CREATE TABLE `BOARD` (
  `board_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `board_title` varchar(100) DEFAULT NULL,
  `board_content` varchar(4000) DEFAULT NULL,
  PRIMARY KEY (`board_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;


-- mydb.TB_FILE definition

CREATE TABLE `TB_FILE` (
  `file_id` char(36) NOT NULL,
  `file_path` varchar(50) DEFAULT NULL,
  `file_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;