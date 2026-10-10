CREATE DATABASE IF NOT EXISTS project_db CHARACTER SET utf8;
USE `project_db`;
DROP TABLE IF EXISTS `slides`;
CREATE TABLE `slides` (
  `slides_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '轮播图ID',
  `title` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '标题',
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '内容',
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '链接',
  `img` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '轮播图',
  `hits` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '点击量',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`slides_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='轮播图';
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth` (
  `auth_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '授权ID',
  `user_group` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '用户组',
  `mod_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '模块名',
  `table_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '表名',
  `page_title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '页面标题',
  `path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '路由路径',
  `parent` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '父级菜单',
  `parent_sort` int(10) NOT NULL DEFAULT '0' COMMENT '父级菜单排序',
  `position` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '位置',
  `mode` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '_blank' COMMENT '跳转方式',
  `add` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否可增加',
  `del` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否可删除',
  `set` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否可修改',
  `get` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否可查看',
  `field_add` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '添加字段',
  `field_set` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '修改字段',
  `field_get` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '查询字段',
  `table_nav_name` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '跨表导航名称',
  `table_nav` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '跨表导航',
  `option` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '配置',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`auth_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户权限管理';
DROP TABLE IF EXISTS `upload`;
CREATE TABLE `upload` (
  `upload_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '上传ID',
  `name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '文件名',
  `path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '访问路径',
  `file` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '文件路径',
  `display` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '显示顺序',
  `father_id` int(11) DEFAULT '0' COMMENT '父级ID',
  `dir` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '文件夹',
  `type` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '文件类型',
  PRIMARY KEY (`upload_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='文件上传';
insert into `upload` values ('1','movie.mp4','/upload/movie.mp4','',null,'0',null,'video');
DROP TABLE IF EXISTS `message_inform`;
CREATE TABLE `message_inform` (
  `message_inform_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '通知ID',
  `user_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '通知人ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `state` varchar(255) DEFAULT NULL COMMENT '状态',
  `type` varchar(64) DEFAULT NULL COMMENT '分类',
  `content` varchar(255) DEFAULT NULL COMMENT '内容',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`message_inform_id`) USING BTREE,
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='通知记录';
DROP TABLE IF EXISTS `private_message`;
CREATE TABLE `private_message` (
  `private_message_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '私信ID',
  `sender_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '发送人ID',
  `receiver_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '接收人ID',
  `conversation_key` varchar(64) NOT NULL DEFAULT '' COMMENT '会话键',
  `content` text COMMENT '消息内容',
  `is_read` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已读',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`private_message_id`) USING BTREE,
  KEY `sender_id` (`sender_id`),
  KEY `receiver_id` (`receiver_id`),
  KEY `conversation_key` (`conversation_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='私信消息';
DROP TABLE IF EXISTS `sensitive_vocabulary`;
CREATE TABLE `sensitive_vocabulary` (
  `sensitive_vocabulary_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '敏感词汇ID',
  `sensitive_vocabulary` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '敏感词汇',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`sensitive_vocabulary_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='敏感词汇';
DROP TABLE IF EXISTS `user_group`;
CREATE TABLE `user_group` (
  `group_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户组ID',
  `display` smallint(4) unsigned NOT NULL DEFAULT '100' COMMENT '显示顺序',
  `name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '名称',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '描述',
  `source_table` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '来源表',
  `source_field` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '来源字段',
  `source_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '来源ID',
  `register` smallint(1) unsigned DEFAULT '0' COMMENT '注册位置',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`group_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户组';
DROP TABLE IF EXISTS `history`;
CREATE TABLE `history` (
  `history_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '浏览历史ID',
  `user_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '浏览人ID',
  `source_table` varchar(255) DEFAULT NULL COMMENT '来源表',
  `source_field` varchar(255) DEFAULT NULL COMMENT '来源字段',
  `source_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '来源ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `img` varchar(255) DEFAULT NULL COMMENT '封面',
  `type` varchar(64) DEFAULT NULL COMMENT '分类',
  `path` varchar(255) DEFAULT NULL COMMENT '路由',
  `params` text COMMENT '参数',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`history_id`) USING BTREE,
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='浏览记录';
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `article_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT COMMENT '文章id',
  `title` varchar(125) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '标题',
  `type` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '文章分类',
  `hits` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '点击数',
  `praise_len` int(11) NOT NULL DEFAULT '0' COMMENT '点赞数',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '来源',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '来源地址',
  `tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '标签',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '正文',
  `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '封面图',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '文章描述',
  PRIMARY KEY (`article_id`,`title`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='文章';
DROP TABLE IF EXISTS `access_token`;
CREATE TABLE `access_token` (
  `token_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '临时访问牌ID',
  `token` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '临时访问牌',
  `info` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '信息',
  `maxage` int(2) NOT NULL DEFAULT '2' COMMENT '最大寿命：默认2小时',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `user_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '用户编号',
  PRIMARY KEY (`token_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='登陆访问时长';
DROP TABLE IF EXISTS `code_token`;
CREATE TABLE `code_token` (
  `code_token_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '验证码ID',
  `token` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL COMMENT '令牌',
  `code` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL COMMENT '验证码',
  `expire_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '失效时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`code_token_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=COMPACT COMMENT='验证码';
DROP TABLE IF EXISTS `collect`;
CREATE TABLE `collect` (
  `collect_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '收藏ID',
  `user_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '收藏人ID',
  `source_table` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '来源表',
  `source_field` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '来源字段',
  `source_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '来源ID',
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '标题',
  `img` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '封面',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`collect_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='收藏';
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice` (
  `notice_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT COMMENT '公告ID',
  `title` varchar(125) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '标题',
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '正文',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`notice_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='公告';
insert into `notice` values ('1','系统维护通知','<p>网站升级通知</p><p>尊敬的客户，为了提供更好的用户体验，我们将于本周三凌晨1:00-5:00进行系统维护升级，期间可能出现短暂服务中断。建议您提前保存操作数据，感谢您的理解与支持！</p>','2026-04-14 22:53:07','2026-04-14 22:53:07');
insert into `notice` values ('2','新功能上线','<p>搜索功能已优化升级！现已正式开放使用，支持关键词搜索，快去体验检索服务吧~</p>','2026-04-14 22:53:07','2026-04-14 22:53:07');
insert into `notice` values ('3','客服时间调整','<p>人工客服服务时间已延长为每日8:00-22:00（含节假日），智能客服24小时在线，随时为您解答问题。</p>','2026-04-14 22:53:07','2026-04-14 22:53:07');
insert into `notice` values ('4','规范提示','<p>请遵守《用户行为守则》：禁止发布广告、虚假信息及不当内容。共同维护友善的网络环境，违规账号将受到限制。</p>','2026-04-14 22:53:07','2026-04-14 22:53:07');
DROP TABLE IF EXISTS `article_type`;
CREATE TABLE `article_type` (
  `type_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `display` smallint(4) unsigned NOT NULL DEFAULT '100' COMMENT '显示顺序',
  `name` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '分类名称',
  `father_id` smallint(5) unsigned NOT NULL DEFAULT '0' COMMENT '上级分类ID',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '描述',
  `icon` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '分类图标',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '外链地址',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`type_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='文章分类';
DROP TABLE IF EXISTS `follow`;
CREATE TABLE `follow` (
  `follow_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户关注ID',
  `follower_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '关注人ID',
  `follower_avatar` varchar(255) DEFAULT NULL COMMENT '关注人头像',
  `follower_nickname` varchar(255) DEFAULT NULL COMMENT '关注人昵称',
  `followed_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '被关注人ID',
  `followed_avatar` varchar(255) DEFAULT NULL COMMENT '被关注人头像',
  `followed_nickname` varchar(255) DEFAULT NULL COMMENT '被关注人昵称',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`follow_id`) USING BTREE,
  KEY `followed_id` (`followed_id`),
  KEY `follower_id` (`follower_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='用户关注';
DROP TABLE IF EXISTS `operation_log`;
CREATE TABLE `operation_log` (
  `operation_log_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '操作日志ID',
  `user_group` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '用户角色',
  `user_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '用户账号',
  `routes` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '模块名称',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`operation_log_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='操作日志表';
DROP TABLE IF EXISTS `praise`;
CREATE TABLE `praise` (
  `praise_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '点赞ID',
  `user_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '点赞人',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `source_table` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '来源表',
  `source_field` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '来源字段',
  `source_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '来源ID',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '点赞状态:1为点赞，0已取消',
  `img` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`praise_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='点赞';
DROP TABLE IF EXISTS `hits`;
CREATE TABLE `hits` (
  `hits_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '点赞ID',
  `user_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '点赞人',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `source_table` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '来源表',
  `source_field` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '来源字段',
  `source_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '来源ID',
  PRIMARY KEY (`hits_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户点击';
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment` (
  `comment_id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '评论ID',
  `user_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '评论人ID',
  `reply_to_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '回复评论ID',
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '内容',
  `nickname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '头像地址',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `source_table` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '来源表',
  `source_field` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '来源字段',
  `source_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '来源ID',
  `hidden` tinyint(4) DEFAULT '0' COMMENT '是否隐藏',
  `sticky` tinyint(4) DEFAULT '0' COMMENT '是否置顶',
  PRIMARY KEY (`comment_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='评论';
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(8) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `state` smallint(1) unsigned NOT NULL DEFAULT '1' COMMENT '账户状态：(1可用|2异常|3已冻结|4已注销)',
  `user_group` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '所在用户组',
  `login_time` timestamp NULL DEFAULT NULL COMMENT '上次登录时间',
  `phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '手机号码',
  `username` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '用户名',
  `nickname` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '昵称',
  `password` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '密码',
  `email` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '邮箱',
  `avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '头像地址',
  `open_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '针对获取用户信息字段',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `vip_level` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '会员等级',
  `vip_discount` double(10,2) DEFAULT '0.00' COMMENT '会员折扣',
  `integral` int(11) DEFAULT '0' COMMENT '积分',
  `balance` double(10,2) DEFAULT '0.00' COMMENT '余额',
  `ip` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'IPv4/IPv6地址',
  `device_hash` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '设备指纹',
  `emergency_name` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '紧急联系人',
  `emergency_mobile` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '紧急联系电话',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户账户';
insert into `user` values ('1','1','管理员','2025-10-09 09:20:03.0',null,'0','admin','admin','bfd59291e825b5f2bbf1eb76569f8fe7','','0','/api/upload/admin_avatar.jpg',null,'2026-04-14 22:53:07',null,'0.0','0','0.0',null,null,null,null);
ALTER TABLE `user` DROP COLUMN balance;
ALTER TABLE `user` DROP COLUMN integral;
ALTER TABLE `user` DROP COLUMN vip_level;
ALTER TABLE `user` DROP COLUMN vip_discount;
ALTER TABLE `user` DROP COLUMN ip;
ALTER TABLE `user` DROP COLUMN device_hash;
ALTER TABLE `user` DROP COLUMN emergency_name;
ALTER TABLE `user` DROP COLUMN emergency_mobile;
UPDATE `user` SET password = 'asd123';
UPDATE user SET avatar = '/static/upload/admin_avatar.jpg';
DROP TABLE IF EXISTS `ordinary_user`;
CREATE TABLE `ordinary_user`(ordinary_user_id int(11) NOT NULL AUTO_INCREMENT COMMENT '普通用户ID',
`user_name` varchar(64) comment '用户姓名',
`users_mobile_phone` varchar(16) comment '用户手机',
`examine_state` varchar(16) DEFAULT '已通过' NOT NULL comment '审核状态',
`user_id` int(11) DEFAULT '0' NOT NULL comment '用户ID',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`create_by` int(11) DEFAULT '1' NOT NULL comment '创建用户ID',
`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (ordinary_user_id))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 comment '普通用户';
insert into `ordinary_user` values (1,'赵磊','13700137000','已通过',2,'2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into user(user_group,username,nickname,password,avatar) values ('普通用户','yonghu1','yonghu1','asd123','/static/upload/default_avatar.jpg');
insert into `ordinary_user` values (2,'黄俊','15500155000','已通过',3,'2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into user(user_group,username,nickname,password,avatar) values ('普通用户','yonghu2','yonghu2','asd123','/static/upload/default_avatar.jpg');
insert into `ordinary_user` values (3,'周涛','13400134000','已通过',4,'2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into user(user_group,username,nickname,password,avatar) values ('普通用户','yonghu3','yonghu3','asd123','/static/upload/default_avatar.jpg');

DROP TABLE IF EXISTS `compileors`;
CREATE TABLE `compileors`(compileors_id int(11) NOT NULL AUTO_INCREMENT COMMENT '编辑人员ID',
`user_name` varchar(64) comment '用户姓名',
`users_phone` varchar(16) comment '用户手机',
`examine_state` varchar(16) DEFAULT '已通过' NOT NULL comment '审核状态',
`user_id` int(11) DEFAULT '0' NOT NULL comment '用户ID',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`create_by` int(11) DEFAULT '1' NOT NULL comment '创建用户ID',
`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (compileors_id))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 comment '编辑人员';
insert into `compileors` values (1,'陈静','13400134000','已通过',5,'2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into user(user_group,username,nickname,password,avatar) values ('编辑人员','yonghu4','yonghu4','asd123','/static/upload/default_avatar.jpg');
insert into `compileors` values (2,'林娜','15900159000','已通过',6,'2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into user(user_group,username,nickname,password,avatar) values ('编辑人员','yonghu5','yonghu5','asd123','/static/upload/default_avatar.jpg');
insert into `compileors` values (3,'徐强','13900139000','已通过',7,'2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into user(user_group,username,nickname,password,avatar) values ('编辑人员','yonghu6','yonghu6','asd123','/static/upload/default_avatar.jpg');


DROP TABLE IF EXISTS `news_class_nameification`;
CREATE TABLE `news_class_nameification`(news_class_nameification_id int(11) NOT NULL AUTO_INCREMENT COMMENT '新闻分类ID',
`news_categories` varchar(64) comment '新闻分类',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`create_by` int(11) DEFAULT '1' NOT NULL comment '创建用户ID',
`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (news_class_nameification_id))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 comment '新闻分类';
-- 标准十类（与爬虫 classify_news_category / CANONICAL_NEWS_CATEGORIES 一致）
insert into `news_class_nameification` values (1,'时政','2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into `news_class_nameification` values (2,'国际','2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into `news_class_nameification` values (3,'社会','2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into `news_class_nameification` values (4,'科技','2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into `news_class_nameification` values (5,'健康','2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into `news_class_nameification` values (6,'教育','2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into `news_class_nameification` values (7,'文化','2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into `news_class_nameification` values (8,'娱乐','2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into `news_class_nameification` values (9,'财经','2026-04-14 22:53:07',1,'2026-04-14 22:53:07');
insert into `news_class_nameification` values (10,'军事','2026-04-14 22:53:07',1,'2026-04-14 22:53:07');

DROP TABLE IF EXISTS `news_resources`;
CREATE TABLE `news_resources`(news_resources_id int(11) NOT NULL AUTO_INCREMENT COMMENT '新闻资源ID',
`title` text comment '标题',
`url` text comment '详情链接',
`img` text comment '图片链接',
`read_num` text comment '阅读量',
`origin` text comment '发布来源',
`release_time` text comment '发布时间',
`content` text comment '正文内容',
`comment_num` text comment '评论数量',
`comment` text comment '最新评论',
`unique_id` varchar(64) DEFAULT '' NOT NULL COMMENT '唯一ID',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`create_by` int(11) DEFAULT '1' NOT NULL comment '创建用户ID',
`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (news_resources_id))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 comment '新闻资源';
insert into `news_resources` values (1,'标题1','www.xn---xn--mpr-mj4mo970b.org','图片链接1','阅读量1','发布来源1','发布时间1','正文内容1','评论数量1','最新评论1','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (2,'标题2','www.xn---xn--o74a-u46py286b.org','图片链接2','阅读量2','发布来源2','发布时间2','正文内容2','评论数量2','最新评论2','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (3,'标题3','www.xn---xn--vc7a-uo23a141b.io','图片链接3','阅读量3','发布来源3','发布时间3','正文内容3','评论数量3','最新评论3','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (4,'标题4','www.xn---xn--x8s-9b5qz156b.org','图片链接4','阅读量4','发布来源4','发布时间4','正文内容4','评论数量4','最新评论4','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (5,'标题5','www.xn---xn--mrv-mn6o159e.co','图片链接5','阅读量5','发布来源5','发布时间5','正文内容5','评论数量5','最新评论5','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (6,'标题6','www.xn---xn--wou-n00oj44h.biz','图片链接6','阅读量6','发布来源6','发布时间6','正文内容6','评论数量6','最新评论6','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (7,'标题7','www.xn---xn--nfv-xc6tw04q.info','图片链接7','阅读量7','发布来源7','发布时间7','正文内容7','评论数量7','最新评论7','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (8,'标题8','www.xn---xn--2u1a-f07ro011b.name','图片链接8','阅读量8','发布来源8','发布时间8','正文内容8','评论数量8','最新评论8','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (9,'标题9','www.xn---xn--y7y-v47vy51h.net','图片链接9','阅读量9','发布来源9','发布时间9','正文内容9','评论数量9','最新评论9','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (10,'标题10','www.xn---xn--674a-9y5v.org','图片链接10','阅读量10','发布来源10','发布时间10','正文内容10','评论数量10','最新评论10','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (11,'标题11','www.xn---xn--dz1a-uk2rt81n.co','图片链接11','阅读量11','发布来源11','发布时间11','正文内容11','评论数量11','最新评论11','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_resources` values (12,'标题12','www.xn---xn--qby-mn6o159e.name','图片链接12','阅读量12','发布来源12','发布时间12','正文内容12','评论数量12','最新评论12','','2026-04-14 22:53:08',1,'2026-04-14 22:53:08');

DROP TABLE IF EXISTS `news_information`;
DROP TABLE IF EXISTS `news_source`;
CREATE TABLE `news_source`(
`news_source_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '新闻源ID',
`code` varchar(64) NOT NULL DEFAULT '' COMMENT '来源编码',
`name` varchar(128) NOT NULL DEFAULT '' COMMENT '来源名称',
`enabled` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否启用',
`source_type` varchar(32) NOT NULL DEFAULT 'builtin' COMMENT '来源类型',
`base_url` varchar(255) DEFAULT '' COMMENT '基础地址',
`list_urls` text COMMENT '列表地址',
`parser_type` varchar(32) NOT NULL DEFAULT 'builtin' COMMENT '解析器类型',
`parser_name` varchar(64) DEFAULT '' COMMENT '解析器名称',
`interval_minutes` int(11) NOT NULL DEFAULT '30' COMMENT '抓取频率',
`priority` int(11) NOT NULL DEFAULT '50' COMMENT '优先级',
`extra_json` text COMMENT '扩展配置',
`last_run_at` datetime DEFAULT NULL COMMENT '最近抓取时间',
`last_status` varchar(32) DEFAULT '' COMMENT '最近状态',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`create_by` int(11) DEFAULT '1' NOT NULL COMMENT '创建用户ID',
`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (`news_source_id`),
UNIQUE KEY `uniq_news_source_code` (`code`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '新闻源配置';
insert into `news_source` values
(1,'tencent','腾讯新闻',1,'builtin','https://news.qq.com/','https://news.qq.com/','builtin','tencent',30,90,'{"origin_name":"腾讯新闻"}',null,'','2026-04-28 15:00:00',1,'2026-04-28 15:00:00'),
(2,'people','人民网',1,'builtin','http://www.people.com.cn/','','builtin','people',30,92,'{"origin_name":"人民网","list_seeds":"","rss_feeds":"","people_use_rss":false}',null,'','2026-04-28 15:00:00',1,'2026-04-28 15:00:00'),
(3,'xinhuanet','新华社',1,'builtin','http://www.news.cn/','http://www.news.cn/','builtin','xinhuanet',30,94,'{"origin_name":"新华社"}',null,'','2026-04-28 15:00:00',1,'2026-04-28 15:00:00'),
(4,'chinanews','中国新闻网',1,'builtin','https://www.chinanews.com.cn/','https://www.chinanews.com.cn/','builtin','chinanews',30,88,'{"origin_name":"中国新闻网"}',null,'','2026-04-28 15:00:00',1,'2026-04-28 15:00:00');
DROP TABLE IF EXISTS `crawl_run`;
CREATE TABLE `crawl_run`(
`crawl_run_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '抓取运行ID',
`run_id` varchar(64) NOT NULL DEFAULT '' COMMENT '运行批次ID',
`source_code` varchar(64) NOT NULL DEFAULT '' COMMENT '来源编码',
`source_name` varchar(128) DEFAULT '' COMMENT '来源名称',
`status` varchar(32) NOT NULL DEFAULT 'running' COMMENT '状态',
`fetched_count` int(11) NOT NULL DEFAULT '0' COMMENT '抓取数',
`written_count` int(11) NOT NULL DEFAULT '0' COMMENT '写入数',
`dropped_count` int(11) NOT NULL DEFAULT '0' COMMENT '过滤数',
`error_message` text COMMENT '错误信息',
`summary` text COMMENT '摘要',
`started_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
`finished_at` datetime DEFAULT NULL COMMENT '结束时间',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`create_by` int(11) DEFAULT '1' NOT NULL COMMENT '创建用户ID',
`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (`crawl_run_id`),
KEY `idx_crawl_run_source_code` (`source_code`),
KEY `idx_crawl_run_status` (`status`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '抓取运行记录';
CREATE TABLE `news_information`(news_information_id int(11) NOT NULL AUTO_INCREMENT COMMENT '新闻资讯ID',
`news_headlines` varchar(64) comment '新闻标题',
`publication_date` date comment '发布日期',
`news_pictures` varchar(255) comment '新闻图片',
`news_categories` varchar(64) comment '新闻分类',
`news_description` text comment '新闻描述',
`news_body` longtext comment '新闻正文',
`hits` int(11) DEFAULT 0 NOT NULL comment '点击数',
`praise_len` int(11) DEFAULT 0 NOT NULL comment '点赞数',
`collect_len` int(11) DEFAULT 0 NOT NULL comment '收藏数',
`comment_len` int(11) DEFAULT 0 NOT NULL comment '评论数',
`recommend` int(11) DEFAULT '0' NOT NULL comment '智能推荐',
`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`create_by` int(11) DEFAULT '1' NOT NULL comment '创建用户ID',
`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
PRIMARY KEY (news_information_id))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 comment '新闻资讯';
insert into `news_information` values (1,'生物多样性保护成全球焦点','2026-04-14','/static/upload/1856978491182940160.jpg','军事','新闻描述1','此处可上传文字、图片、视频、超链接等内容区1',320,389,778,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (2,'远程办公趋势改变城市发展','2026-04-14','/static/upload/1856978528151535617.jpg','健康','新闻描述2','此处可上传文字、图片、视频、超链接等内容区2',102,453,256,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (3,'青年创业者引领社会创新浪潮','2026-04-14','/static/upload/1856978379278909441.jpg','娱乐','新闻描述3','此处可上传文字、图片、视频、超链接等内容区3',643,808,954,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (4,'教育科技投资持续升温','2026-04-14','/static/upload/1856978467233464320.jpg','社会','新闻描述4','此处可上传文字、图片、视频、超链接等内容区4',760,753,793,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (5,'5G网络覆盖推动智能家居普及','2026-04-14','/static/upload/1856978514557796353.jpg','财经','新闻描述5','此处可上传文字、图片、视频、超链接等内容区5',875,275,174,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (6,'全球供应链面临重构挑战','2026-04-14','/static/upload/1856978455967563777.jpg','科技','新闻描述6','此处可上传文字、图片、视频、超链接等内容区6',533,225,568,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (7,'虚拟现实技术重塑娱乐体验','2026-04-14','/static/upload/1856978430650744833.jpg','教育','新闻描述7','此处可上传文字、图片、视频、超链接等内容区7',717,306,156,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (8,'新能源汽车销量创新高','2026-04-14','/static/upload/1856978478948155392.jpg','娱乐','新闻描述8','此处可上传文字、图片、视频、超链接等内容区8',685,187,97,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (9,'数字货币监管政策出台','2026-04-14','/static/upload/1856978444382896129.jpg','时政','新闻描述9','此处可上传文字、图片、视频、超链接等内容区9',202,149,891,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (10,'全球气候变化峰会即将召开','2026-04-14','/static/upload/1856978501664505857.jpg','文化','新闻描述10','此处可上传文字、图片、视频、超链接等内容区10',968,251,140,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (11,'太空探索公司计划火星任务','2026-04-14','/static/upload/1856978389701754881.jpg','社会','新闻描述11','此处可上传文字、图片、视频、超链接等内容区11',479,522,34,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');
insert into `news_information` values (12,'AI技术革新医疗行业','2026-04-14','/static/upload/1856978366977015808.jpg','时政','新闻描述12','此处可上传文字、图片、视频、超链接等内容区12',759,285,800,0,0,'2026-04-14 22:53:08',1,'2026-04-14 22:53:08');

insert into `auth` values ('1','管理员','普通用户','ordinary_user','普通用户','/ordinary_user/table','','0','','_blank','1','1','1','1','user_name,users_mobile_phone','user_name,users_mobile_phone','user_name,users_mobile_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('2','管理员','普通用户','ordinary_user','用户详情','/ordinary_user/view','','0','','_blank','1','1','1','1','user_name,users_mobile_phone','user_name,users_mobile_phone','user_name,users_mobile_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('3','管理员','编辑人员','compileors','编辑人员','/compileors/table','','0','','_blank','1','1','1','1','user_name,users_phone','user_name,users_phone','user_name,users_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('4','管理员','编辑人员','compileors','人员详情','/compileors/view','','0','','_blank','1','1','1','1','user_name,users_phone','user_name,users_phone','user_name,users_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('5','管理员','新闻分类','news_class_nameification','新闻分类','/news_class_nameification/table','','0','','_blank','1','1','1','1','news_categories','news_categories','news_categories',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('6','管理员','新闻分类','news_class_nameification','分类详情','/news_class_nameification/view','','0','','_blank','1','1','1','1','news_categories','news_categories','news_categories',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('7','管理员','新闻爬虫','news_resources','新闻爬虫','/news_resources/table','','0','','_blank','0','1','1','1','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('8','管理员','新闻爬虫','news_resources','资源详情','/news_resources/view','','0','','_blank','0','1','1','1','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('122','管理员','抓取运行记录','crawl_run','抓取运行记录','/crawl_run/table','','0','','_blank','0','0','1','1','run_id,source_code,source_name,status,fetched_count,written_count,dropped_count,error_message,started_at,finished_at','run_id,source_code,source_name,status,fetched_count,written_count,dropped_count,error_message,started_at,finished_at','run_id,source_code,source_name,status,fetched_count,written_count,dropped_count,error_message,started_at,finished_at',null,'0','{}','2026-04-28 15:00:00.0','2026-04-28 15:00:00.0');
insert into `auth` values ('123','管理员','抓取运行记录','crawl_run','抓取运行详情','/crawl_run/view','','0','','_blank','0','0','1','1','run_id,source_code,source_name,status,fetched_count,written_count,dropped_count,error_message,started_at,finished_at','run_id,source_code,source_name,status,fetched_count,written_count,dropped_count,error_message,started_at,finished_at','run_id,source_code,source_name,status,fetched_count,written_count,dropped_count,error_message,started_at,finished_at',null,'0','{}','2026-04-28 15:00:00.0','2026-04-28 15:00:00.0');
insert into `auth` values ('9','管理员','新闻发布','news_information','新闻资讯','/news_information/table','','0','','_blank','1','1','1','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{"can_show_comment":true}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('10','管理员','新闻发布','news_information','资讯详情','/news_information/view','','0','','_blank','1','1','1','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('11','管理员','新闻发布','news_information','新闻资讯','/news_information/list','','0','top','_blank','1','1','1','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('12','管理员','新闻发布','news_information','资讯详情','/news_information/details','','0','','_blank','1','1','1','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{"can_comment":true,"can_show_comment":true}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('13','管理员','热点专题','article','热点新闻','/article/table','','0','','_blank','1','1','1','1','','','',null,'0','{"print":true,"export_db":true,"import_db":true}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('14','管理员','热点专题','article','新闻详情','/article/view','','0','','_blank','1','1','1','1','','','',null,'0','{"print":true}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('15','管理员','热点专题','article','热点新闻','/article/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('16','管理员','热点专题','article','新闻详情','/article/details','','0','','_blank','1','1','1','1','','','',null,'0','{"can_comment":true,"can_show_comment":true}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('17','管理员','专题分类','article_type','新闻分类','/article_type/table','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('18','管理员','专题分类','article_type','分类详情','/article_type/view','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('19','管理员','最新公告','notice','最新公告','/notice/table','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('20','管理员','最新公告','notice','公告详情','/notice/view','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('21','管理员','最新公告','notice','最新公告','/notice/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('22','管理员','最新公告','notice','公告详情','/notice/details','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('23','管理员','我的收藏','collect','收藏记录','/collect/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('24','管理员','我的点赞','praise','点赞记录','/praise/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('25','管理员','评论','comment','评论管理','/comment/table','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('26','管理员','评论','comment','评论详情','/comment/view','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('27','管理员','评论','comment','我的评论','/comment/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('28','管理员','评论','comment','评论详情','/comment/details','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('29','游客','普通用户','ordinary_user','普通用户','/ordinary_user/table','','0','','_blank','1','0','0','0','user_name,users_mobile_phone','user_name,users_mobile_phone','user_name,users_mobile_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('30','游客','普通用户','ordinary_user','用户详情','/ordinary_user/view','','0','','_blank','1','0','0','0','user_name,users_mobile_phone','user_name,users_mobile_phone','user_name,users_mobile_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('31','游客','编辑人员','compileors','编辑人员','/compileors/table','','0','','_blank','1','0','0','0','user_name,users_phone','user_name,users_phone','user_name,users_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('32','游客','编辑人员','compileors','人员详情','/compileors/view','','0','','_blank','1','0','0','0','user_name,users_phone','user_name,users_phone','user_name,users_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('33','游客','新闻分类','news_class_nameification','新闻分类','/news_class_nameification/table','','0','','_blank','0','0','0','0','news_categories','news_categories','news_categories',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('34','游客','新闻分类','news_class_nameification','分类详情','/news_class_nameification/view','','0','','_blank','0','0','0','0','news_categories','news_categories','news_categories',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('35','游客','新闻爬虫','news_resources','新闻爬虫','/news_resources/table','','0','','_blank','0','0','0','0','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('36','游客','新闻爬虫','news_resources','资源详情','/news_resources/view','','0','','_blank','0','0','0','0','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('37','游客','新闻发布','news_information','新闻资讯','/news_information/table','','0','','_blank','0','0','0','0','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{"can_show_comment":false}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('38','游客','新闻发布','news_information','资讯详情','/news_information/view','','0','','_blank','0','0','0','0','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('39','游客','新闻发布','news_information','新闻资讯','/news_information/list','','0','top','_blank','0','0','0','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('40','游客','新闻发布','news_information','资讯详情','/news_information/details','','0','','_blank','0','0','0','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{"can_comment":false,"can_show_comment":false}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('41','游客','热点专题','article','热点新闻','/article/table','','0','','_blank','0','0','0','0','','','',null,'0','{"print":false,"export_db":false,"import_db":false}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('42','游客','热点专题','article','新闻详情','/article/view','','0','','_blank','0','0','0','0','','','',null,'0','{"print":false}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('43','游客','热点专题','article','热点新闻','/article/list','','0','','_blank','0','0','0','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('44','游客','热点专题','article','新闻详情','/article/details','','0','','_blank','0','0','0','1','','','',null,'0','{"can_comment":false,"can_show_comment":false}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('45','游客','专题分类','article_type','新闻分类','/article_type/table','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('46','游客','专题分类','article_type','分类详情','/article_type/view','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('47','游客','最新公告','notice','最新公告','/notice/table','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('48','游客','最新公告','notice','公告详情','/notice/view','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('49','游客','最新公告','notice','最新公告','/notice/list','','0','','_blank','0','0','0','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('50','游客','最新公告','notice','公告详情','/notice/details','','0','','_blank','0','0','0','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('51','游客','我的收藏','collect','收藏记录','/collect/list','','0','','_blank','0','0','0','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('52','游客','我的点赞','praise','点赞记录','/praise/list','','0','','_blank','0','0','0','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('53','游客','评论','comment','评论管理','/comment/table','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('54','游客','评论','comment','评论详情','/comment/view','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('55','游客','评论','comment','我的评论','/comment/list','','0','','_blank','0','0','0','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('56','游客','评论','comment','评论详情','/comment/details','','0','','_blank','0','0','0','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('57','普通用户','普通用户','ordinary_user','普通用户','/ordinary_user/table','','0','','_blank','0','0','0','0','user_name,users_mobile_phone','user_name,users_mobile_phone','user_name,users_mobile_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('58','普通用户','普通用户','ordinary_user','用户详情','/ordinary_user/view','','0','','_blank','0','0','1','1','user_name,users_mobile_phone','user_name,users_mobile_phone','user_name,users_mobile_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('59','普通用户','编辑人员','compileors','编辑人员','/compileors/table','','0','','_blank','0','0','0','0','user_name,users_phone','user_name,users_phone','user_name,users_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('60','普通用户','编辑人员','compileors','人员详情','/compileors/view','','0','','_blank','0','0','0','0','user_name,users_phone','user_name,users_phone','user_name,users_phone',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('61','普通用户','新闻分类','news_class_nameification','新闻分类','/news_class_nameification/table','','0','','_blank','0','0','0','0','news_categories','news_categories','news_categories',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('62','普通用户','新闻分类','news_class_nameification','分类详情','/news_class_nameification/view','','0','','_blank','0','0','0','0','news_categories','news_categories','news_categories',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('63','普通用户','新闻爬虫','news_resources','新闻爬虫','/news_resources/table','','0','','_blank','0','0','0','0','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('64','普通用户','新闻爬虫','news_resources','资源详情','/news_resources/view','','0','','_blank','0','0','0','0','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('65','普通用户','新闻发布','news_information','新闻资讯','/news_information/table','','0','','_blank','0','0','0','0','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{"can_show_comment":false}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('66','普通用户','新闻发布','news_information','资讯详情','/news_information/view','','0','','_blank','0','0','0','0','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('67','普通用户','新闻发布','news_information','新闻资讯','/news_information/list','','0','top','_blank','1','1','1','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('68','普通用户','新闻发布','news_information','资讯详情','/news_information/details','','0','','_blank','1','1','1','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{"can_comment":true,"can_show_comment":true}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('69','普通用户','热点专题','article','热点新闻','/article/table','','0','','_blank','0','0','0','0','','','',null,'0','{"print":false,"export_db":false,"import_db":false}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('70','普通用户','热点专题','article','新闻详情','/article/view','','0','','_blank','0','0','0','0','','','',null,'0','{"print":false}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('71','普通用户','热点专题','article','热点新闻','/article/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('72','普通用户','热点专题','article','新闻详情','/article/details','','0','','_blank','1','1','1','1','','','',null,'0','{"can_comment":true,"can_show_comment":true}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('73','普通用户','专题分类','article_type','新闻分类','/article_type/table','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('74','普通用户','专题分类','article_type','分类详情','/article_type/view','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('75','普通用户','最新公告','notice','最新公告','/notice/table','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `auth` values ('76','普通用户','最新公告','notice','公告详情','/notice/view','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('77','普通用户','最新公告','notice','最新公告','/notice/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('78','普通用户','最新公告','notice','公告详情','/notice/details','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('79','普通用户','我的收藏','collect','收藏记录','/collect/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('80','普通用户','我的点赞','praise','点赞记录','/praise/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('81','普通用户','评论','comment','评论管理','/comment/table','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('82','普通用户','评论','comment','评论详情','/comment/view','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('83','普通用户','评论','comment','我的评论','/comment/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('84','普通用户','评论','comment','评论详情','/comment/details','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('85','编辑人员','普通用户','ordinary_user','普通用户','/ordinary_user/table','','0','','_blank','0','0','0','0','user_name,users_mobile_phone','user_name,users_mobile_phone','user_name,users_mobile_phone',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('86','编辑人员','普通用户','ordinary_user','用户详情','/ordinary_user/view','','0','','_blank','0','0','0','0','user_name,users_mobile_phone','user_name,users_mobile_phone','user_name,users_mobile_phone',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('87','编辑人员','编辑人员','compileors','编辑人员','/compileors/table','','0','','_blank','0','0','0','0','user_name,users_phone','user_name,users_phone','user_name,users_phone',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('88','编辑人员','编辑人员','compileors','人员详情','/compileors/view','','0','','_blank','0','0','1','1','user_name,users_phone','user_name,users_phone','user_name,users_phone',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('89','编辑人员','新闻分类','news_class_nameification','新闻分类','/news_class_nameification/table','','0','','_blank','0','0','0','0','news_categories','news_categories','news_categories',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('90','编辑人员','新闻分类','news_class_nameification','分类详情','/news_class_nameification/view','','0','','_blank','0','0','0','0','news_categories','news_categories','news_categories',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('91','编辑人员','新闻爬虫','news_resources','新闻爬虫','/news_resources/table','','0','','_blank','0','1','1','1','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('92','编辑人员','新闻爬虫','news_resources','资源详情','/news_resources/view','','0','','_blank','0','1','1','1','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment','title,url,img,read_num,origin,release_time,content,comment_num,comment',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('93','编辑人员','新闻发布','news_information','新闻资讯','/news_information/table','','0','','_blank','1','1','1','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{"can_show_comment":true}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('94','编辑人员','新闻发布','news_information','资讯详情','/news_information/view','','0','','_blank','1','1','1','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('95','编辑人员','新闻发布','news_information','新闻资讯','/news_information/list','','0','top','_blank','1','1','1','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('96','编辑人员','新闻发布','news_information','资讯详情','/news_information/details','','0','','_blank','1','1','1','1','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body','news_headlines,publication_date,news_pictures,news_categories,news_description,news_body',null,'0','{"can_comment":true,"can_show_comment":true}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('97','编辑人员','热点专题','article','热点新闻','/article/table','','0','','_blank','1','1','1','1','','','',null,'0','{"print":true,"export_db":true,"import_db":true}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('98','编辑人员','热点专题','article','新闻详情','/article/view','','0','','_blank','1','1','1','1','','','',null,'0','{"print":true}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('99','编辑人员','热点专题','article','热点新闻','/article/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('100','编辑人员','热点专题','article','新闻详情','/article/details','','0','','_blank','1','1','1','1','','','',null,'0','{"can_comment":true,"can_show_comment":true}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('101','编辑人员','专题分类','article_type','新闻分类','/article_type/table','','0','','_blank','1','0','0','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('102','编辑人员','专题分类','article_type','分类详情','/article_type/view','','0','','_blank','1','0','0','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('103','编辑人员','最新公告','notice','最新公告','/notice/table','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('104','编辑人员','最新公告','notice','公告详情','/notice/view','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('105','编辑人员','最新公告','notice','最新公告','/notice/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('106','编辑人员','最新公告','notice','公告详情','/notice/details','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('107','编辑人员','我的收藏','collect','收藏记录','/collect/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('108','编辑人员','我的点赞','praise','点赞记录','/praise/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('109','编辑人员','评论','comment','评论管理','/comment/table','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('110','编辑人员','评论','comment','评论详情','/comment/view','','0','','_blank','0','0','0','0','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('111','编辑人员','评论','comment','我的评论','/comment/list','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `auth` values ('112','编辑人员','评论','comment','评论详情','/comment/details','','0','','_blank','1','1','1','1','','','',null,'0','{}','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `user_group` values ('1','100','管理员',null,'','','0','0','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `user_group` values ('2','100','游客',null,'','','0','0','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `user_group` values ('3','100','普通用户',null,'ordinary_user','ordinary_user_id','0','3','2026-04-14 22:53:08.0','2026-04-14 22:53:08.0');
insert into `user_group` values ('4','100','编辑人员',null,'compileors','compileors_id','0','0','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
ALTER TABLE `comment` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE;
ALTER TABLE `collect` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE;
ALTER TABLE `praise` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE;
insert into `slides` values ('1','轮播图1','内容1','https://www.baidu.com','/static/upload/1970780152262557696.jpg','472','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `slides` values ('2','轮播图2','内容2','https://www.163.com','/static/upload/1970780152145117184.jpg','495','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `slides` values ('3','轮播图3','内容3','https://www.jd.com','/static/upload/1970780152287723521.jpg','886','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
insert into `article` values ('1','重庆通报燃气企业收费问题调查情况 拟处罚金810万元并问责责任人','新闻news','148','0','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0',null,null,null,'<p>2025-02-15 08:35:02</p><p><br></p><p>新华社重庆2月14日电（记者 田金文）14日，重庆市市场监督管理局发布《重庆燃气集团燃气收费问题调查情况通报》称，2025年1月起，有市民反映重庆燃气集团燃气收费异常情况，重庆市相关部门成立调查组调查发现，该企业存在抄表周期混乱、违规估抄、错抄、抄表力量配备不足等问题，涉及侵犯消费者合法权益；未发现乱涨价、燃气表计量失准、燃气质量、远程操控改变燃气表计量和换表导致气费上涨等问题。</p><p>通报显示，调查组在调查核查过程中，督促企业受理办结投诉举报7198件，入户核查用户1073户，分析企业数据2.4亿余条。经查，2024年4月查处重庆燃气集团多计多收燃气费问题以来，该企业未深刻汲取教训，落实整改责任不到位，整改工作流于形式、推进不力，目前仍然存在抄表周期混乱、违规估抄、错抄等问题。</p><p>通报称，重庆燃气集团落实相关制度不到位，损害了群众利益，违反了相关法规，重庆市市场监管部门拟依法对其从重处罚，责令其立即整改，拟处罚金810万元。调查组已将相关情况通报该企业上级单位，责令其深入开展内部调查，严肃问责处理相关责任人，并成立专项工作组入驻重庆燃气集团开展为期3个月的专项整治，督促指导整改工作全面彻底落实。</p>','/static/upload/1891667250537037824.jpg',null);
insert into `article` values ('2','中新网评：从指尖入心间，发出主流舆论最强音','新闻news','630','0','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0',null,null,null,'<p>发布于：2025-02-18 09:33</p><p><br></p><p>	站在人类文明演进的坐标轴上，网络正能量不是简单的信息传递，而是数字时代集体智慧的结晶。光纤中流淌的不仅是0和1的代码，更是人性温度与文明的火种。</p><p>	在浩瀚的网络世界，多种声音交织激荡，如何让中国声音更加洪亮悦耳，让昂扬奋进的大国形象更加立体全面。</p><p>	由中央网信办主办的2024中国正能量网络精品征集展播活动已启动网络展播投票，时间为2月15日至2月21日，投票结果将作为中国正能量网络精品遴选的重要参考。</p><p>	当万象更新的时序更迭流转，网络正能量的故事始终相伴，与我们共同走过四季轮转。</p><p>	向善舆论场，网络正能量勾画多维图景。</p><p>	嫦娥六号带回月球背面样品，中国航天探索之路越走越远；过境免签政策放宽，中国以更开放的姿态迎接世界游客；川藏、青藏公路建成通车70周年，天路铸就高原传奇；深中通道拉近距离和人心，中国基建再创奇迹。</p><p>	走过不平凡的2024年，我国经济实力、科技实力、综合国力持续增强，中国式现代化迈出新的坚实步伐，标注着中国号巨轮的壮阔航程，见证着亿万人民的拼搏奋斗。这些印记不仅是中国发展的见证，更是中华民族精神的体现。</p><p>	能量转化论，让数字脉冲传递现实动能。</p><p><br></p>','/static/upload/1891667900293447681.jpg',null);
insert into `article` values ('3','新华视点丨“哪吒”破圈背后的中国IP成功密码','新闻news','839','0','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0',null,null,null,'<p>2025年02月18日 00:20:08</p><h6><br></h6><p>新华社北京2月17日电<strong>题：“哪吒”破圈背后的中国IP成功密码</strong></p><p><br></p><p>如同踩上风火轮，上映以来的《哪吒2》票房屡破纪录。中国影史票房第一名、迈入10亿美元门槛、突破百亿元、跻身全球票房榜前十名……每一次数字的变化，都在见证新的历史。</p><p>海外的浪潮接续而来。</p><p class="ql-align-center"><br></p><p class="ql-align-center">2月8日，人们在美国洛杉矶举行的《哪吒之魔童闹海》北美首映礼上举起电影海报。新华社发（曾慧摄）</p><p>当地时间2月13日，电影《哪吒2》在澳大利亚上映，14日正式登陆北美市场。负责《哪吒2》海外发行的华人影业相关负责人介绍，该片在北美地区排片总数突破770间，仅预售票房就超越了近20年华语片首周末票房。</p><p>根据美国康姆斯科分析公司的数据，《哪吒2》闯入最新的北美周末票房榜前五；周末三天预估票房收入达721万美元，创近年来中国国产电影北美首周末票房最高纪录。</p><p>与中国电影人有超过十年合作经历的好莱坞制片人罗伯特·金说，《哪吒2》是大片级别的动画片，吸引了众多观众，影院中的年轻人非常多，表明近年来中国电影在“讲好故事”方面有了长足进步。</p><p>事实上，从影视内容到网络游戏、网络文学、短视频，越来越多中国IP走热，初步形成更为市场化、规模化、年轻化的出海新生态。</p><p>《纽约时报》注意到，除了《哪吒2》这部电影，中国传统文化也激发了其他娱乐形式的突破。在电子游戏领域，改编自《西游记》的《黑神话：悟空》游戏去年甫一推出即大获成功。</p><p>在中央文化和旅游管理干部学院副研究员孙佳山看来，经过十余年的跨越式发展，我国文化产业的IP模式日渐成熟，逐渐形成综合性的IP矩阵，在海外产生更大影响力。</p><p>出海“破圈”的中国IP，都有哪些共同特征与成功密码？</p>','/static/upload/1891668101339021312.jpg',null);
insert into `article` values ('4','《中国新闻出版广电报》2024年度优秀畅销书排行榜总榜发布','新闻news','179','0','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0',null,null,null,'<p>发表时间：2024-12-28</p><p><br></p><p>每一本好书，都是浩瀚宇宙里的闪亮星辰。在书中，我们品读思想的深邃、精神的伟力。</p><p><br></p><p>《中国新闻出版广电报》2024年度优秀畅销书排行榜，依托月度优秀畅销书排行榜，同时参照本报《读周刊》微信公众号“好书品读”月度书榜、科普书榜、童书榜、绘本榜等书单，在2023年11月至2024年12月出版的图书中产生。</p><p><br></p><p>共推荐 2024年度优秀畅销书排行榜总榜图书50种，社科、文学、经管、少儿、科技生活五大分榜图书各40种。总榜、分榜各书顺序，基本依照出版时间排列。</p><p><br></p><p>纵观《中国新闻出版广电报》年度优秀畅销书，呈现出以下鲜明特点：反映时代精神，紧贴社会热点；沉入生活深处，呈现史诗巨变；展现前沿科技，提升科学素养；汇集名家名作，用心用情书写。</p><p><br></p><p>2024年，我们在文字的旷野里驰骋，阅见2025年，阅见美好的未来。</p>','/static/upload/1891667548986933248.jpg',null);
insert into `article` values ('5','借短视频之力，吉林冰雪旅游“燃爆”冬日文旅圈','新闻news','895','0','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0',null,null,null,'<p class="ql-align-justify">在文旅市场竞争白热化的当下，吉林冰雪旅游成功“破圈”，成为这个冬日现象级的旅游热点，为全国文旅产业发展提供了创新范本。其凭借与短视频深度融合的营销策略，在流量、目的地、美食、行业等多个维度强势出圈，不仅让“到吉林玩雪”的口号传遍大江南北，更实现了旅游产业的全方位发展。</p><p class="ql-align-justify">流量出圈，营销数据见证传播热度</p><p class="ql-align-justify">短视频时代，流量是文旅产业发展的关键。吉林文旅精准把握这一趋势，以“整个世界在吉林”为主题开展种草活动，引发流量狂欢。截至1月11日，该活动在抖音播放量突破10亿，众多达人团队纷纷前往打卡。由明星艺人、奥运冠军、头部KOL领衔，联合大量优质腰部KOL和KOC组成的超强营销天团，通过创作极具吸引力的短视频，在网络上掀起传播热潮。</p><p class="ql-align-justify"><br></p><p class="ql-align-justify">无忧传媒旗下的“不吃奶露拖”与吉林本地达人董赤赤在长春冰雪新天地拍摄的视频，点赞近400万。视频中，网红达人们在雪地里的欢乐场景，搭配绚丽烟花，通过短视频广泛传播，极大激发了网友的旅行热情。同时，众多带有吉林冰雪元素的话题持续霸屏抖音热榜，“长春冰雪新天地先卷起来了”在抖音种草榜排名第三，“用我的滑板鞋打开长白山滑雪”排名第八。春节期间，借助短视频平台的传播优势，吉林冰雪旅游相关话题持续发酵，更多游客在社交媒体分享自己的春节冰雪之旅，特色民俗活动、绚丽冰雪夜景等内容吸引大量关注，流量与话题热度持续攀升。</p><p class="ql-align-justify"><br></p><p class="ql-align-justify">流量与热度共舞，游客量大幅增长</p><p class="ql-align-justify">流量的爆发直接带动了吉林各热门旅游目的地的火爆。长春冰雪新天地和长白山凭借丰富的旅游资源和强大的营销热度，在各大榜单长时间霸榜。“嗨玩长春冰雪新天地”“来延吉做公主”“滑粉雪度假”等热门项目吸引大量游客。从流量数据来看，吉林冰雪旅游相关内容在社交媒体平台的话题讨论量数以千万计，游客的分享进一步扩大了吉林的影响力。</p><p><br></p>','/static/upload/1891667000166449152.jpg',null);
insert into `article` values ('6','中国朝鲜族民俗园登上抖音元宵节热榜第四名','新闻news','132','0','2026-04-14 22:53:09.0','2026-04-14 22:53:09.0',null,null,null,'<p>2025-02-17 12:06</p><p>吉林</p><p>近日，中国朝鲜族民俗园在抖音元宵节话题热度榜上表现亮眼，其所在话题#最强元宵气氛组登上种草榜第四名。</p><p>2月12日至13日，该话题的播放量超过458.8万，显示出其广泛的关注度和影响力。</p><p><br></p><p>元宵节期间，中国朝鲜族民俗园举办了丰富多彩的民俗活动，吸引了众多游客参与。活动包括“福满上元”民俗巡游、</p><p><br></p><p>免费品尝聪耳酒和五谷饭、月亮房祈福等。游客们与表演者一起载歌载舞，沉浸式体验朝鲜族传统文化的独特魅力。</p><p><br></p><p>作为延边州文化旅游的重要名片，中国朝鲜族民俗园凭借其独特的文化底蕴和吸引力，赢得了国内外游客的广泛好评。</p><p><br></p><p>近年来，该园区屡获殊荣，曾入围第三批国家级夜间文化和旅游消费集聚区名单，并被评为文化创意赋能吉林文旅产业高质量发展十佳案例之一。</p><p><br></p><p>此外，中国朝鲜族民俗园还登上了抖音用户欢迎的10大景区榜单以及去哪儿网热门“沉浸式”景区排行榜前十名。</p><p><br></p>','/static/upload/1891666755613360128.jpg',null);
insert into `article_type` values ('1','100','新闻news','0',null,null,null,'2026-04-14 22:53:09.0','2026-04-14 22:53:09.0');
