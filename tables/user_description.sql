drop table if exists user_description;
create table user_description (
  id integer primary key autoincrement not null unique,
  login varchar not null,
  hash varchar not null,
  date_create date not null,
  mail varchar not null,
  avatar varchar,
  valid integer not null
);

insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (1, "tutu", "32a89bdcec2d50f9dc9747cd47ecfc14cf9c3dbe", "2011-10-09", "tutu", "", 1);
insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (2, "toto", "0b9c2625dc21ef05f6ad4ddf47c5f203837aa32c", "2011-10-09", "toto", "", 1);
insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (3, "tata", "90795a0ffaa8b88c0e250546d8439bc9c31e5a5e", "2011-10-09", "tata", "", 1);
insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (4, "tata2", "90795a0ffaa8b88c0e250546d8439bc9c31e5a5e", "2011-10-09", "tata2", "", 1);
insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (5, "tata3", "90795a0ffaa8b88c0e250546d8439bc9c31e5a5e", "2011-10-09", "tata3", "", 1);