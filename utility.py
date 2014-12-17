"""
Utility Classes
"""

from config import CONFIG
from bs4 import BeautifulSoup
import requests


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
        headers = {'User-Agent': CONFIG['user_agent']}
        response = requests.get(self.url, headers=headers)
        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.content)
            return self.parser(self, soup)

    def __repr__(self):
        return "<FetchPage url=%s, parser=%s>" % (self.url, self.parser)
