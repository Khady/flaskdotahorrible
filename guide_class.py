#-*- encoding: utf-8 -*-

import sqlite3
from flask import render_template, g, url_for, redirect, request, Markup, session, flash
from dota2 import app

def connect_db(base):
    return sqlite3.connect(base)

class Guide:
    """ Gestion des guides en base """
    def __init__(self):
        self.id = -1
        self.gid = -1
        self.hero = -1
        self.heroname = ""
        self.autor = ""
        self.title = ""
        self.tag = ""
        self.diff = -1
        self.untouch = ""
        self.markup = ""
        self.dateCreate = ""
        self.dateModif = ""
        self.valid = 0
        self.score = 0

    def get_frombase(self, id_guide, gid, valid):
        g.db = connect_db(app.config['USER_DB'])
        print valid, id_guide
        if valid == 1:
            cur = g.db.execute('select * from guide where id = ? and valid = ?', [id_guide, valid])
        else:
            cur = g.db.execute('select * from guide where id = ? and guide_id = ?', [id_guide, gid])
        row = cur.fetchall()[0]
        self.id = row[0]
        self.gid = row[1]
        self.hero = row[2]
        self.heroname = row[3]
        self.autor = row[4]
        self.title = row[5]
        self.tag = row[6]
        self.diff = row[7]
        self.untouch = row[8]
        self.markup = row[9]
        self.dateCreate = row[10]
        self.dateModif = row[11]
        self.valid = row[12]
        self.score = row[13]
        g.db.close()

    def get_indict(self):
        pass

    def new_gid(self, id_guide):
        if id_guide == -1:
            gid = 0
        else:
            g.db = connect_db(app.config['USER_DB'])
            cur = g.db.execute('select count(guide_id) from guide where id = ?', [id_guide])
            gid = cur.fetchall()[0][0]
            g.db.close()
        return gid + 1

    def update(self):
        g.db = connect_db(app.config['USER_DB'])
        if self.gid != -1:
            selectstr = 'update guide set hero = ?, heroname = ?,\
autor = ?, title = ?, tag = ?, difficulties = ?, content_untouch = ?, content_markup = ?,\
date_create = ?, date_last_modif = ?, valid = ?, score = ? where id = ? and valid = 1'
            g.db.execute(selectstr,
                         [self.hero,
                          self.heroname,
                          self.autor,
                          self.title,
                          self.tag,
                          self.diff,
                          self.untouch,
                          self.markup,
                          self.dateCreate,
                          self.dateModif,
                          self.valid,
                          self.score,
                          self.id])
        else:
            g.db.execute('insert into guide (id, guide_id, hero, heroname,\
autor, title, tag, difficulties, content_untouch, content_markup, date_create, date_last_modif, valid, score)\
values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                         [self.id,
                          self.gid,
                          self.hero,
                          self.heroname,
                          self.autor,
                          self.title,
                          self.tag,
                          self.diff,
                          self.untouch,
                          self.markup,
                          self.dateCreate,
                          self.dateModif,
                          self.valid,
                          self.score])
        g.db.commit()
        g.db.close()

    def create(self):
        g.db = connect_db(app.config['USER_DB'])
        nid = g.db.execute('select max(id) from guide').fetchall()[0][0]
        if nid is None:
            nid = 1
        else:
            nid += 1
        g.db.execute('insert into guide (id, guide_id, hero, heroname,\
autor, title, tag, difficulties, content_untouch, content_markup, date_create, date_last_modif, valid, score)\
values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [nid,
                      self.gid,
                      self.hero,
                      self.heroname,
                      self.autor,
                      self.title,
                      self.tag,
                      self.diff,
                      self.untouch,
                      self.markup,
                      self.dateCreate,
                      self.dateModif,
                      self.valid,
                      self.score])
        g.db.commit()
        g.db.close()

    def save(self):
        if self.id == -1:
            self.create()
        else:
            self.update()
