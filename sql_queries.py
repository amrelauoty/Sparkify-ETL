# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES



user_table_create = ("""
create table if not exists users(
    user_id int primary key not null, 
    first_name varchar, 
    last_name varchar, 
    gender char(1), 
    level varchar
    )
""")

song_table_create = ("""
create table if not exists songs(
    song_id varchar primary key not null, 
    title varchar not null, 
    artist_id varchar, 
    year int, 
    duration numeric not null
)
""")

artist_table_create = ("""
create table if not exists artists(
    artist_id varchar primary key not null, 
    name varchar not null, 
    location varchar, 
    latitude double precision, 
    longitude double precision
)
""")

time_table_create = ("""
create table if not exists time(
    start_time timestamp primary key not null, 
    hour int, 
    day int, 
    week int, 
    month int, 
    year int, 
    weekday int
)
""")

songplay_table_create = ("""
create table if not exists songplays(
    songplay_id serial primary key not null, 
    start_time timestamp not null, 
    user_id int not null, 
    level varchar, 
    song_id varchar, 
    artist_id varchar, 
    session_id varchar, 
    location varchar, 
    user_agent varchar,
    CONSTRAINT fk_time
      FOREIGN KEY(start_time) 
	  REFERENCES time(start_time),
    CONSTRAINT fk_songs
      FOREIGN KEY(song_id)
      REFERENCES songs(song_id),
    CONSTRAINT fk_artists
      FOREIGN KEY(artist_id)
      REFERENCES artists(artist_id),
    CONSTRAINT fk_users
      FOREIGN KEY(user_id)
      REFERENCES users(user_id)

    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
insert into songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
values(%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT
DO NOTHING
""")

user_table_insert = ("""
insert into users(user_id, first_name, last_name, gender, level)
values(%s,%s,%s,%s,%s)
ON CONFLICT (user_id) DO UPDATE
SET level = EXCLUDED.level
""")

song_table_insert = ("""
insert into songs(song_id, title, artist_id, year, duration)
values(%s,%s,%s,%s,%s)
ON CONFLICT (song_id)
DO NOTHING
""")

artist_table_insert = ("""
insert into artists(artist_id, name, location, latitude, longitude)
values(%s,%s,%s,%s,%s)
ON CONFLICT (artist_id)
DO NOTHING
""")


time_table_insert = ("""
insert into time(start_time, hour, day, week, month, year, weekday)
values(%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (start_time)
DO NOTHING
""")

# FIND SONGS

song_select = ("""
select songs.song_id, artists.artist_id
from songs 
join artists 
on songs.artist_id = artists.artist_id
where songs.title = %s and artists.name = %s and songs.duration = %s 
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create,songplay_table_create]
drop_table_queries = [user_table_drop, song_table_drop, artist_table_drop, time_table_drop,songplay_table_drop]