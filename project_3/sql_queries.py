import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender CHAR(1),
    itemInSession SMALLINT,
    lastName VARCHAR,
    length DOUBLE PRECISION,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration BIGINT,
    sessionId INTEGER,
    song VARCHAR,
    status INTEGER,
    ts BIGINT,
    userAgent VARCHAR,
    userId INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    artist_id VARCHAR,
    artist_latitude DOUBLE PRECISION,
    artist_location VARCHAR,
    artist_longitude DOUBLE PRECISION,
    artist_name VARCHAR,
    duration DOUBLE PRECISION,
    num_songs INTEGER,
    song_id VARCHAR,
    title VARCHAR,
    year INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id INT IDENTITY (1, 1) PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL,
    level VARCHAR NOT NULL,
    song_id VARCHAR NOT NULL,
    artist_id VARCHAR NOT NULL,
    session_id INTEGER NOT NULL,
    location VARCHAR NOT NULL,
    user_agent VARCHAR NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (start_time) REFERENCES time(start_time)
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    gender CHAR(1) NOT NULL,
    level VARCHAR NOT NULL
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    artist_id VARCHAR NOT NULL,
    year INTEGER NOT NULL,
    duration DOUBLE PRECISION NOT NULL
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    location VARCHAR,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY,
    hour INTEGER NOT NULL,
    day INTEGER NOT NULL,
    week INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    weekday INTEGER NOT NULL
);
""")

# STAGING TABLES

staging_events_copy = ("""
copy staging_events
from {log_data}
iam_role {iam_role}
json {log_json_path};
""").format(log_data=config.get("S3", "LOG_DATA"), iam_role=config.get("IAM_ROLE", "ARN"), log_json_path=config.get("S3", "LOG_JSONPATH"))

staging_songs_copy = ("""
copy staging_songs
from {song_data}
iam_role {iam_role}
json 'auto';
""").format(song_data=config.get("S3", "SONG_DATA"), iam_role=config.get("IAM_ROLE", "ARN"))

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (
    start_time,
    user_id,
    level,
    song_id,
    artist_id,
    session_id,
    location,
    user_agent
    )
    SELECT
        DISTINCT TIMESTAMP 'epoch' + e.ts/1000 *INTERVAL '1 second' AS start_time, 
        e.userId AS user_id, 
        e.level, 
        s.song_id, 
        s.artist_id, 
        e.sessionId AS session_id, 
        e.location, 
        e.userAgent AS user_agent
    FROM staging_songs s
    INNER JOIN staging_events e ON (s.title = e.song AND e.artist = s.artist_name)
    WHERE e.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (
    SELECT
        DISTINCT userId AS user_id,
        firstName AS first_name,
        lastName AS last_name,
        gender,
        level
    FROM staging_events
    WHERE page = 'NextSong'
);
""")

song_table_insert = ("""
INSERT INTO songs (
    SELECT
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
);
""")

artist_table_insert = ("""
INSERT INTO artists (
    SELECT
        DISTINCT artist_id,
        artist_name AS name,
        artist_location AS location,
        artist_latitude AS latitude,
        artist_longitude AS longitude
    FROM staging_songs
);
""")

time_table_insert = ("""
INSERT INTO time (
    SELECT
        DISTINCT start_time,
        EXTRACT(hour FROM start_time) AS hour,
        EXTRACT(day FROM start_time) AS day,
        EXTRACT(week FROM start_time) AS week,
        EXTRACT(month FROM start_time) AS month,
        EXTRACT(year FROM start_time) AS year,
        EXTRACT(dow FROM start_time) AS weekday
    FROM (
      SELECT
          TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' AS start_time
      FROM staging_events
      ) base
);
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
