-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;
\c tournament;


DROP TABLE IF EXISTS matches cascade;
DROP TABLE IF EXISTS players cascade;


CREATE TABLE players(
    id serial primary key,
    name text
);


CREATE TABLE matches(
    match_id serial primary key,
    winnerid integer references players(id),
    loserid integer references players(id)
);

insert into players values(1,'Chuy Ramirez');
insert into players values(2,'Buddha');
insert into players values(3,'Jesus');
insert into players values(4,'Mohamed');


insert into matches(winnerid,loserid) values(1,2);
insert into matches(winnerid,loserid) values(1,2);
insert into matches(winnerid,loserid) values(1,2);
insert into matches(winnerid,loserid) values(3,2);

create view winnum as select id,name,count(winnerid) as winnum from players left join matches on id = winnerid group by id order by id;

create view totalnum as select id,count(winnerid) as totalnum from players left join matches on id = winnerid or id = loserid group by id order by id;

create view standing as select winnum.id,winnum.name,winnum,totalnum from totalnum left join winnum on winnum.id = totalnum.id order by winnum desc;