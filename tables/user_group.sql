drop table if exists user_group;
create table user_group (
  id_group integer not null,
  id_user integer not null,
  gadm integer not null
);

insert into user_group (id_group, id_user, gadm) values (1, 1, 0);
insert into user_group (id_group, id_user, gadm) values (2, 2, 0);
insert into user_group (id_group, id_user, gadm) values (3, 3, 0);
insert into user_group (id_group, id_user, gadm) values (4, 4, 0);
insert into user_group (id_group, id_user, gadm) values (5, 5, 0);
insert into user_group (id_group, id_user, gadm) values (6, 6, 0);