drop table if exists entries;
create table entries (
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
	 reg_life integer,
	 reg_mana integer,
	 orb varchar,
	 aura varchar,
	 cap_pas varchar,
	 cap_act varchar
};