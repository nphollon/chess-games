# Download games from Lichess

This program downloads the games for a player from Lichess and saves them to a MySQL database. The database structure is specific to the individual player (for example, the result of each game is recorded as "win", "loss", or "draw").

I wrote this to help with analysis for my own games. Maybe you will find it useful? Who knows?

There's no front-end (yet?!), so you need to be familiar with MySQL.

## Installation

1. Create a MySQL database. Name it whatever you want! I called mine "chess_games".
2. Run `db-init.sql` on your database to create the necessary tables. For example, `mysql chess_games < db-init.sql`
2. Log into Lichess and create a [personal API access token](https://lichess.org/account/oauth/token)
3. Make a copy of `config.json.template`. Call it `config.json`.
4. Fill out the four fields in `config.json`. (The database can't be password-protected.)
5. Run `python3 parse-games.py`.
6. Now the database has your games in it. Have fun with your data.

You can run `parse-games.py` multiple times. It won't overwrite existing data. Still, if you want to reset the database, you can run `db-clean.sql` and `db-init.sql`.