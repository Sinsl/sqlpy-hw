insert into singer (name)
values ('Sabaton'), ('Rammstein'), ('Metallica'), ('Scorpions')

insert into album (title, year_release)
values ('Attero Dominatus', 2006), ('The Art of War', 2008), ('The War to End All Wars', 2022), 
('Mutter', 2001), ('Zeit', 2022),
('Metallica', 1991), ('72 Seasons', 2023),
('Crazy World', 1990), ('Rock Believer', 2022)

insert into album_singer (album_id, singer_id)
values (1, 1), (2, 1), (3, 1), (4, 2), (5, 2), (6, 3), (7, 3), (8, 4), (9, 4)

insert into genre (title)
values ('hard-rock'), ('ballades'), ('heavy-metal'), ('industrial-metal')

insert into singer_genre (singer_id, genre_id)
values (1, 3), (2, 4), (2, 1), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2)

insert  into track (title, duration, album_id)
values ('Attero Dominatus', 223, 1), ('Rise of Evil', 499, 1),
('Ghost Division', 231, 2), ('Panzerkampf', 351, 2),
('Versailles', 254, 3), ('Hellfighters', 206, 3),
('Mein Herz brennt', 280, 4), ('Rein, raus', 191, 4),
('Zeit', 321, 5), ('Zick Zack', 244, 5),
('Nothing Else Matters', 387, 6), ('The Unforgiven', 386, 6),
('72 Seasons', 459, 7), ('You Must Burn!', 423, 7),
('Wind of Change', 313, 8), ('Send Me an Angel', 273, 8),
('Rock Believer', 237, 9), ('Peacemaker', 177, 9)

insert into collection (name, year)
values ('Ballades', 2020), ('Metal', 2023), ('Old', 2023), ('New', 2023)

insert  into track_collection (track_id, collection_id)
values (11, 1), (15, 1),
(1, 2), (4, 2), (9, 2), (18, 2),
(2, 3), (1, 3), (7, 3), (8, 3), (11, 3), (12, 3),
(5, 4), (6, 4), (9, 4), (10, 4), (13, 4), (14, 4)