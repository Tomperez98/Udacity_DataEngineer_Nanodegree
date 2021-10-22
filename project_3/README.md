# Process Documentation
Sparkify, a music streaming startup, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As a Data Engineer, I'll build an ETL pipeline (More an ELT pipeline) that extracts their data from S3, stage them in Redshift, and transforms data into a set of dimensional tables for their analytics team.

## Purpose of this analytical database for Sparkify
As data grows big, analytical workload starts to create a burden in transactional databases (Which are optimized for well... transactional workload not analytical). This has a direct impact in the UX within the app. For that reason we want to separate the process into two parts (1) Transactional database and (2) Analytical database.

This will allow business users (Data analysts, data scientist, etc) to do any query without impacting UX within the app, plus these queries will be executed in a highly optimized environment (Column oriented storage, MPP, etc) as Redshift (Amazon data warehouse service).
Not only that, data will be modeled in a denormalized schema (star schema) that's easy and fast to query.

## ETL justification and database schema.
Since storage has become so cheap we want to use the capabilities of DW to perform transformation within it in a staging are (The kitchen) before actually presenting it with the dimensional models (The front door). That said, we first load the raw data into staging tables with Redshift and then perform SQL queries to those tables to prepare the data for the dimension and fact tables.

The dimensional model has 5 tables (1 fact and 4 dimensions). This model will allow Sparkify to do analytical queries on the `songplays` business process, group by users, songs, artists and time

## Query ideas
```
--- By gender and by weekday how many songs are listened.
SELECT
    c.gender,
    b.weekday,
    COUNT(DISTINCT a.song_id)
FROM songplays a
INNER JOIN time b ON (a.start_time = b.start_time)
INNER JOIN users c ON (a.user_id = c.user_id)
GROUP BY 1,2
ORDER BY 1 DESC, 3 ASC, 2 DESC;
```

```
--- Number of paid and free subscribers.
SELECT
    a.level,
    COUNT(DISTINCT a.user_id)
FROM songplays a
GROUP BY 1;
```