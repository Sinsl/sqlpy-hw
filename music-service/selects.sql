--Задание 2

--Название и продолжительность самого длительного трека
select t.duration, t.title from track t
order by t.duration desc limit 1

--Название треков, продолжительность которых не менее 3,5 минут
select t.duration, t.title from track t
where t.duration > 210
order by t.duration desc

--Названия сборников, вышедших в период с 2018 по 2020 год включительно.
select c."name", c."year" from collection c
where c."year" >= 2018 and c."year" <= 2020

--Исполнители, чьё имя состоит из одного слова.
select s."name" from singer s
where s."name" not like '% %'

--Название треков, которые содержат слово «мой» или «my», добавила Me
select t.title from track t 
where t.title like '% мой %' or t.title like '% my %' or t.title like '% Me %'

--Задание 3

--Количество исполнителей в каждом жанре.
select g.title, count(sg.singer_id)  from genre g
join singer_genre sg on g.id = sg.genre_id
group by g.title 

--Количество треков, вошедших в альбомы 2019–2020 годов, расширила до 2023 года
select a.title, a.year_release, count(t.id) as count_tracks from album a
join track t on a.id = t.album_id 
where a.year_release >= 2019 and a.year_release <= 2023
group by a.title, a.year_release

--Средняя продолжительность треков по каждому альбому.
select a.title, avg(t.duration) as avg_duration_track from album a
join track t on a.id = t.album_id
group by a.title

--Все исполнители, которые не выпустили альбомы в 2020 году, изменила на 2022
select s."name" from singer s
except
select s2."name" from singer s2
join album_singer as2 on as2.singer_id = s2.id 
join album a on as2.album_id = a.id
where a.year_release in (2022)

--Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами) - Sabaton
select distinct c."name" from collection c
join track_collection tc on tc.collection_id = c.id 
join track t on t.id = tc.track_id
join album a on a.id = t.album_id
join album_singer as2 on as2.album_id = a.id
join singer s on s.id = as2.singer_id
where s."name" = 'Sabaton'