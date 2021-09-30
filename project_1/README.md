# Document Process
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