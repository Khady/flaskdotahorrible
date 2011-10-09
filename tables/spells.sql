drop table if exists spells;
create table spells (
         id integer primary key autoincrement not null unique,
	 name_hero varchar not null,
	 nam varchar not null,
	 des varchar not null,
	 abi_type varchar not null,
	 tar_type varchar not null,
	 allo_tar varchar not null,
	 pos integer
);
drop table if exists spells_effect;
create table spells_effect (
         id integer primary key autoincrement not null unique,
	 id_spell integer not null,
	 lvl_spell integer not null,
	 cd integer,
	 rang integer,
	 mana_cost integer,
	 life_cost integer,
	 aoe integer,
	 effect varchar not null
);