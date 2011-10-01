drop table if exists spells;
create table spells (
         id integer primary key autoincrement not null unique,
	 nam varchar not null,
	 des varchar not null,
	 cd integer,
	 range integer,
	 mana_cost integer,
	 life_cost integer,
	 aoe integer,
	 effect varchar not null,
};