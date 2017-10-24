CREATE DATABASE wechat_tool_db;
DROP TABLE IF EXISTS  wechat_users;
CREATE TABLE
  wechat_users
(
  id INT NOT NULL AUTO_INCREMENT COMMENT 'ID',
  username varchar(100) default '' COMMENT'微信用户名字符串',
  nick_name varchar(100) default '' COMMENT '微信昵称',
  back_name varchar(100) default '' COMMENT '群备注昵称',
  group_name varchar(100) default '' COMMENT'群名称',
  wechat_id varchar(100) default '' COMMENT '微信号',
  create_time TIMESTAMP  COMMENT '加入时间',
  invite_num int default 0 COMMENT '邀请人数',
  pid int default 0 COMMENT '被邀请人ID' ,
  master int default 0 COMMENT '管理员id',
  remark varchar(200) COMMENT '备注',
   PRIMARY KEY (id)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微信组邀请表';
CREATE TABLE  wechat_group
(
  id INT NOT NULL AUTO_INCREMENT COMMENT 'ID',
  group_name varchar(100) default '' COMMENT'讨论组名称',
  group_ids varchar(100) default '' COMMENT '讨论组ID,发送信息用',
  owner int default 0 COMMENT '群主ID',
  manager_id int default 0 COMMENT '管理员ID',
  remark varchar(100) default '' COMMENT'其他备注',
   PRIMARY KEY (id)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微信组表';