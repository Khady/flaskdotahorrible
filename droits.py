#!/usr/bin/env python2
#-*- encoding: utf-8 -*-

import sqlite3
from flask import g
from dota2 import app

def connect_db(base):
    return sqlite3.connect(base)

def check_droits(user_id, droit):
    cur = g.db.execute('select id_group from user_group where id_user == ?', [user_id])
    for row in cur.fetchall():
        cur2 = g.db.execute('select %s from groupe where id == ?' % droit, [row[0]])
        for row2 in cur2.fetchall():
            if row2[0] == 1:
                return True
    return False

def get_droits(uid):
    droits = {'news': 0, 'guide': 0, 'adm': 0, 'groupe': 0}
    cur = g.db.execute('select id_group from user_group where id_user == ?', [uid])
    groups = [row[0] for row in cur.fetchall()]
    for group in groups:
        cur = g.db.execute('select news, guide, groupe, adm from groupe where id == ?', [group])
        row = cur.fetchall()
        if len(row) != 0:
            row = row[0]
            if row[0] == 1:
                droits['news'] = 1
            if row[1] == 1:
                droits['guide'] = 1
            if row[2] == 1:
                droits['groupe'] = 1
            if row[3] == 1:
                droits['adm'] = 1
    return droits

def create_group():
    pass

def delete_group():
    pass

def set_nom_group(gid, name):
    g.db.execute('update into groupe (nom) values (?) where id == ?',
                 [name, gid])

def get_nom_group(gid):
    cur = g.db.execute('select nom from groupe where id == ?', [gid])
    nom = cur.fetchall()[0][0]
    return nom

def set_droit_group(gid, name, droit):
    g.db.execute('update into groupe (?) values (?) where id == ?',
                 [name, droit, gid])

def set_droits_group(gid, droits):
    g.db.execute('update into groupe (news, guide, adm, groupe) values (?, ?, ?, ?) where if == ?',
                 [droits['news'], droits['guide'], droits['adm'], droits['groupe'], gid])

def get_droit_group(gid, droit):
    cur = g.db.execute('select ? from groupe where id == ?', [droit, gid])
    row = cur.fetchall()
    return row[0][0]

def get_droits_group(gid):
    cur = g.db.execute('select news, guide, adm, groupe from groupe where id == ?', [gid])
    row = cur.fetchall()
    droits = {'news':row[0][0], 'guide':row[0][1], 'adm':row[0][2], 'groupe':row[0][3]}
    return droits

def check_gadm(user_id):
    """ Cherche si l'utilisateur est gadmin dans un groupe """
    cur = g.db.execute('select gadm from user_group where id_user == ?', [user_id])
    for row in cur.fetchall():
        if row[0] == 1:
            return True
    return False

def get_gadm_list():
    """ recupere la liste des utilisateurs qui sont gadm """
    cur = g.db.execute('select id_user from user_group where gadm == 1', [uid])
    gadm = [row[0] for row in cur.fetchall()]
    return gadm

def get_gadm_names(uid):
    cur = g.db.execute('select id, nom from groupe where id in (select \
id_group from user_group where id_user = ? and gadm == 1)', [uid])
    groups = [dict(gid=row[0], nom=row[1]) for row in cur.fetchall()]
    return groups

def get_gadm(uid):
    """ Récupere un tableau avec la liste des groupes dans lequel l'user est gadmin """
    cur = g.db.execute('select id_group from user_group where id_user == ? and gadm == 1', [uid])
    gadm = [row[0] for row in cur.fetchall()]
    return gadm

def set_gadm(uid, gid):
    """ Rajoute les droits de gadmin a l'utilisateur """
    g.db.execute('update into user_group (gadm) values (1) where id_user == ? and id_group == ?',
                 [uid, gid])
