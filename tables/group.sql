drop table if exists groupe;
create table groupe (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  nom varchar not null,
  news integer not null,
  guide integer not null,
  adm integer not null,
  groupe integer not null
);