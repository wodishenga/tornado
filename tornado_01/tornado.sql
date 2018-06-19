drop database tornado;
create database tornado charset=utf8;
use tornado;
create table it_user_info(
 	ui_user_id bigint unsigned auto_increment primary key  comment '用户id',
 	ui_name varchar(64) not null comment '用户名',
 	ui_passwd varchar(128) not null comment '密码',
 	ui_age int  unsigned comment '年龄',
 	ui_mobile char(11) not null unique comment '手机号',
 	ui_avatar varchar(128) null comment '头像',
 	ui_ctime datetime not null default current_timestamp comment '创建时间',
 	ui_utime datetime not null default current_timestamp  on update current_timestamp comment '更新时间'

)engine=InnoDB default charset=utf8 comment '用户表';

create table it_house_info(
 	hi_house_id bigint unsigned auto_increment primary key  comment '房屋id',
 	hi_user_id bigint unsigned not null comment '用户ID',
 	hi_name varchar(64) not null comment '房屋名',
 	hi_address varchar(256) not null comment '房屋地址',
 	hi_price int unsigned not null comment '房屋价格',
 	hi_ctime datetime not null default current_timestamp comment '创建时间',
 	hi_utime datetime not null default current_timestamp  on update current_timestamp comment '更新时间',
 	foreign key(hi_user_id) references it_user_info(ui_user_id)
)engine=InnoDB default charset=utf8 comment '房屋信息表';

create table it_house_image(
 	hi_image_id bigint unsigned auto_increment primary key  comment '图片id',
 	hi_house_id bigint unsigned comment '房屋id',
 	hi_url varchar(128) not null comment '图片url',
 	hi_ctime datetime not null default current_timestamp comment '创建时间',
 	hi_utime datetime not null default current_timestamp  on update current_timestamp comment '更新时间',
 	foreign key(hi_house_id) references it_house_info(hi_house_id)
)engine=InnoDB default charset=utf8 comment '房屋图片';
