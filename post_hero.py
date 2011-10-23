import sqlite3
from flask import render_template, g, url_for, redirect, request, session
from dota2 import app
from droits import get_droits

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/post_hero/', methods=['GET', 'POST'])
@app.route('/post_hero/<name>', methods=['GET', 'POST'])
def post_hero(name=None):
    if 'logged_in' in session:
        uid = session['user_id']
        g.db = connect_db(app.config['USER_DB'])
        droits = get_droits(uid)
        g.db.close()
        if droits['adm'] == 1:
            if (request.method == 'POST'):
                g.db = connect_db(app.config['USER_DB'])
                cur = g.db.execute('select id from hero where nam like ?',
                                   [request.form['nam']])
                entries = [dict(name=row[0]) for row in cur.fetchall()]
                if len(entries) == 0:
                    g.db.execute('insert into hero (nam, typ, des, bio, str_start, agi_start, int_start, str_lvl, agi_lvl, int_lvl, life, mana, damages, range, cast_speed, anim_speed, vision, armor, aspeed, ms) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                 [request.form['nam'], request.form['typ'],
                                  request.form['des'], request.form['bio'],
                                  request.form['str_start'],
                                  request.form['agi_start'],
                                  request.form['int_start'],
                                  request.form['str_lvl'],
                                  request.form['agi_lvl'],
                                  request.form['int_lvl'],
                                  request.form['life'], request.form['mana'],
                                  request.form['damages'],
                                  request.form['range'],
                                  request.form['cast_speed'],
                                  request.form['anim_speed'],
                                  request.form['vision'],
                                  request.form['armor'],
                                  request.form['aspeed'],
                                  request.form['ms']])
                else:
                    g.db.execute('update hero set typ = ?, des = ?, bio = ?, str_start = ?, agi_start = ?, int_start = ?, str_lvl = ?, agi_lvl = ?, int_lvl = ?, life = ?, mana = ?, damages = ?, range = ?, cast_speed = ?, anim_speed = ?, vision = ?, armor = ?, aspeed = ?, ms = ?, nam = ? where nam like ?',
                                 [request.form['typ'], request.form['des'],
                                  request.form['bio'],
                                  request.form['str_start'],
                                  request.form['agi_start'],
                                  request.form['int_start'],
                                  request.form['str_lvl'],
                                  request.form['agi_lvl'],
                                  request.form['int_lvl'],
                                  request.form['life'],
                                  request.form['mana'],
                                  request.form['damages'],
                                  request.form['range'],
                                  request.form['cast_speed'],
                                  request.form['anim_speed'],
                                  request.form['vision'],
                                  request.form['armor'],
                                  request.form['aspeed'],
                                  request.form['ms'], request.form['nam'],
                                  request.form['nam']])
                    g.db.commit()
                    g.db.close()
                return redirect(url_for('hero', name = request.form['nam']))
            else:
                if name == None:
                    return render_template('post_hero.html')
                else:
                    g.db = connect_db(app.config['USER_DB'])
                    cur = g.db.execute('select * from hero where nam like ?',
                                       [name])
                    entries = [dict(id_hero=row[0], nam=row[1], typ=row[2],
                                    des=row[3], bio=row[4], str_start=row[5],
                                    agi_start=row[6], int_start=row[7],
                                    str_lvl=row[8], agi_lvl=row[9],
                                    int_lvl=row[10], life=row[11],
                                    mana=row[12], damages=row[13],
                                    rang=row[14], cast_speed=row[15],
                                    anim_speed=row[16], vision=row[17],
                                    armor=row[18], aspeed=row[19],
                                    ms=row[20]) for row in cur.fetchall()]
                    g.db.close()
                    if (len(entries) == 0):
                        return render_template('post_hero.html')
                    else:
                        return render_template('post_hero.html',
                                               entries = entries)
    return redirect(url_for('default'))
