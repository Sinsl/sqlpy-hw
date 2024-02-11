CREATE TABLE collection (
id serial PRIMARY KEY,
name varchar(50) not NULL,
YEAR integer
)

create table album (
id serial PRIMARY KEY,
title varchar(100) not null,
year_release integer not null
)

create table track (
id serial primary key,
title varchar(100) not null,
duration integer,
album_id integer references album(id)
)

create table track_collection (
track_id integer references track(id),
collection_id integer references collection(id),
primary key (track_id, collection_id)
)

create table singer (
id serial primary key,
name varchar(50) not null
)

create table genre (
id serial primary key,
title varchar(50)
)

create table album_singer (
album_id integer references album(id),
singer_id integer references singer(id),
primary key (album_id, singer_id)
)

create table singer_genre (
singer_id integer references singer(id),
genre_id integer references genre(id),
primary key (singer_id, genre_id)
)
