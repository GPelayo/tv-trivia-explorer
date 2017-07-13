from urllib import request, parse
import json
from urllib import request, parse
import settings
from models import Show


def get_show_by_id(title_query, year=''):
    qry_dict = {'t': title_query, 'apikey': settings.OMDB_API_KEY}
    if year:
        qry_dict.update({'y': year})

    r = request.urlopen("http://www.omdbapi.com/?{}".format(parse.urlencode(qry_dict)))
    omdb_json = json.load(r)
    imdb_id = omdb_json.get('imdbID')
    title = omdb_json.get('Title')
    s = Show(imdb_id, title)
    y = omdb_json.get('Year', None)

    if y:
        s.year_start, s.year_end = y.split('–') if len(y.split('–')) > 1 else (y, '')
    return s
