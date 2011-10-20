drop table if exists news;
create table news (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  title varchar not null,
  autor integer not null,
  tag varchar,
  content_untouch varchar not null,
  content_markup varchar not null,
  date_create date not null,
  date_last_modif date not null
);