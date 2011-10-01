drop table if exists user_description;
create table user_description (
  id integer primary key autoincrement not null unique,
  login varchar not null,
  hash varchar not null,
  date_create date not null,
  mail varchar not null,
  avatar varchar not null,
  valid integer not null
);