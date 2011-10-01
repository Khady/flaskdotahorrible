drop table if exists guide_items;
create table guide_items (
  id_guide INTEGER,
  id_items varchar not null,
  id_categorie integer not null,
  desc_items varchar not null
);