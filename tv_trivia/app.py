from flask import Flask, render_template, request, jsonify
from tv_trivia import imdb

app = Flask(__name__)

DEFAULT_SEASON = 1


@app.route('/')
def search_page():
    return render_template('trivia.html')


@app.route('/show')
def show():
    print('Finding Data')
    opt_args = []
    if 'year' in request.args.keys():
        opt_args.append(request.args['year'])
    if 'season' in request.args.keys():
        opt_args.append(request.args['season'])
    show_data = imdb.get_show_data_by_title(request.args['title'])
    print('Sent JSON')
    return jsonify(show_data)
