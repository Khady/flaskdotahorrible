drop table if exists spells;
create table spells (
         id integer primary key autoincrement not null unique,
	 name_hero varchar not null,
	 nam varchar not null,
	 tooltip varchar not null,
	 tooltip_untouch varchar not null,
	 pos integer,
	 des integer
);
