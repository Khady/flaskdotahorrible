#-*- encoding: utf-8 -*-

from flask import render_template
from dota2 import app

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')
