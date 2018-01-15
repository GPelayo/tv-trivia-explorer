class Show:
    seasons = None
    imdb_id = None
    title = None
    year_start = None
    year_end = None
    season_qty= None

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
    show_id = None

    def __init__(self, num, show_id):
        self.number = num
        self.show_id = show_id
        self.episodes = []

    def serialize(self):
        return {
            'season': {
                'number': self.number,
                'episodes': [e.serialize() for e in self.episodes]
            }
        }

    @property
    def episode_ids(self):
        print([e.imdb_id for e in self.episodes])
        return [e.imdb_id for e in self.episodes]


class Episode:
    title = None
    season = None
    ep_num = None
    link = None
    trivia = None
    show_id = None

    def __init__(self, ep_id, title, season):
        self.title = title
        self.season = season
        self.trivia = []
        self.show_id = ep_id

    def __str__(self):
        return self.link

    def serialize(self):
        return {
                    'episode': {
                        'title': self.title,
                        'season': self.season,
                        'ep_num': self.ep_num,
                        'link': self.link,
                        'show_id': self.show_id,
                        'trivia': [t.serialize() for t in self.trivia]
                    }
                }


class Trivia:
    fact = None
    rating = None

    def serialize(self):
        return {"fact": self.fact, "rating": self.rating}
