drop table if exists items;
create table items (
         id integer primary key autoincrement not null unique,
	 nam varchar not null,
	 price integer not null,
	 recette varchar,
	 use_in varchar,
	 des varchar,
	 str integer,
	 agi integer,
	 inte integer,
	 armor integer,
	 aspeed integer,
	 ms integer,
	 life integer,
	 mana integer,
	 damages integer,
	 reg_life integer,
	 reg_mana integer,
	 orb varchar,
	 aura varchar,
	 cap_pas varchar,
	 cap_act varchar
);