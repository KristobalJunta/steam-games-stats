CREATE TABLE games(
id integer primary key,
appid integer unsigned,
title text
);
CREATE TABLE points(
id integer primary key,
game_id integer unsigned,
hours integer unsigned,
timestamp text
);
