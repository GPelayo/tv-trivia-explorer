from selenium.webdriver import Firefox
from urllib import parse
import json
import os
import pprint
import time
MAX_SEASONS = 100
#
# DRIVER_FOLDER = 'webdriver'
# FULL_DRIVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DRIVER_FOLDER)
FULL_DRIVER_PATH = '/usr/local/bin'
# print(FULL_DRIVER_PATH)
os.environ['PATH'] = FULL_DRIVER_PATH

webdriver_class = Firefox


def extract_imdb_id_from_url(link):
    return parse.urlparse(link).path.strip('/').split('/')[-1]


class Show:
    seasons = []
    imdb_id = None

    def __init__(self, imdb_id):
        self.imdb_id = imdb_id

    def get_all_episode_idss(self):
        return [e.imdb_id for s in self.seasons for e in s.episodes]

    def serialize(self):
        return {
            'show': {
                'imdb_id': self.imdb_id,
                'seasons': [s.serialize() for s in self.seasons]
            }
        }


class Season:
    number = -1
    episodes = []

    def __init__(self, num, link):
        self.number = num
        self.imdb_link = link

    def serialize(self):
        return {
            'season': {
                'number': self.number,
                'episodes': [e.serialize() for e in self.episodes]
            }
        }


class Episode:
    title = None
    season = None
    ep_num = None
    link = None
    trivia = []

    def __init__(self, title, season, link):
        self.title = title
        self.season = season
        self.link = link

    def __str__(self):
        return self.link

    @property
    def imdb_id(self):
        return extract_imdb_id_from_url(self.link)

    def serialize(self):
        return {
                    'episode': {
                        'title': self.title,
                        'season': self.season,
                        'ep_num': self.ep_num,
                        'link': self.link,
                        'imdb_id': self.imdb_id,
                        'trivia': [t.serialize() for t in self.trivia]
                    }
                }


class Trivia:
    fact = None
    rating = None

    def serialize(self):
        return {"fact": self.fact, "rating": self.rating}


def populate_show(show):
    browser = webdriver_class()
    populate_seasons(browser, show)
    browser.close()


def populate_seasons(browser, show):
    for i in range(4, MAX_SEASONS+1):
        episode_query = "episodes?season={}".format(i)
        season_imdb_link = 'http://www.imdb.com/title/{}/{}'.format(show.imdb_id, episode_query)
        s = Season(i, episode_query)
        browser.get(season_imdb_link)
        s.episodes = []
        for e in browser.find_elements_by_xpath("//div[contains(@class, 'list_item')]"
                                                "/div[@class='info']"
                                                "/strong"
                                                "/a")[:1]:
            link = e.get_attribute('href')
            imdb_id = extract_imdb_id_from_url(link)
            if [True for x in show.get_all_episode_idss() if x == imdb_id]:
                return
            else:
                e = Episode(e.text, i, link)
                populate_with_trivia(e)
                s.episodes.append(e)
        show.seasons.append(s)


TRIVIA_SUFFIX = "trivia"


def populate_with_trivia(episode: Episode, rating_threshold=0):
    trivia_list = []
    browser = webdriver_class()
    trivia_url = episode.link.split('?')[0] + TRIVIA_SUFFIX
    browser.get(trivia_url)
    trivia_divs = browser.find_elements_by_xpath("//div[contains(@id, 'trivia_content')]"
                                                 "/div[contains(@class, 'list')]"
                                                 "/div[contains(@class, 'soda')]")
    for triv_box in trivia_divs:
        intrst_words = triv_box.find_element_by_xpath("div[contains(@class, 'did-you-know-actions')]").text
        good_rate, all_rate = intrst_words.split()[:3:2]
        trivia_rating = int(good_rate)/int(all_rate) if good_rate.isdigit() and all_rate.isdigit() else 0
        if rating_threshold <= trivia_rating:
            t = Trivia()
            t.fact = triv_box.find_element_by_xpath("div[contains(@class, 'sodatext')]").text
            t.rating = trivia_rating
            trivia_list.append(t)
    episode.trivia = trivia_list
    browser.close()

# for l in get_episode_links('tt0903747'):
sh = Show('tt0903747')

populate_show(sh)
pprint.pprint(sh.serialize())

fp = open('imdb.json', 'w')
json.dump(sh.serialize(), fp)

'''
Add batch extract trvia (stop reloading browser)

make parameter Episodsode obj
Get title
    get season links should output episodes
 Populate Objects
    ep
        trivia
        num
        season
    Season
        num
        link
        episodes
 Create JSON
    Study forms for React.js

Check if scraper gathered spoiler trivia
'''