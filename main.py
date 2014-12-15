from mongokit import *
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import json

CONFIG = json.load(open('./config.json'))

BASE_URL = 'http://www.nhl.com/ice/playerstats.htm'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

def db_setup():
    connection = Connection(CONFIG['mongoURI'])

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

    return connection

Models = db_setup()

class MappedRow():
    """
    MappedRow is a convenience class for taking an array with names and mapping it to an array of values
    """

    def __init__(self, values, keys):
        """
        Pass in an array of values and an array of keys
        :param values:
        :param keys:
        :return:
        """
        self.keys = keys
        self.values = values

    def __getitem__(self, item):
        index = self.keys.index(item)
        return self.values[index]

    def get_dict(self):
        """
        Dump to dictionary type
        :return:
        """
        value_dict = {}
        for index in range(0, len(self.keys)):
            value_dict[self.keys[index]] = self.values[index]
        return value_dict

    def __repr__(self):
        return str(self.get_dict())


class FetchPage():
    def __init__(self, url, parser=None):
        if hasattr(parser, '__call__'):
            self.parser = parser
        self.url = url

    def set_parser(self, parser):
        if hasattr(parser, '__call__'):
            self.parser = parser

    def fetch(self):
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(self.url, headers=headers)
        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.content)
            self.parser(self, soup)


def home_parser(self, data):
    table = data.select('table.data.stats tr')
    stat_keys = [row.text.strip() for row in table[0].select('th')]
    stat_keys.append('uri')
    # Skipping the navigation row
    table = table[2:]
    stat_rows = []
    # Yes I know its O^2
    for row in table:
        stat_row = [field.text.strip() for field in row]
        link = row.select('a')[0]
        stat_row.append(link.get('href'))
        stat_rows.append(MappedRow(stat_row, stat_keys))

    for row in stat_rows:
        player = Models.PlayerModel()
        player['name'] = row['Player']
        player['team'] = row['Team']
        player['pos'] = row['Pos']
        player['uri'] = row['uri']
        try:
            player.save()
        except Exception:
            pprint("Issue saving %s" % player['name'])


def execute():
    home = FetchPage(BASE_URL, parser=home_parser)
    home.fetch()



if __name__ == '__main__':
    execute()





