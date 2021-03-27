from flask import Flask, render_template, request, jsonify

import imdb

APP = Flask(__name__)

DEFAULT_SEASON = 1


def search_page():
    return render_template('trivia.html')


@APP.route('/show')
def show():
    opt_args = {}
    if 'year' in request.args.keys():
        opt_args['year'] = int(request.args['year'])
    if 'season' in request.args.keys():
        opt_args['season_start'] = int(request.args['season'])
        opt_args['season_end'] = int(request.args['season'])
    else:
        opt_args['season_start'] = opt_args['season_end'] = 1
    print([i for i in request.args.keys()])
    show_data = imdb.OMDBAPIShowFactory(request.args['title'], **opt_args).create()
    return jsonify(show_data.serialize())


@APP.route('/episode')
def episode():
    opt_args = {}
    ep_id = request.args('ep_id', None)

    if ep_id:
        show_data = imdb.OMDBAPIShowFactory(request.args['title'], has_trivia=False, **opt_args).create()
        return jsonify(show_data.serialize())
    else:
        pass
        # return 404
