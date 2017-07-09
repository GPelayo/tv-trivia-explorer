from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/temp')
def temp():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)
