#-*- encoding: utf-8 -*-

from flask import Flask, url_for, redirect

# configuration
USER_DB = 'dota2.db'
DEBUG = True
SECRET_KEY = 'development key'
SITEURL = "http://dota2-arena.com/"

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

from sign_up import *
from hero import *
from post_hero import *
from post_spell import *
from post_news import *
from post_item import *
from post_guide import *
from post_comment import *
from guide import *
from groups import *
from item import *
from news import *
from admin import *
from contact import *
from stream import *

@app.route('/', methods=['GET'])
def default():
    uni = u'Bienvenue sur Dota 2 Arena'
    flash(uni)
    return news()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
