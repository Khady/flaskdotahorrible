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

insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (1, "admin", "d033e22ae348aeb5660fc2140aec35850c4da997", "2011-10-09", "tutu", "", 1);
insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (2, "adm", "42ef63e7836ef622d9185c1a456051edf16095cc", "2011-10-09", "toto", "", 1);
insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (3, "user", "12dea96fec20593566ab75692c9949596833adc9", "2011-10-09", "tata", "", 1);
insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (4, "news", "3c6bdcddc94f64bf77deb306aae490a90a6fc300", "2011-10-09", "tata2", "", 1);
insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (5, "guide", "4956faddb70fe7e02e4eff88353ab96e3ee4fb7e", "2011-10-09", "tata3", "", 1);
insert into user_description (id, login, hash, date_create, mail, avatar, valid) values (6, "groupe", "0c52dc77f8a5b2ae6e7c7938521ed5fd26ebb8a8", "2011-10-09", "tata3", "", 1);
