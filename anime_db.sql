drop table if exists anime;
drop table if exists brand;
drop table if exists actor;
drop table if exists originwriter;
drop table if exists director;
drop table if exists openingsong;
drop table if exists endingsong;
drop table if exists songer;
drop table if exists broadcaster;
drop table if exists broadcast_time;
drop table if exists users;
drop table if exists userreview;
drop table if exists userhighlight;

create table anime(
	anime_id int(6), title varchar(40), about varchar(500), 
	brand_id int(6), actor_id int(6), writer_id int(6), 
	director_id int(6), op_id int(6), ed_id int(6), 
	official_page varchar(2083), official_twitter varchar(2083), 
	PRIMARY KEY(anime_id)
);
create table brand(
	brand_id int(6), name varchar(20), 
	PRIMARY KEY(brand_id), 
	FOREIGN KEY(brand_id) REFERENCES anime(brand_id)
);
create table actor(
	actor_id int(6), name varchar(20), 
	PRIMARY KEY(actor_id), 
	FOREIGN KEY(actor_id) REFERENCES anime(actor_id)
); 
create table originwriter(
	writer_id int(6), name varchar(20), 
	PRIMARY KEY(writer_id), 
	FOREIGN KEY(writer_id) REFERENCES anime(writer_id)
);
create table director(
	director_id int(6), name varchar(20), 
	PRIMARY KEY(director_id), 
	FOREIGN KEY(director_id) REFERENCES anime(director_id)
);
create table openingsong(
	op_id int(6), name varchar(20), songer_id int(6), 
	PRIMARY KEY(op_id), 
	FOREIGN KEY(op_id) REFERENCES anime(op_id)
);
create table endingsong(
	ed_id int(6), name varchar(20), songer_id int(6), 
	PRIMARY KEY(ed_id), 
	FOREIGN KEY(ed_id) REFERENCES anime(ed_id)
);
create table songer(
	songer_id int(6), name varchar(20), 
	PRIMARY KEY(songer_id), 
	FOREIGN KEY(songer_id) REFERENCES openingsong(songer_id)
);
create table broadcaster(
	broadcaster_id int(6), name varchar(20), 
	PRIMARY KEY(broadcaster_id), 
	FOREIGN KEY(broadcaster_id) REFERENCES anime(broadcaster_id)
);
create table broadcast_time(
	anime_id int(6), broadcaster_id int(6), time varchar(20), 
	PRIMARY KEY(anime_id, broadcaster_id), 
	FOREIGN KEY(anime_id) REFERENCES anime(anime_id)
);
create table users(
	uid int(10), user_name varchar(10), pass_hash varchar(20), 
	PRIMARY KEY(uid)
);
create table userreview(
	uid int(10), anime_id int(6), tokuten int(3), 
	tourokubi unsigned, hitokoto varchar(200), 
	PRIMARY KEY(anime_id, uid)
);
create table userhighlight(
	uid int(10), anime_id int(6), broadcaster_id int(6), 
	PRIMARY KEY(uid, anime_id, broadcaster_id)
);
