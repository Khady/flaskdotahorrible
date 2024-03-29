#-*- encoding: utf-8 -*-

import sqlite3
from flask import render_template, g, url_for, redirect, Markup
from dota2 import app

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/hero/')
@app.route('/hero/<name>')
def hero(name=None):
    g.db = connect_db(app.config['USER_DB'])
    if name == None:
        cur = g.db.execute('select nam, typ, des from hero order by nam asc')
        entries = [dict(name=row[0],type=row[1],des=row[2]) for row in cur.fetchall()]
        g.db.close()
        return render_template('hero-list.html', entries = entries)
    else:
        cur = g.db.execute('select * from hero where nam like ?', [name])
        entries = [dict(id_hero=row[0], name=row[1], typ=row[2], des=row[3],
                        bio=row[4], str_start=row[5], agi_start=row[6],
                        int_start=row[7], str_lvl=row[8], agi_lvl=row[9],
                        int_lvl=row[10], life=row[11], mana=row[12],
                        damages=row[13], rang=row[14], cast_speed=row[15],
                        anim_speed=row[16], vision=row[17], armor=row[18],
                        aspeed=row[19], ms=row[20]) for row in cur.fetchall()]
        if len(entries) == 0:
            g.db.close()
            return redirect(url_for('hero'))
        cur = g.db.execute('select * from spells where name_hero = ? order by pos asc', [entries[0]['name']])
        spells = [dict(id_spell=row[0], name_hero=row[1], name=row[2],
                       tooltip=Markup(row[3]),
                       pos=row[5]) for row in cur.fetchall()]
        g.db.close()
        return render_template('hero.html', entries=entries,
                               spells=spells)
