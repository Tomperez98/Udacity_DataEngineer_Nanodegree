# Documented Process
## Files description
* `create_tables.py`: This script drops anything there's in the database and resets both the database and the tables.
* `sql_queries.py`: Here we have all the SQL queries use in the initialization of the database and the data insertion of rows.
* `etl.py`: This script is where the data extraction from \*.json files, transformation of data and load into the database happends.
* `etl.ipynb`: Playground file to do a fast implementation, debugging and code iteration for the etl process.
* `test.ipynb`: Playground file to run SQL queries into the database and confirm everything is working as expected.

## How to run the code
On terminal run:
* python create_tables.py
* python etl.py

You can use test.ipynb to do sql queries (%sql for only one line or %%sql for the whole cell.)

In the files `etl.ipynb` and `sql_query` you will see, with more detail, how everyting works.

## Data modeling importance in an startup.
Being able to monitor, track and have a clear image of what's going one with the main KPIs of the company, your area or team
is one, if not, the most important thing to take decisions. Data models allow us to simplify and make queries faster which, 
problably won't see like to much when you have small data but when big data comes you better have a well design DW and ETLs to 
feed your data models for data scientists, data analysts and ML engineers.

This first project allow me to understand how to actually think about dimension and facts, and most importantly how to implement
that logic in python code.

## Database schema.
Normally when designing and analytical model you first want to clearly understand what's going to be used for. The star schema we
implemented in this project helps the business answer a bunch of different questions related to *when* do people listing more music
with the time_dim, *which* songs do they listen to with the songs_dim, *which* artist with the artist_dim, *who* with the users_dim.

This can help the business organize promotions, maybe recommend new artists in the platform or design playlists for their users.