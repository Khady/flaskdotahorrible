drop table if exists guide;
create table guide (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  hero integer not null,
  autor integer not null,
  title varchar not null,
  tag varchar,
  difficulties varchar not null,
  spells varchar not null,
  skill1 varchar not null,
  skill2 varchar not null,
  skill3 varchar not null,
  skill4 varchar not null,
  content varchar not null
);