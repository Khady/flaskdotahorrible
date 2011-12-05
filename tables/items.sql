drop table if exists items;
create table items (
         id integer primary key autoincrement not null unique,
	 nam varchar not null,
	 price integer not null,
	 recette varchar,
	 use_in varchar,
	 tooltip varchar not null,
	 tooltip_untouch varchar not null,
	 des varchar,
	 categorie varchar not null
);