-- mydb.tb_file definition

CREATE TABLE `tb_file` (
  `file_id` char(36) NOT NULL,
  `file_path` varchar(50) DEFAULT NULL,
  `file_name` varchar(50) DEFAULT NULL,
  `file_crtdt` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- mydb.board definition

CREATE TABLE `board` (
  `board_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `board_title` varchar(100) DEFAULT NULL,
  `board_content` varchar(4000) DEFAULT NULL,
  `board_crtdt` datetime DEFAULT CURRENT_TIMESTAMP,
  `board_upddt` datetime DEFAULT NULL,
  `board_deldt` datetime DEFAULT NULL,
  PRIMARY KEY (`board_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;