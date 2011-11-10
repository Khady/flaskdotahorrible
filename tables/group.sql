drop table if exists groupe;
create table groupe (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  nom varchar not null,
  news integer not null,
  guide integer not null,
  guide_validation integer not null,
  adm integer not null,
  groupe integer not null
);

insert into groupe (nom, news, guide, guide_validation, adm, groupe) values ("adm", 1, 1, 1, 1, 1);
insert into groupe (nom, news, guide, guide_validation, adm, groupe) values ("user", 0, 0, 0, 0, 0);
insert into groupe (nom, news, guide, guide_validation, adm, groupe) values ("gadm", 1, 1, 0, 1, 0);
