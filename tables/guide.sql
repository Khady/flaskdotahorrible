drop table if exists guide;
create table guide (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  hero integer not null,
  autor integer not null,
  title varchar not null,
  tag varchar,
  difficulties varchar not null,
  content_untouch varchar not null,
  content_markup varchar not null,
  date_create date not null,
  date_last_modif date not null,
  score integer
);