from flask import Flask, url_for
from hero import Hero

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hero/')
@app.route('/hero/<name>')
def hero(name=None):
    return Hero(name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
