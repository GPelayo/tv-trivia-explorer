import json
from urllib import request, parse
import codecs
from tv_trivia import settings
from tv_trivia.models import Show


def get_show_by_id(title_query, year=''):
    qry_dict = {'t': title_query, 'apikey': settings.OMDB_API_KEY}
    if year:
        qry_dict.update({'y': year})

    r = request.urlopen("http://www.omdbapi.com/?{}".format(parse.urlencode(qry_dict)))
    rdr = codecs.getdecoder('utf-8')
    omdb_json = json.loads(r.read().decode('utf-8'))
    imdb_id = omdb_json.get('imdbID')
    title = omdb_json.get('Title')
    s = Show(imdb_id, title)
    s.season_qty = int(omdb_json.get('totalSeasons'))
    y = omdb_json.get('Year', None)

    if y:
        s.year_start, s.year_end = y.split('–') if len(y.split('–')) > 1 else (y, '')
    return s
