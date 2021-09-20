CREATE TABLE IF NOT EXISTS time_format
( id INTEGER AUTO_INCREMENT PRIMARY KEY
, speed VARCHAR(40) NOT NULL
, time SMALLINT UNSIGNED NOT NULL
, increment SMALLINT UNSIGNED NOT NULL DEFAULT 0
);


CREATE TABLE IF NOT EXISTS opening
( id INTEGER AUTO_INCREMENT PRIMARY KEY
, eco VARCHAR(3) UNIQUE NOT NULL
, name VARCHAR(120) NOT NULL
, variation VARCHAR(120)
);


CREATE TABLE IF NOT EXISTS game
( id INTEGER AUTO_INCREMENT PRIMARY KEY
, lichess_id VARCHAR(8) UNIQUE
, datetime DATETIME
, color ENUM('white','black')
, format_id INTEGER
, result ENUM('win','loss','draw')
, result_detail VARCHAR(80)
, rating SMALLINT UNSIGNED
, provisional TINYINT(1)
, rating_change SMALLINT
, opponent_name VARCHAR(80)
, opponent_rating SMALLINT UNSIGNED
, opening_id INTEGER
, time_remaining TIME
, ply_length SMALLINT UNSIGNED
, moves TEXT
, pgn TEXT

, CONSTRAINT FOREIGN KEY (format_id) REFERENCES time_format(id)
, CONSTRAINT FOREIGN KEY (opening_id) REFERENCES opening(id)
);


CREATE TABLE IF NOT EXISTS analysis
( id INTEGER AUTO_INCREMENT PRIMARY KEY

, game_id INTEGER NOT NULL
, CONSTRAINT FOREIGN KEY (game_id) REFERENCES game(id) ON DELETE CASCADE

, inaccuracies TINYINT UNSIGNED
, mistakes TINYINT UNSIGNED
, blunders TINYINT UNSIGNED
, average_centipawn_loss SMALLINT UNSIGNED
, analysis TEXT
);
