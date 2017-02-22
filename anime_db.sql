drop table if exists anime;
drop table if exists brand;
drop table if exists actor;
drop table if exists originwriter;
drop table if exists director;
drop table if exists openingsong;
drop table if exists endingsong;
drop table if exists singer;
drop table if exists broadcaster;
drop table if exists broadcast_time;
drop table if exists users;
drop table if exists userreview;
drop table if exists userhighlight;

create table anime(
	anime_id int, title varchar(40), about varchar(500), 
	brand_id int, writer_id int, 
	director_id int, op_id int, ed_id int, 
	official_page varchar(2083), official_twitter varchar(2083), 
	PRIMARY KEY(anime_id)
);
create table brand(
	brand_id int AUTO_INCREMENT, name varchar(20), 
	PRIMARY KEY(brand_id)
);
create table anime_actor(
	anime_id int, actor_id int,
	PRIMARY KEY(anime_id, actor_id)
);
create table actor(
	actor_id int AUTO_INCREMENT, name varchar(20), 
	PRIMARY KEY(actor_id)
); 
create table originwriter(
	writer_id int AUTO_INCREMENT, name varchar(20), 
	PRIMARY KEY(writer_id)
);
create table director(
	director_id int AUTO_INCREMENT, name varchar(20), 
	PRIMARY KEY(director_id)
);
create table openingsong(
	op_id int AUTO_INCREMENT, name varchar(20), singer_id int, 
	PRIMARY KEY(op_id)
);
create table endingsong(
	ed_id int AUTO_INCREMENT, name varchar(20), singer_id int, 
	PRIMARY KEY(ed_id)
);
create table singer(
	singer_id int AUTO_INCREMENT, name varchar(20), 
	PRIMARY KEY(singer_id)
);
create table broadcaster(
	broadcaster_id int, name varchar(20), 
	PRIMARY KEY(broadcaster_id)
);
create table broadcast_time(
	anime_id int, broadcaster_id int, dayofweek varchar(20), time varchar(20), 
	PRIMARY KEY(anime_id, broadcaster_id)
);
create table users(
	uid int(10) AUTO_INCREMENT, user_name varchar(10), pass_hash varchar(20), 
	PRIMARY KEY(uid)
);
create table userreview(
	uid int(10), anime_id int, tokuten int, 
	tourokubi int, hitokoto varchar(200), 
	PRIMARY KEY(anime_id, uid)
);
create table userhighlight(
	uid int(10), anime_id int, broadcaster_id int, 
	PRIMARY KEY(uid, anime_id, broadcaster_id)
);

insert into broadcaster values (02, "NHK Eテレ");
insert into broadcaster values (04, "日本テレビ");
insert into broadcaster values (05, "テレビ朝日");
insert into broadcaster values (06, "TBS");
insert into broadcaster values (07, "テレビ東京");
insert into broadcaster values (08, "フジテレビ");
insert into broadcaster values (09, "TOKYO MX");
insert into broadcaster values (10, "AT-X");

