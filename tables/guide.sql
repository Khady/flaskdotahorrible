drop table if exists guide;
create table guide (
  id INTEGER  NOT NULL,
  guide_id integer,
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
  score integer no null,
  PRIMARY KEY (id, guide_id)
);
