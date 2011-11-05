from flask import Flask, url_for, redirect

# configuration
USER_DB = 'dota2.db'
DEBUG = True
SECRET_KEY = 'development key'
SITEURL = "http://dota2-arena.com/"

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

from sign_up import *
from hero import *
from post_hero import *
from post_spell import *
from post_news import *
from post_item import *
from post_guide import *
from guide import *
from groups import *
from item import *
from news import *

@app.route('/', methods=['GET'])
def default():
    flash('Bienvenue sur Dota 2 Arena')
    return news()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
