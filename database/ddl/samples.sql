CREATE TABLE `samples`
(
    `id`         bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 id',
    `user_id`    bigint(20) unsigned DEFAULT NULL COMMENT '外键:user_id',
    `name`       varchar(50)         NOT NULL DEFAULT '' COMMENT '用户昵称',
    `mobile`     varchar(30)         NOT NULL DEFAULT '' COMMENT '绑定手机',
    `photo`      varchar(200)        NOT NULL DEFAULT '' COMMENT '用户头像',
    `sex`        tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '性别: 0未知, 1男, 2女',
    `type`       tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '类型: 0未知, 1-否, 2-是',
    `status`     tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '状态: 1-否, 2-是',
    `created_at` datetime            NOT NULL COMMENT '创建时间|注册时间',
    `updated_at` datetime                     DEFAULT NULL COMMENT '更新时间',
    `deleted_at` datetime                     DEFAULT NULL COMMENT '删除时间',
    PRIMARY KEY (`id`) USING BTREE,
    KEY `id` (`id`) USING BTREE,
    KEY `type` (`type`) USING BTREE,
    KEY `status` (`status`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = DYNAMIC COMMENT ='模板表';