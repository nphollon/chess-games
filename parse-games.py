import MySQLdb
import json
import requests

# TODO
# 1. Fetch games from Python script
# 2. Incremental fetch
# 3. Parameterize player name
# 4. CL interface - clean, init, fetch
# 5. Front-end??

player_name = "pigeonpal"
db_name = "chess_games"
db_user = "local"

def save_time_format(game_json, cursor):
    speed = game_json["speed"]
    time = game_json["clock"]["initial"]
    increment = game_json["clock"]["increment"]

    cursor.execute("SELECT id FROM time_format WHERE speed=%s AND time=%s AND increment=%s", (speed, time, increment))

    format_record = cursor.fetchone()
    if format_record is None:
        cursor.execute("INSERT INTO time_format (speed, time, increment) VALUES (%s, %s, %s)", (speed, time, increment))
        cursor.execute("SELECT id FROM time_format WHERE speed=%s AND time=%s AND increment=%s", (speed, time, increment))
        format_record = cursor.fetchone()

    return format_record[0]


def save_opening(opening_json, cursor):
    eco = opening_json["eco"]

    cursor.execute("SELECT id FROM opening WHERE eco=%s", (eco,))
    opening_record = cursor.fetchone()

    if opening_record is None:
        opening_names = list(map(lambda s: s.strip(), opening_json["name"].split(":")))

        if (len(opening_names) == 1):
            cursor.execute("INSERT INTO opening (eco, name) VALUES (%s,%s)", (eco, opening_names[0]))
        else:
            cursor.execute("INSERT INTO opening (eco, name, variation) VALUES (%s,%s,%s)", \
                (eco, opening_names[0], opening_names[1]))

        cursor.execute("SELECT id FROM opening WHERE eco=%s", (eco,))
        opening_record = cursor.fetchone()

    return opening_record[0]

def save_game(game_json, cursor):
    lichess_id = game_json["id"]

    cursor.execute("SELECT id FROM game where lichess_id=%s", (lichess_id,))
    game_record = cursor.fetchone()
    
    if game_record is None:
        datetime = game_json["createdAt"]

        # assume that player_name played this game
        if player_name == game_json["players"]["white"]["user"]["id"]:
            color = "white"
            opponent_color = "black"
        else:
            color = "black"
            opponent_color = "white"

        result_detail = game_json["status"]

        if "winner" not in game_json:
            result = "draw"
        elif game_json["winner"] == color:
            result = "win"
        else:
            result = "loss"

        moves = game_json["moves"]
        ply_length = len(moves.split())
        pgn = game_json["pgn"]


        # Players & Ratings
        me = game_json["players"][color]
        rating = me["rating"]
        rating_change = me["ratingDiff"]
        provisional = me.get("provisional") == "true"

        opponent = game_json["players"][opponent_color]
        opponent_name = opponent["user"]["id"]
        opponent_rating = opponent["rating"]


        format_id = save_time_format(game_json, cursor)
        
        opening_id = save_opening(game_json["opening"], cursor)

        cursor.execute('''INSERT INTO game 
            (lichess_id, datetime, color, format_id, result, result_detail, rating,
            provisional, rating_change, opponent_name, opponent_rating, opening_id, ply_length, pgn) 
            VALUES (%s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (lichess_id, datetime, color, format_id, result, result_detail, rating, \
            provisional, rating_change, opponent_name, opponent_rating, opening_id, ply_length, pgn))

        cursor.execute("SELECT id FROM game where lichess_id=%s", (lichess_id,))
        game_record = cursor.fetchone()

    return game_record[0]


def save_analysis(game_json, game_id, cursor):
    cursor.execute("SELECT id FROM analysis WHERE game_id=%s", (game_id,))
    if cursor.fetchone() is not None:
        return

    # TODO duplicated :-|
    if player_name == game_json["players"]["white"]["user"]["id"]:
        color = "white"
    else:
        color = "black"

    player_stats = game_json["players"][color]["analysis"]
    inaccuracies = player_stats["inaccuracy"]
    mistakes = player_stats["mistake"]
    blunders = player_stats["blunder"]
    average_centipawn_loss = player_stats["acpl"]
    analysis = json.dumps(game_json["analysis"])

    cursor.execute('''INSERT INTO analysis
        (game_id, inaccuracies, mistakes, blunders, average_centipawn_loss, analysis)
        VALUES (%s, %s, %s, %s, %s, %s)''', \
        (game_id, inaccuracies, mistakes, blunders, average_centipawn_loss, analysis))


def parse_json_entry(game_json, cursor):
    game_id = save_game(game_json, cursor)

    if "analysis" in game_json:
        save_analysis(game_json, game_id, cursor)


if __name__ == "__main__":
    headers = {
        'Accept': 'application/x-ndjson',
        'Authorization': f'Bearer {lichess_api_token}'
    }

    url = f"https://lichess.org/api/games/user/{player_name}"
    
    params = {
        'rated': 'true',
        'perfType': 'ultraBullet,bullet,blitz,rapid,classical,correspondence',
        'pgnInJson': 'true',
        'clocks': 'true',
        'evals': 'true',
        'opening': 'true'
    }

    response = requests.get(url, params, headers=headers)

    connection = MySQLdb.connect(host='localhost', db=db_name, user=db_user)

    try:
        line = ""
        game_count = 0
        for chunk in response.iter_content(chunk_size=128):
            line += chunk.decode("utf-8")

            # assume at most one newline
            if '\n' in line:
                linesplit = line.split("\n")
                parse_json_entry(json.loads(linesplit[0]), connection.cursor())
                connection.commit()
                game_count += 1
                line = linesplit[1]
    finally:
        connection.close()
        print(f'{game_count} games downloaded')
