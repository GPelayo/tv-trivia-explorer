from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib import parse
from models import Episode, Trivia, Season
import omdb

MAX_SEASONS = 100


TRIVIA_SUFFIX = "trivia"
driver_type = webdriver.PhantomJS


def extract_imdb_id_from_url(link):
    return parse.urlparse(link).path.strip('/').split('/')[-1]


def populate_show(show, season=1):
    browser = driver_type()

    for i in range(season, season+1):
        populate_season(browser, show, season)
    browser.close()


def populate_season(browser, show, season=1):
    episode_query = "episodes?season={}".format(season)
    season_imdb_link = 'http://www.imdb.com/title/{}/{}'.format(show.imdb_id, episode_query)
    s = Season(season, episode_query)
    browser.get(season_imdb_link)
    s.episodes = []
    for e in browser.find_elements_by_xpath("//div[contains(@class, 'list_item')]"
                                            "/div[@class='info']"
                                            "/strong"
                                            "/a"):
        link = e.get_attribute('href')
        imdb_id = extract_imdb_id_from_url(link)
        if [True for x in show.get_all_episode_idss() if x == imdb_id]:
            return
        else:
            e = Episode(e.text, season, link)
            populate_with_trivia(e)
            s.episodes.append(e)
    show.seasons.append(s)


def populate_with_trivia(episode: Episode, rating_threshold=0):
    trivia_list = []
    browser = driver_type()
    trivia_url = episode.link.split('?')[0] + TRIVIA_SUFFIX
    browser.get(trivia_url)
    trivia_divs = browser.find_elements_by_xpath("//div[contains(@id, 'trivia_content')]"
                                                 "/div[contains(@class, 'list')]"
                                                 "/div[contains(@class, 'soda')]")
    for triv_box in trivia_divs:
        try:
            intrst_words = triv_box.find_element_by_xpath("div[contains(@class, 'did-you-know-actions')]").text
        except NoSuchElementException:
            break
        else:
            good_rate, all_rate = intrst_words.split()[:3:2]
            trivia_rating = int(good_rate)/int(all_rate) if good_rate.isdigit() and all_rate.isdigit() else 0
            if rating_threshold <= trivia_rating:
                t = Trivia()
                t.fact = triv_box.find_element_by_xpath("div[contains(@class, 'sodatext')]").text
                t.rating = trivia_rating
                trivia_list.append(t)
    episode.trivia = trivia_list
    browser.close()


def get_show_data_by_title(title, year="", season=1):
    sh = omdb.get_show_by_id(title, year=year)
    populate_show(sh, season)
    return sh.serialize()
