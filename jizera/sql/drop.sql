-- coding: utf-8 --

begin transaction;

-- Wywalamy poprzednie tabelki.
drop table if exists tube_data;
drop table if exists meteor_data;
drop table if exists bortle_data;
drop table if exists dslr_data;
drop table if exists sqm_data;
drop table if exists locations;
drop table if exists reviews;
drop table if exists observers;
drop table if exists observations;

commit;
