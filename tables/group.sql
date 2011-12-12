drop table if exists groupe;
create table groupe (
  id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE,
  nom varchar not null,
  news integer not null,
  guide integer not null,
  groupe integer not null,
  adm integer not null
);

insert into groupe (nom, news, guide, groupe, adm) values ("admin", 0, 0, 0, 1);
insert into groupe (nom, news, guide, groupe, adm) values ("adm", 1, 1, 1, 1);
insert into groupe (nom, news, guide, groupe, adm) values ("user", 0, 0, 0, 0);
insert into groupe (nom, news, guide, groupe, adm) values ("news", 1, 0, 0, 0);
insert into groupe (nom, news, guide, groupe, adm) values ("guide", 0, 1, 0, 0);
insert into groupe (nom, news, guide, groupe, adm) values ("groupe", 0, 0, 1, 0);
