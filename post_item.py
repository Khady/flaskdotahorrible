import sqlite3
from flask import render_template, g, url_for, redirect, request, session
from dota2 import app
from droits import get_droits

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/post_item/', methods=['GET', 'POST'])
@app.route('/post_item/<name>', methods=['GET', 'POST'])
def post_hero(name=None):
    if 'logged_in' in session:
        uid = session['user_id']
        g.db = connect_db(app.config['USER_DB'])
        droits = get_droits(uid)
        g.db.close()
        if droits['adm'] == 1:
            if (request.method == 'POST'):
                g.db = connect_db(app.config['USER_DB'])
                cur = g.db.execute('select id from items where nam like ?',
                                   [request.form['nam']])
                entries = [dict(name=row[0]) for row in cur.fetchall()]
                if len(entries) == 0:
                    g.db.execute('insert into items (nam, price, recette, use_in, des, str, agi, inte, armor, aspeed, ms, life, mana, damages, reg_life, reg_mana, orb, aura, cap_pas, cap_act) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                 [request.form['nam'], request.form['prix'],
                                  request.form['recette'],
                                  request.form['use_in'],
                                  request.form['des'],
                                  request.form['str'],
                                  request.form['agi'],
                                  request.form['inte'],
                                  request.form['armor'],
                                  request.form['aspeed'],
                                  request.form['ms'],
                                  request.form['life'], request.form['mana'],
                                  request.form['damages'],
                                  request.form['reg_life'],
                                  request.form['reg_mana'],
                                  request.form['orb'],
                                  request.form['aura'],
                                  request.form['cap_pas'],
                                  request.form['cap_act']])
                else:
                    g.db.execute('update items set price = ?, recette = ?, use_in = ?, des = ?, str = ?, agi = ?, inte = ?, armor = ?, aspeed = ?, ms = ?, life = ?, mana = ?, damages = ?, reg_life = ?, reg_mana = ?, orb = ?, aura = ?, cap_pas = ?, cap_act = ?, nam = ? where nam like ?',
                                 [request.form['prix'],
                                  request.form['recette'],
                                  request.form['use_in'],
                                  request.form['des'],
                                  request.form['str'],
                                  request.form['agi'],
                                  request.form['inte'],
                                  request.form['armor'],
                                  request.form['aspeed'],
                                  request.form['ms'],
                                  request.form['life'],
                                  request.form['mana'],
                                  request.form['damages'],
                                  request.form['reg_life'],
                                  request.form['reg_mana'],
                                  request.form['orb'],
                                  request.form['aura'],
                                  request.form['cap_pas'],
                                  request.form['cap_act'],
                                  request.form['nam'],
                                  request.form['nam']])
                    g.db.commit()
                    g.db.close()
                return redirect(url_for('item', name = request.form['nam']))
            else:
                if name == None:
                    return render_template('post_item.html')
                else:
                    g.db = connect_db(app.config['USER_DB'])
                    cur = g.db.execute('select * from items where nam like ?',
                                       [name])
                    entries = [dict(id_item=row[0], nam=row[1], prix=row[2],
                                    recette=row[3], use_in=row[4],
                                    des=row[5],
                                    str=row[6], agi=row[7],
                                    inte=row[8], armor=row[9],
                                    aspeed=row[10], ms=row[11],
                                    life=row[12], mana=row[13],
                                    damages=row[14], reg_life=row[15],
                                    reg_mana=row[16], orb=row[17],
                                    aura=row[18], cap_pas=row[19],
                                    cap_act=row[20]) for row in cur.fetchall()]
                    g.db.close()
                    if (len(entries) == 0):
                        return render_template('post_item.html')
                    else:
                        return render_template('post_item.html',
                                               entries = entries)
    return redirect(url_for('default'))
