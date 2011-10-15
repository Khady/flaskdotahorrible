import sqlite3
from flask import render_template, g, url_for, redirect
from dota2 import app

def connect_db(base):
    return sqlite3.connect(base)

@app.route('/item/')
@app.route('/item/<name>')
def item(name=None):
    g.db = connect_db(app.config['USER_DB'])
    if name == None:
        cur = g.db.execute('select nam from items order by nam asc')
        entries = [dict(name=row[0]) for row in cur.fetchall()]
        g.db.close()
        return render_template('item-list.html', entries = entries)
    else:
        cur = g.db.execute('select * from items where nam like ?', [name])
        entries = [dict(id_item=row[0], name=row[1], price=row[2],
                        recette=row[3], use_in=row[4], des=row[5],
                        str_stat=row[6], agi_stat=row[7], int_stat=row[8],
                        armor=row[9], aspeed=row[10], ms=row[11], life=row[12],
                        mana=row[13], reg_life=row[14], reg_mana=row[15],
                        orb=row[16], aura=row[17], cap_pas=row[18],
                        cap_act=row[19]) for row in cur.fetchall()]
        if len(entries) == 0:
            g.db.close()
            return redirect(url_for('item'))
        g.db.close()
        return render_template('item.html', entries=entries)
