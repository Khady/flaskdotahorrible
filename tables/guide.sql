drop table if exists guide;
create table guide (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  hero integer not null,
  heroname varchar not null,
  autor integer not null,
  title varchar not null,
  tag varchar,
  difficulties varchar not null,
  content_untouch varchar not null,
  content_markup varchar not null,
  date_create date not null,
  date_last_modif date not null,
  valid integer not null,
  score integer no null
);

drop table if exists guidetmp;
create table guidetmp (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  id_guide integer,
  hero integer not null,
  heroname varchar not null,
  autor integer not null,
  title varchar not null,
  tag varchar,
  difficulties varchar not null,
  content_untouch varchar not null,
  content_markup varchar not null,
  date_create date not null,
  date_last_modif date not null,
  valid integer not null,
  score integer no null
);