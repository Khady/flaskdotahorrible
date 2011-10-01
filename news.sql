drop table if exists news;
create table news (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  title varchar not null,
  autor integer not null,
  date_create date not null,
  tag varchar
);