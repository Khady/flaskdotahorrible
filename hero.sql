drop table if exists hero;
create table hero (
         id integer primary key autoincrement not null unique,
	 nam varchar not null,
	 typ integer not null,
	 des varchar not null,
	 bio varchar not null,
	 str_start integer not null,
	 agi_start integer not null,
	 int_start integer not null,
	 str_lvl integer not null,
	 agi_lvl integer not null,
	 int_lvl integer not null,
	 life integer not null,
	 mana integer not null,
	 damages varchar not null,
	 range integer not null,
	 cast_speed integer not null,
	 anim_speed integer not null,
	 vision varchar not null,
	 armor integer not null,
	 aspeed integer not null,
	 ms integer not null
);
