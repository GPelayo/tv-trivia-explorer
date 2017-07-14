from flask import Flask, render_template, request, jsonify

import imdb

APP = Flask(__name__)

DEFAULT_SEASON = 1


@APP.route('/')
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
    show_data = imdb.OMDBAPIShowFactory(request.args['title'], **opt_args).create()
    return jsonify(show_data.serialize())
