CREATE TABLE `oauth_clients`
(
    `id`            bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键 id',
    `scope_id`      varchar(255)        NOT NULL DEFAULT '' COMMENT '授权范围-标记: 字符串',
    `client`        varchar(255)        NOT NULL DEFAULT '' COMMENT '授权客户端-描述: 字符串',
    `client_id`     varchar(255)        NOT NULL DEFAULT '' COMMENT '授权客户端-标记: 字符串',
    `client_secret` varchar(255)        NOT NULL DEFAULT '' COMMENT '授权客户端-密匙: 字符串',
    `created_at`    datetime            NOT NULL COMMENT '创建时间',
    `updated_at`    datetime                     DEFAULT NULL COMMENT '更新时间',
    `deleted_at`    datetime                     DEFAULT NULL COMMENT '删除时间',
    PRIMARY KEY (`id`) USING BTREE,
    KEY `id` (`id`) USING BTREE,
    KEY `scope_id` (`scope_id`) USING BTREE,
    KEY `client_id` (`client_id`) USING BTREE,
    KEY `scope_id_client_id` (`scope_id`, `client_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  ROW_FORMAT = DYNAMIC COMMENT ='授权客户端表';