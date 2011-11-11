drop table if exists commentaire;
create table commentaire (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  id_genre integer not null,
  genre varchar not null,
  autor integer not null,
  content_untouch varchar not null,
  content_markup varchar not null,
  date_create date not null,
  date_last_modif date not null
);