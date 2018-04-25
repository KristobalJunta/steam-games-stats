import requests
import sqlite3
import re
import json
from datetime import datetime, timezone, timedelta
import os


def find_game(gid, game_json):
    for game in game_json:
        if gid == game['appid']:
            return game

    return None


curwd = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(curwd + '/steamstats.db')
cur = conn.cursor()

games = cur.execute('select * from games;').fetchall()
profile_url = 'https://steamcommunity.com/id/kristobaljunta/games/?tab=all&sort=playtime'
content = requests.get(profile_url).content.decode()
lines = content.split('\r\n')
game_json = '[]'

for line in lines:
    if 'var rgGames' in line:
        search = re.search('\[.*\]', line)
        if search is not None:
            game_json = search.group(0)

game_json = json.loads(game_json)

print(games)

for g in games:
    game = find_game(g[1], game_json)
    if game is not None:
        hours = int(game['hours_forever'])
        print(hours)

        date = datetime.now(timezone(timedelta(hours=2)))
        print(date)

        cur.execute('insert into points(hours, game_id, timestamp) values(?,?,?);', (hours, g[0], date))
        conn.commit()
