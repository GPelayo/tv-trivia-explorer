from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib import parse
from models import Episode, Trivia, Season
import omdb
import settings

MAX_SEASONS = 100


TRIVIA_SUFFIX = "trivia"


class InvalidShowError(Exception):
    pass


class TVFactory:

    def create(self):
        raise NotImplementedError


class SelSecDcrtr:
    @staticmethod
    def safely_scrape(function):
        def wrapper(self, *args, **kwargs):
            is_parent = kwargs.get('browser', None) is not None
            kwargs['browser'] = kwargs.get('browser', self.default_browser)
            print(is_parent)
            output = function(self, *args, **kwargs)
            print(is_parent)
            if not is_parent:
                kwargs['browser'].close()
            return output
        return wrapper


class IMDBSeleniumScraper:
    driver_type = settings.SELENIUM_WEBDRIVER_TYPE
    default_browser = None

    def __init__(self, browser=None):
        self.default_browser = browser or self.driver_type()

    @SelSecDcrtr.safely_scrape
    def get_episode_data(self, show_id, season, browser=None):
        episode_list = []
        browser.get('http://www.imdb.com/title/{}/episodes?season={}'.format(show_id, season))
        trivia_browser = self.driver_type()
        for e in browser.find_elements_by_xpath("//div[contains(@class, 'list_item')]"
                                               "/div[@class='info']"
                                               "/strong"
                                               "/a"):
            link = e.get_attribute('href')
            e = Episode(e.text, season, link)
            e.trivia = self.get_trivia_data(e, browser=trivia_browser)
            episode_list.append(e)
        trivia_browser.close()
        return episode_list

    @SelSecDcrtr.safely_scrape
    def get_trivia_data(self, episode, rating_threshold=0, browser=None):
        trivia_list = []
        trivia_url = episode.link.split('?')[0] + TRIVIA_SUFFIX
        browser.get(trivia_url)
        trivia_divs = browser.find_elements_by_xpath("//div[contains(@id, 'trivia_content')]"
                                                                  "/div[contains(@class, 'list')]"
                                                                  "/div[contains(@class, 'soda')]")
        for trivia_box in trivia_divs:
            try:
                intrst_words = trivia_box.find_element_by_xpath("div[contains(@class, 'did-you-know-actions')]").text
            except NoSuchElementException:
                break
            else:
                good_rate, all_rate = intrst_words.split()[:3:2]
                trivia_rating = int(good_rate)/int(all_rate) if good_rate.isdigit() and all_rate.isdigit() else 0
                if rating_threshold <= trivia_rating:
                    t = Trivia()
                    t.fact = trivia_box.find_element_by_xpath("div[contains(@class, 'sodatext')]").text
                    t.rating = trivia_rating
                    trivia_list.append(t)
        return trivia_list


class ShowFactory(TVFactory):
    def __init__(self, title=None, show_id=None, year=None, season_start=1, season_end=1):
        self.title = title
        self.show_id = show_id
        self.year = year
        self.season_start = season_start
        self.season_end = season_end
        self.season_qty = None

        if not (self.title or self.show_id):
            raise InvalidShowError

    def create(self):
        raise NotImplementedError


class SeasonFactory(TVFactory):
    def __init__(self, show_id, season, season_qty):
        self.show_id = show_id
        self.season = season

    def create(self):
        raise NotImplementedError


class EpisodeFactory(TVFactory):
    driver_type = webdriver.PhantomJS

    def __init__(self, episode_id):
        self.show_id = episode_id

    def create(self):
        raise NotImplementedError


class OMDBAPIShowFactory(ShowFactory, IMDBSeleniumScraper):
    def __init__(self, title=None, imdb_show_id=None, year=None, season_start=None, season_end=None, browser=None):
        ShowFactory.__init__(self, title=title, show_id=imdb_show_id, season_start=season_start, season_end=season_end,
                             year=year)
        IMDBSeleniumScraper.__init__(self, browser=browser)

    def create(self):
        sh = omdb.get_show_by_id(self.title, year=self.year)
        season_min = self.season_start or 1
        season_max = self.season_end or sh.season_qty
        sh.seasons = [IMDBSeasonFactory(imdb_show_id=sh.imdb_id, season=i, browser=self.default_browser).create()
                      for i in range(season_min, season_max+1)]
        return sh


class IMDBSeasonFactory(SeasonFactory, IMDBSeleniumScraper):
    def __init__(self, imdb_show_id, season, season_qty=1, browser=None):
        SeasonFactory.__init__(self, imdb_show_id, season, season_qty=season_qty)
        IMDBSeleniumScraper.__init__(self, browser=browser)

    def create(self):
        s = Season(self.season, self.show_id)
        s.episodes = self.get_episode_data(self.show_id, self.season)
        return s

