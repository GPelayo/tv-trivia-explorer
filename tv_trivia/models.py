class Show:
    seasons = None
    imdb_id = None
    title = None
    year_start = None
    year_end = None

    def __init__(self, imdb_id, title):
        self.title = title
        self.imdb_id = imdb_id
        self.seasons = []

    def get_all_episode_idss(self):
        return [e.imdb_id for s in self.seasons for e in s.episodes]

    def serialize(self):
        return {
            'show': {
                'imdb_id': self.imdb_id,
                'seasons': [s.serialize() for s in self.seasons],
                'title': self.title,
                'year_start': self.year_start,
                'year_end': self.year_end
            }
        }


class Season:
    number = -1
    episodes = None

    def __init__(self, num, link):
        self.number = num
        self.imdb_link = link
        self.episodes = []

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
    trivia = None
    imdb_id = None

    def __init__(self, title, season, link):
        self.title = title
        self.season = season
        self.link = link
        self.trivia = []

    def __str__(self):
        return self.link

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
