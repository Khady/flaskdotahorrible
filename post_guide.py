import sqlite3
import re
import Mail
from flask import render_template, g, url_for, redirect, request, Markup, session
from markdown import markdown
from dota2 import app
from droits import get_droits
from datetime import datetime

def connect_db(base):
    return sqlite3.connect(base)

def parse_tbl(content):
    g.db = connect_db(app.config['USER_DB'])
    tbl = re.compile(r'\[lvl=[1-5,]*\]')
    tableaux = tbl.findall(content)
    contenttmp = tbl.split(content)
    i = 0
    guide = ""
    for tab in tableaux:
        guide += contenttmp[i]
        i += 1
        guide += "<table border><caption>Sorts</caption>"
        tab = re.findall(r'[1-5]', tab)
        for ligne in range(5):
            guide += "<tr><td>sort %i</td>" % (ligne + 1)
            for lvl in range(len(tab)):
                guide += "<td>"
                if ligne + 1 == int(tab[lvl]):
                    guide += "X"
                else:
                    guide += " "
                guide += "</td>"
            guide += "</tr>"
        guide += "</table>"
    guide += contenttmp[i]
    return (guide)

def parse_hero(content):
    hero = re.compile(r'\[hero=[a-zA-Z ]*\]')
    g.db = connect_db(app.config['USER_DB'])
    heros = hero.findall(content)
    contenttmp = hero.split(content)
    guide = ""
    i = 0
    for hro in heros:
        guide += contenttmp[i]
        i += 1
        hroname = re.search(r'=[a-zA-Z]*', hro).group(0)[1:]
        cur = g.db.execute('select * from hero where nam like ?', [hroname])
        hroinfos = [dict(name=row[1]) for row in cur.fetchall()]
        if len(hroinfos) != 0:
            guide += hroname
        else:
            guide += "erreur : %s" % hro
    guide += contenttmp[i]
    return guide


def parse_spell(content):
    g.db = connect_db(app.config['USER_DB'])
    spell = re.compile(r'\[spell=[a-zA-Z]*\]')
    spells = spell.findall(content)
    contenttmp = spell.split(content)
    guide = ""
    i = 0
    for spl in spells:
        guide += contenttmp[i]
        i += 1
        splname = re.search(r'=[a-zA-Z]*', spl).group(0)[1:]
        cur = g.db.execute('select id, des from spells where nam like ?', [splname])
        entries = [dict(id=row[0], desc=row[1]) for row in cur.fetchall()]
        if len(entries) != 0:
            entries = entries[0]
            cur = g.db.execute("select cd, mana_cost, life_cost, effect from spells_effect where lvl_spell = ? and id = ?", [4, int(entries['id'])])
            effects = [dict(cd=row[0], mana=row[1], life=row[2], effect=row[3]) for row in cur.fetchall()][0]
            guide += splname
        else:
            guide += "erreur : %s" % spl
    guide += contenttmp[i]
    return guide


def parse_item(content):
    g.db = connect_db(app.config['USER_DB'])
    item = re.compile(r'\[item=[a-zA-Z ]*\]')
    items = item.findall(content)
    contenttmp = item.split(content)
    guide = ""
    i = 0
    for itm in items:
        guide += contenttmp[i]
        i += 1
        itmname = re.search(r'=[a-zA-Z]*', itm).group(0)[1:]
        cur = g.db.execute('select * from items where nam like ?', [itmname])
        itminfos = [dict(name=row[1]) for row in cur.fetchall()]
        if len(itminfos) != 0:
            guide += itmname
        else:
            guide += "erreur : %s" % itm
    guide += contenttmp[i]
    return guide

def parse_balise(content):
    content = parse_tbl(content)
    content = parse_item(content)
    content = parse_hero(content)
    content = parse_spell(content)
    return content


def valid_guide(heros):
    error = None
    if len(request.form['titre']) == 0:
        error = "Pas de titre"
    elif len(request.form['content']) == 0:
        error = "Pas de contenu"
    elif len(request.form['difficulte']) == 0:
        error = "Pas de difficulte"
    if error != None:
        hid = request.form['hero']
        titre=request.form['titre']
        content=request.form['content']
        tag=request.form['tag']
        diff = request.form['difficulte']
        return render_template('post_guide.html', error=error,
                               hero=heros, herolen=len(heros), hid=hid, # heros liste
                               titre=titre, tag=tag, content=content, diff=diff)
    else:
        return True

def add_guide():
    g.db = connect_db(app.config['USER_DB'])
    g.db.execute('insert into guide (title, autor, tag, hero, heroname, difficulties, content_untouch, content_markup, date_create, date_last_modif, valid, score) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 [request.form['titre'],
                  session['user_login'],
                  request.form['tag'],
                  request.form['hero'],
                  get_heroName(request.form['hero']),
                  request.form['difficulte'],
                  request.form['content'],
                  markdown(Markup.escape(request.form['content'])),
                  datetime.today(), datetime.today(),
                  0, 0])
    g.db.commit()


def update_guide(id_guide):
    g.db = connect_db(app.config['USER_DB'])
    g.db.execute('update guide set title = ?, tag = ?, hero = ?, heroname = ?, difficulte = ?, content_untouch = ?, content_markup = ?, date_last_modif = ? where id = ?',
                 [request.form['titre'],
                  request.form['tag'],
                  request.form['hero'],
                  get_heroName(request.form['hero']),
                  request.form['difficulte'],
                  request.form['content'],
                  parse_balise(markdown(Markup.escape(request.form['guide']))),
                  datetime.today(), id_guide])
    g.db.commit()


def get_heros():
    g.db = connect_db(app.config['USER_DB'])
    cur = g.db.execute('select id, nam from hero')
    hero = [dict(id=row[0], nom=row[1]) for row in cur.fetchall()]
    return hero

def get_heroName(id_hero):
    g.db = connect_db(app.config['USER_DB'])
    cur = g.db.execute('select nam from hero where id = ?', [id_hero])
    heroname = [row[0] for row in cur.fetchall()][0]
    return heroname

def mail_guide(id_guide):
    g.db = connect_db(app.config['USER_DB'])
    mail = ""
    cur = g.db.execute('select id_user from user_group where id_group = ?', [1])
    users = [row[0] for row in cur.fetchall()]
    for user in users:
        cur = g.db.execute('select mail from user_description where id = ?', [user])
        mail = [row[0] for row in cur.fetchall()][0]
        Mail.send(mail, "Nouveau guide",
                  ("Un nouveau guide (ou une mise a jour d'un guide) est disponible.\n%s"
                   % url_for('guide', id_guide = id_guide)))

@app.route('/post_guide/', methods = ['GET', 'POST'])
@app.route('/post_guide/<int:id_guide>', methods = ['GET', 'POST'])
def post_guide(id_guide=None):
    if 'logged_in' in session:
        uid = session['user_id']
        g.db = connect_db(app.config['USER_DB'])
        droits = get_droits(uid)
        g.db.close()
        heros = get_heros()
        herolen = len(heros)
        if droits['guide'] == 1:
            if (request.method == 'POST'):
                if request.form['mode_post'] == 'Previsualisation':
                    guide = (Markup.escape(request.form['content']))
                    hid = request.form['hero']
                    titre=request.form['titre']
                    content=request.form['content']
                    tag=request.form['tag']
                    diff = request.form['difficulte']
                    return render_template('post_guide.html',
                                           previsualisation=1, guide=Markup(parse_balise(markdown(guide))), # previsualisation
                                           hero=heros, herolen=herolen, hid=hid,# heros liste
                                           titre=titre, tag=tag, content=content, diff=diff)
                else:
                    val = valid_guide(heros)
                    if val != True:
                        return val
                    print 'toto'
                    print id_guide
                    # mail_guide(id_guide)
                    if (id_guide == None):
                        id_guide = add_guide()
                    else:
                        update_guide(id_guide)
                        return redirect(url_for('guide', id_guide=id_guide))
            else:
                if (id_guide == None):
                    return render_template('post_guide.html', hero=heros, herolen=herolen)
                else:
                    g.db = connect_db(app.config['USER_DB'])
                    cur = g.db.execute('select title, autor, tag, difficulties, content_untouch from guide where id = ?',
                                       [id_guide])
                    row = cur.fetchall()
                    if len(row) != 0:
                        titre=row[0][0]
                        autor=row[0][1]
                        tag=row[0][2]
                        diff=row[0][3]
                        guide=row[0][4]
                        return render_template('post_guide.html',
                                               id_guide=id_guide,
                                               hero=heros, herolen=herolen,
                                               titre=titre, tag=tag, content=guide, diff=diff)
                    else:
                        return render_template('post_guide.html', hero=heros, herolen=herolen)
    return redirect(url_for('guide'))

