#!/usr/bin/env python2
#-*- encoding: utf-8 -*-
from __future__ import with_statement
import sqlite3
import time
import random
import string

from contextlib import closing
from flask import request, session, g, redirect, url_for, \
     abort, render_template, flash
import Mail
from dota2 import app
from droits import *

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/admin')
def admin():
    g.db = connect_db(app.config['USER_DB'])
    if 'logged_in' in session:
        droits = get_droits(session['user_id'])
    else:
        return redirect(url_for('default'))
    g.db.close()
    return render_template('admin.html', droits=droits)

@app.route('/admin/user', methods=['GET', 'POST'])
def user_adm():
    if 'logged_in' not in session:
        return redirect(url_for('default'))
    if request.method == 'GET':
        return render_template('user_adm.html')
    else:
        password = request.form['password']
        pass_hash = sha1(password.encode('utf-8')).hexdigest()
        mail = request.form['mail'].lower()
        if len(mail) != 0:
            g.db.execute('update user_description set mail = ? where id = ?', [mail, session['user_id']])
        if len(password) != 0:
            g.db.execute('update user_description set hash = ? where id = ?', [pass_hash, session['user_id']])
        return redirect(url_for('user_adm'))

@app.route('/admin/guides', methods=['GET', 'POST'])
def guide_validation():
    g.db = connect_db(app.config['USER_DB'])
    if 'logged_in' not in session or get_droits(session['user_id'])['guide_validation'] != 1:
        return redirect(url_for('default'))
    cur = g.db.execute('select id, title, hero, heroname, score, valid from guide')
    guides = [dict(id=row[0], titre=row[1], hero=row[2], heroname=row[3],
                   score=row[4], valid=row[5]) for row in cur.fetchall()]
    cur = g.db.execute('select id, title, hero, heroname, score, valid, id_guide from guidetmp')
    guidestmp = [dict(id=row[0], titre=row[1], hero=row[2], heroname=row[3],
                      score=row[4], valid=row[5], id_guide=row[6]) for row in cur.fetchall()]
    print guides
    if request.method != 'GET':
        if request.form['submit'] == 'Valider':
            for guide in guides:
                guide['valid'] = int(request.form[guide['heroname']])
                if guide['valid'] == 2:
                    g.db.execute('delete from guide where id = ?', [guide['id']])
                else:
                    g.db.execute('update guide set valid = ? where id = ?', [guide['valid'], guide['id']])
                g.db.commit()
            g.db.close()
        else:
            for guide in guidestmp:
                guide['valid'] = int(request.form[guide['heroname']])
                if guide['valid'] == 2:
                    g.db.execute('delete from guide where id = ?', [guide['id']])
                elif guide['valid'] == 1:
                    if guide['id_guide'] == None:
                        g.db.execute('insert into guidetmp (title, tag, hero, heroname, difficulties, content_untouch, content_markup, date_last_modif, valid) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                     [guide['titre'],
                                      guide['tag'],
                                      guide['hero'],
                                      guide['heroname'],
                                      guide['diff'],
                                      guide['content'],
                                      guide['content_markup'],
                                      guide['date_last_modif'],
                                      1])
                    else:
                        g.db.execute('update guide set title = ?, tag = ?, hero = ?, heroname = ?, difficulties = ?, content_untouch = ?, content_markup = ?, date_last_modif = ?, valid = ?'
                                     [guide['titre'],
                                      guide['tag'],
                                      guide['hero'],
                                      guide['heroname'],
                                      guide['diff'],
                                      guide['content'],
                                      guide['content_markup'],
                                      guide['date_last_modif'],
                                      1])
                g.db.commit()
            g.db.close()
    return render_template('guides_adm.html', guides=guides, guidestmp=guidestmp)
