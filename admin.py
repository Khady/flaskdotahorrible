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
from hashlib import sha1

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/admin')
def admin():
    g.db = connect_db(app.config['USER_DB'])
    if 'logged_in' in session:
        droits = get_droits(session['user_id'])
        print droits
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
        g.db = connect_db(app.config['USER_DB'])
        password = request.form['password']
        pass_hash = sha1(password.encode('utf-8')).hexdigest()
        mail = request.form['mail'].lower()
        if len(mail) != 0:
            g.db.execute('update user_description set mail = ? where id = ?', [mail, session['user_id']])
        if len(password) != 0:
            g.db.execute('update user_description set hash = ? where id = ?', [pass_hash, session['user_id']])
        g.db.commit()
        g.db.close()
        return redirect(url_for('user_adm'))

@app.route('/admin/guides', methods=['GET', 'POST'])
def guide_validation():
    g.db = connect_db(app.config['USER_DB'])
    droits = get_droits(session['user_id'])
    if 'logged_in' not in session or (droits['guide'] != 1 and droits['adm'] != 1):
        return redirect(url_for('default'))
    cur = g.db.execute('select id, guide_id, title, hero, heroname, score, valid from guide where valid = ?', [1])
    guides = [dict(id=row[0], id_guide=row[1], titre=row[2], hero=row[3], heroname=row[4],
                   score=row[5], valid=row[6], uid=str(row[0]) + "-" + str(row[1]))
              for row in cur.fetchall()]

    cur = g.db.execute('select id, guide_id, title, hero, heroname, score, valid from guide where valid != ?', [1])
    guidestmp = [dict(id=row[0], id_guide=row[1], titre=row[2], hero=row[3], heroname=row[4],
                   score=row[5], valid=row[6], uid=str(row[0]) + "-" + str(row[1]))
                 for row in cur.fetchall()]
    g.db.close()
    if request.method != 'GET':
        g.db = connect_db(app.config['USER_DB'])
        if request.form['submit'] == 'Valider':
            for guide in guides:
                guide['valid'] = int(request.form[guide['heroname']])
                if guide['valid'] == 2:
                    g.db.execute('delete from guide where id = ? and valid = ?', [guide['id'], 1])
                else:
                    g.db.execute('update guide set valid = ? where id = ? and valid = ?',
                                 [guide['valid'], guide['id'], 1])
                g.db.commit()
            g.db.close()
        else:
            for guide in guidestmp:
                guide['valid'] = int(request.form[guide['uid']])
                if guide['valid'] == 2:
                    g.db.execute('delete from guide where id = ? and gid = ?',
                                 [guide['id'], guide['id_guide']])
                elif guide['valid'] == 1:
                    g.db.execute('delete from guide where id = ? and valid = ?',
                                 [guide['id'], 1])
                    g.db.execute('update guide set valid = ? where id = ? and guide_id = ?',
                                 [1, guide['id'], guide['id_guide']])
                g.db.commit()
                g.db.close()
    return render_template('guides_adm.html', guides=guides, guidestmp=guidestmp)
