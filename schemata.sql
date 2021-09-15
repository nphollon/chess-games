CREATE TABLE player
( id INTEGER AUTO_INCREMENT PRIMARY KEY
, lichess_id VARCHAR(40) UNIQUE
, name VARCHAR(40)
, rating SMALLINT UNSIGNED
, provisional TINYINT(1)
, lifetime_wins_against SMALLINT UNSIGNED
, lifetime_losses_to SMALLINT UNSIGNED
, lifetime_draws SMALLINT UNSIGNED
);


CREATE TABLE game_format
( id INTEGER AUTO_INCREMENT PRIMARY KEY
, speed VARCHAR(40) NOT NULL
, time SMALLINT UNSIGNED NOT NULL
, increment SMALLINT UNSIGNED NOT NULL DEFAULT 0
);


CREATE TABLE opening
( id INTEGER AUTO_INCREMENT PRIMARY KEY
, eco VARCHAR(3) UNIQUE NOT NULL
, name VARCHAR(120) NOT NULL
, variation VARCHAR(120)
);


CREATE TABLE game
( id INTEGER AUTO_INCREMENT PRIMARY KEY
, lichess_id VARCHAR(8) UNIQUE
, game_number INTEGER UNSIGNED
, datetime DATETIME
, color ENUM('white','black')

, format_id INTEGER
, CONSTRAINT FOREIGN KEY (format_id) REFERENCES game_format(id) ON DELETE RESTRICT

, opponent_id INTEGER
, CONSTRAINT FOREIGN KEY (opponent_id) REFERENCES player(id) ON DELETE RESTRICT

, result ENUM('win','loss','draw')
, result_detail VARCHAR(80)
, rating SMALLINT UNSIGNED
, provisional TINYINT(1)
, rating_change SMALLINT
, opponent_rating SMALLINT UNSIGNED

, opening_id INTEGER
, CONSTRAINT FOREIGN KEY (opening_id) REFERENCES opening(id) ON DELETE RESTRICT

, time_remaining TIME
, ply_length SMALLINT UNSIGNED
, moves TEXT
, pgn TEXT
);


CREATE TABLE analysis
( id INTEGER AUTO_INCREMENT PRIMARY KEY

, game_id INTEGER NOT NULL
, CONSTRAINT FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE

, inaccuracies TINYINT UNSIGNED
, mistakes TINYINT UNSIGNED
, blunders TINYINT UNSIGNED
, average_centipawn_loss SMALLINT UNSIGNED
, analysis TEXT
);
