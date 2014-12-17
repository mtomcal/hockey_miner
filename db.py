import pymongo
import datetime
from mongokit import *
from config import CONFIG

connection = Connection(CONFIG['mongo_uri'])

@connection.register
class PlayerModel(Document):
    __collection__ = 'players'
    __database__ = 'nhl'
    structure = {
        "name": basestring,
        "team": basestring,
        "pos": basestring,
        "uri": basestring
    }

class GameStatsModel(Document):
    __collection__ = 'gamestats'
    __database__ = 'nhl'
    structure = {
        "player_id": pymongo.objectid.ObjectId,
        "date": datetime.datetime,
        "player_type": IS('skater', 'goalie'),
        "skater": {
            "goals": int,
            "assists": int,
            "plus_minus": int,
            "power_play_goals": int,
            "short_handed_goals": int,
            "shots": int,
            "shot_percent": int,
            "shifts": int,
            "time_on_ice": basestring,
            "faceoff_win_percent": int
        },
        "goalie": {
            "games_played": int,
            "games_started": int,
            "wins": int,
            "losses": int,
            "overtime": int,
            "shots_against": int,
            "goals_against": int,
            "goals_against_ave": float,

        }

    }


def setup():
    return connection