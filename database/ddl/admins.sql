CREATE TABLE `admins`
(
    `id`            bigint(20) unsigned     NOT NULL AUTO_INCREMENT COMMENT '主键 id',
    `user_id`       bigint(20) unsigned     NOT NULL DEFAULT '0' COMMENT '关联用户id',
    `role`          varchar(255)            NOT NULL DEFAULT 'admin' COMMENT '管理员角色:user,admin',
    `name`          varchar(255)            NOT NULL DEFAULT '' COMMENT '管理员名称',
    `avatar`        varchar(255)            NOT NULL DEFAULT '' COMMENT '管理员头像',
    `sex`           tinyint(3) unsigned     NOT NULL DEFAULT '0' COMMENT '性别:0-未知,1-男,2-女',
    `mobile`        varchar(30)             NOT NULL DEFAULT '' COMMENT '绑定手机',
    `pass_word`     varchar(255)            NOT NULL DEFAULT '' COMMENT '密码',
    `client_driver` text                    NOT NULL COMMENT '客户端信息:浏览器信息',
    `client_type`   tinyint(3) unsigned     NOT NULL DEFAULT '0' COMMENT '客户端类型:0未知,1-WEB,2-WEP,3-APP',
    `lat`           decimal(10, 6) unsigned NOT NULL DEFAULT '0.000000' COMMENT '坐标:纬度',
    `lng`           decimal(10, 6) unsigned NOT NULL DEFAULT '0.000000' COMMENT '坐标:经度',
    `status`        tinyint(3) unsigned     NOT NULL DEFAULT '0' COMMENT '状态:0未知,1-未启用,2-已启用',
    `on_line_time`  datetime                         DEFAULT NULL COMMENT '登录时间',
    `off_line_time` datetime                         DEFAULT NULL COMMENT '登出时间',
    `created_at`    datetime                NOT NULL COMMENT '创建时间|注册时间',
    `updated_at`    datetime                         DEFAULT NULL COMMENT '更新时间',
    `deleted_at`    datetime                         DEFAULT NULL COMMENT '删除时间',
    PRIMARY KEY (`id`) USING BTREE,
    KEY `id` (`id`) USING BTREE,
    KEY `user_id` (`user_id`) USING BTREE,
    KEY `role` (`role`) USING BTREE,
    KEY `id_role` (`id`, `role`) USING BTREE,
    KEY `lat_lng` (`lat`, `lng`) USING BTREE,
    KEY `client_type` (`client_type`) USING BTREE,
    KEY `status` (`status`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = DYNAMIC COMMENT ='管理员表';