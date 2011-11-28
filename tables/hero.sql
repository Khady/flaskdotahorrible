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
	 str_lvl float not null,
	 agi_lvl float not null,
	 int_lvl float not null,
	 life integer not null,
	 mana integer not null,
	 damages varchar not null,
	 range integer not null,
	 cast_speed varchar not null,
	 anim_speed varchar not null,
	 vision varchar not null,
	 armor float not null,
	 aspeed float not null,
	 ms integer not null
);
insert into hero (nam, typ, des, bio, str_start, agi_start, int_start, str_lvl, agi_lvl, int_lvl, life, mana, damages, range, cast_speed, anim_speed, vision, armor, aspeed, ms) values ('Lina', 3, 'radiant', 'The sibling rivalries between Lina the Slayer, and her younger sister Rylai, the Crystal Maiden, were the stuff of legend in the temperate region where they spent their quarrelsome childhoods together. Lina always had the advantage, however, for while Crystal was guileless and naive, Lina''s fiery ardor was tempered by cleverness and conniving. The exasperated parents of these incompatible offspring went through half a dozen homesteads, losing one to fire, the next to ice, before they realized life would be simpler if the children were separated. As the oldest, Lina was sent far south to live with a patient aunt in the blazing Desert of Misrule, a climate that proved more than comfortable for the fiery Slayer. Her arrival made quite an impression on the somnolent locals, and more than one would-be suitor scorched his fingers or went away with singed eyebrows, his advances spurned. Lina is proud and confident, and nothing can dampen her flame.', 18, 16, 24, 1.5, 1.5, 3.2, 400, 400, '37-55', 625, '0.45/1.08', '0.75/0.78', '1800/800', 1.24, 1.7, 295);