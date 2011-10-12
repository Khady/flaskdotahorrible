from flask import Flask, url_for

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
from groups import *

@app.route('/', methods=['GET'])
def default():
    flash('Welcome to Dota 2 Arena')
    return render_template('sign_up.html', error=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
