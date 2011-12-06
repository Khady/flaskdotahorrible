#-*- encoding: utf-8 -*-

from flask import render_template
from dota2 import app

@app.route('/stream/', methods=['GET', 'POST'])
def stream():
    return render_template('stream.html')
