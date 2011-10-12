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

def get_grp_data():
    data = {'gname': 0, 'news': 0, 'guide': 0, 'adm': 0, 'groupe': 0}
    data['gname'] = request.form['gname']
    if 'news' in request.form:
        data['news'] = 1
    if 'guide' in request.form:
        data['guide'] = 1
    if 'groupe' in request.form:
        data['groupe'] = 1
    if 'adm' in request.form:
        data['adm'] = 1
    return data

def get_grp_droits(uid, gid):
    admin = check_droits(uid, "adm")
    adm_groups = check_droits(uid, "groupe")
    gadm = get_gadm(uid)
    if (admin == False and adm_groups == False and gid not in gadm):
        flash("Vous n'avez pas les droits pour modifier ce groupe")
        return False
    return True

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    g.db = connect_db(app.config['USER_DB'])
    error = None
    # variables de l'utilisateur
    if 'logged_in' in session:
        uid = session['user_id']
    else:
        uid = -1
        error = "You're not logged in"

    # droits
    admin = check_droits(uid, "adm")
    adm_groups = check_droits(uid, "groupe")
    gadm = check_gadm(uid)
    if admin or adm_groups:
        cur = g.db.execute('select id, nom from groupe')
        groups = [dict(gid=row[0], nom=row[1]) for row in cur.fetchall()]
    else:
        groups = get_gadm_names(uid)

    # affichage de la page sans modification de groupes
    if request.method == 'GET':
        gid = None
        g.db.close()
        return render_template('groups.html', error=error, admin=admin, adm_groups=adm_groups,
                               gid=gid, gadmin=gadm, len=len(groups), entries=groups)
    # gestion de la partie modification
    else:
        gid = request.form['group']
        ginfo = get_droits_group(gid)
        gname = get_nom_group(gid)
        g.db.close()
        return render_template('groups.html', error=error, admin=admin, adm_groups=adm_groups,
                               gadmin=gadm, len=len(groups), entries=groups,
                               gid=gid, gname=gname, news=ginfo['news'], guide=ginfo['guide'],
                               groupe=ginfo['groupe'], adm=ginfo['adm'])


@app.route('/groups/create', methods=['POST'])
def create_groups():
    g.db = connect_db(app.config['USER_DB'])
    # check si a les droits qu'il faut
    if 'logged_in' in session:
        uid = session['user_id']
    else:
        uid = -1
    admin = check_droits(uid, "adm")
    adm_groups = check_droits(uid, "groupe")
    gadm = get_gadm(uid)
    if (admin == False and adm_groups == False and gid not in gadm):
        flash("Vous n'avez pas les droits pour creer ce groupe")
        g.db.close()
        return redirect(url_for('groups'))
    # creation du nouveau groupe
    data = get_grp_data()
    # verifie qu'un groupe n'existe pas deja

    if data['gname'] != '':
        g.db.execute('insert into groupe (nom, news, guide, adm, groupe) values (?, ?, ?, ?, ?)',
                     [data['gname'], data['news'], data['guide'], data['adm'], data['groupe']])
        flash('groupe enregistre')
        g.db.commit()
    else:
        flash('Nom de groupe incorrect')
    g.db.close()
    return redirect(url_for('groups'))

@app.route('/groups/change', methods=['POST'])
@app.route('/groups/change/<int:gid>', methods=['POST'])
def change_groups(gid = None):
    g.db = connect_db(app.config['USER_DB'])
    # check si a les droits qu'il faut
    if 'logged_in' in session:
        uid = session['user_id']
    else:
        uid = -1
    if not get_grp_droits(uid, gid):
        g.db.close()
        return redirect(url_for('groups'))
    # modifie le groupe
    data = get_grp_data()
    if data['gname'] != '':
        g.db.execute('update groupe set nom = ?, news = ?, guide = ?, adm = ?, groupe = ? where id == ?',
                     [data['gname'], data['news'], data['guide'], data['adm'], data['groupe'], gid])
        flash('groupe %s modifie' % data['gname'])
        g.db.commit()
    else:
        flash('Nom de groupe incorrect')
    g.db.close()
    return redirect(url_for('groups'))

@app.route('/groups/add_user', methods=['POST'])
@app.route('/groups/add_user/<int:gid>', methods=['POST'])
def add_user_groups(gid = None):
    g.db = connect_db(app.config['USER_DB'])
    # check si a les droits qu'il faut
    if 'logged_in' in session:
        uid = session['user_id']
    else:
        uid = -1
    if not get_grp_droits(uid, gid):
        g.db.close()
        return redirect(url_for('groups'))
    # on recupere le formulaire
    uname = request.form['uname']
    if 'gadm' in request.form:
        gadm = 1
    else:
        gadm = 0
    # on ajoute l'utilisateur
    cur = g.db.execute('select login from user_description')
    entries = [row[0] for row in cur.fetchall()]
    if uname in entries:
        cur = g.db.execute('select id from user_description where login == ?', [uname])
        uid = cur.fetchall()[0][0]
    else:
        uid = -1
    if uid != -1:
        g.db.execute('insert into user_group (id_user, id_group, gadm) values (?, ?, ?)',
                     [uid, gid, gadm])
        g.db.commit()
        flash ('Utilisateur ajoute')
    else:
        flash('Nom utilisateur invalide')
    g.db.close()
    return redirect(url_for('groups'))
