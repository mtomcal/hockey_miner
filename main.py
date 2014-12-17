from pprint import pprint
from utility import MappedRow, FetchPage
from config import CONFIG
import db

Models = db.setup()

def stat_parser(self, data):
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

def pagination_parser(self, data):
    last_link = data.select('div.pages > a')
    """There are seven pagination links. Get the last one."""
    link_text = last_link[7].get('href')
    """Assuming double digit page number at end of url"""
    last_page = int(link_text[-2:])
    return last_page



def execute():
    base = FetchPage(CONFIG['base_url'], parser=pagination_parser)
    last_page = base.fetch()
    queue = []
    for i in range(1, last_page + 1):
        paged_url_base = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20152ALLSASAll&viewName=summary&sort=points&pg="
        queue.append(FetchPage(paged_url_base + str(i), parser=stat_parser))

    for req in queue:
        pprint(req)
        #req.fetch()

if __name__ == '__main__':
    execute()





