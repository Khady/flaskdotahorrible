#-*- encoding: utf-8 -*-

import sqlite3
from flask import render_template, g, url_for, redirect, request, session
from dota2 import app
from droits import get_droits

def connect_db(base):
    return sqlite3.connect(base)

def add_spell_base(name):
    g.db.execute('insert into spells (name_hero, nam, des, abi_type, tar_type, allo_tar, pos) values (?, ?, ?, ?, ?, ?, ?)',
                 [name, request.form['nam_skill'], request.form['des_skill'],
                  request.form['abi_type_skill'],
                  request.form['tar_type_skill'],
                  request.form['allo_tar_skill'], request.form['pos_skill']])
    g.db.commit()
    return

def update_spell_base(name):
    g.db.execute('update spells set nam = ?, des = ?, abi_type = ?, tar_type = ?, allo_tar = ?, pos = ? where name_hero like ?',
                 [request.form['nam_skill'], request.form['des_skill'],
                  request.form['abi_type_skill'],
                  request.form['tar_type_skill'],
                  request.form['allo_tar_skill'], request.form['pos_skill'],
                  name])
    g.db.commit()
    return

def recup_spell(i, entries):
    spell = []
    if len(entries):
        cur = g.db.execute('select * from spells_effect where id_spell = ? and lvl_spell = ? order by lvl_spell asc', [entries[0]["id_spell"], i])
        spell = [dict(id_spell_effect=row[0], id_spell=row[1],
                      lvl_spell=row[2], cd=row[3], rang=row[4],
                      mana_cost=row[5], life_cost=row[6], aoe=row[7],
                      effect=row[8]) for row in cur.fetchall()]
    return spell

def post_spell_lvl1(entries):
    if request.form['modif_lvl1'] == '1':
        g.db.execute('insert into spells_effect (id_spell, lvl_spell, cd, rang, mana_cost, life_cost, aoe, effect) values (?, ?, ?, ?, ?, ?, ?, ?)',
                     [entries[0]['id_spell'], 1,
                      request.form['cd_lvl1'],
                      request.form['rang_lvl1'],
                      request.form['mana_cost_lvl1'],
                      request.form['life_cost_lvl1'],
                      request.form['aoe_lvl1'],
                      request.form['effect_lvl1']])
        g.db.commit()
    else:
        g.db.execute('update spells_effect set cd = ?, rang = ?, mana_cost = ?, life_cost = ?, aoe = ?, effect = ? where id_spell = ? and lvl_spell = 1',
                     [request.form['cd_lvl1'],
                      request.form['rang_lvl1'],
                      request.form['mana_cost_lvl1'],
                      request.form['life_cost_lvl1'],
                      request.form['aoe_lvl1'],
                      request.form['effect_lvl1'],
                      entries[0]['id_spell']])
        g.db.commit()

def post_spell_lvl2(entries):
    if request.form['modif_lvl2'] == '1':
        g.db.execute('insert into spells_effect (id_spell, lvl_spell, cd, rang, mana_cost, life_cost, aoe, effect) values (?, ?, ?, ?, ?, ?, ?, ?)',
                     [entries[0]['id_spell'], 2,
                      request.form['cd_lvl2'],
                      request.form['rang_lvl2'],
                      request.form['mana_cost_lvl2'],
                      request.form['life_cost_lvl2'],
                      request.form['aoe_lvl2'],
                      request.form['effect_lvl2']])
        g.db.commit()
    else:
        g.db.execute('update spells_effect set cd = ?, rang = ?, mana_cost = ?, life_cost = ?, aoe = ?, effect = ? where id_spell = ? and lvl_spell = 2',
                     [request.form['cd_lvl2'],
                      request.form['rang_lvl2'],
                      request.form['mana_cost_lvl2'],
                      request.form['life_cost_lvl2'],
                      request.form['aoe_lvl2'],
                      request.form['effect_lvl2'],
                      entries[0]['id_spell']])
        g.db.commit()

def post_spell_lvl3(entries):
    if request.form['modif_lvl3'] == '1':
        g.db.execute('insert into spells_effect (id_spell, lvl_spell, cd, rang, mana_cost, life_cost, aoe, effect) values (?, ?, ?, ?, ?, ?, ?, ?)',
                     [entries[0]['id_spell'], 3,
                      request.form['cd_lvl3'],
                      request.form['rang_lvl3'],
                      request.form['mana_cost_lvl3'],
                      request.form['life_cost_lvl3'],
                      request.form['aoe_lvl3'],
                      request.form['effect_lvl3']])
        g.db.commit()
    else:
        g.db.execute('update spells_effect set cd = ?, rang = ?, mana_cost = ?, life_cost = ?, aoe = ?, effect = ? where id_spell = ? and lvl_spell = 3',
                     [request.form['cd_lvl3'],
                      request.form['rang_lvl3'],
                      request.form['mana_cost_lvl3'],
                      request.form['life_cost_lvl3'],
                      request.form['aoe_lvl3'],
                      request.form['effect_lvl3'],
                      entries[0]['id_spell']])
        g.db.commit()

def post_spell_lvl4(entries):
    if request.form['modif_lvl4'] == '1':
        g.db.execute('insert into spells_effect (id_spell, lvl_spell, cd, rang, mana_cost, life_cost, aoe, effect) values (?, ?, ?, ?, ?, ?, ?, ?)',
                     [entries[0]['id_spell'], 4,
                      request.form['cd_lvl4'],
                      request.form['rang_lvl4'],
                      request.form['mana_cost_lvl4'],
                      request.form['life_cost_lvl4'],
                      request.form['aoe_lvl4'],
                      request.form['effect_lvl4']])
        g.db.commit()
    else:
        g.db.execute('update spells_effect set cd = ?, rang = ?, mana_cost = ?, life_cost = ?, aoe = ?, effect = ? where id_spell = ? and lvl_spell = 4',
                     [request.form['cd_lvl4'],
                      request.form['rang_lvl4'],
                      request.form['mana_cost_lvl4'],
                      request.form['life_cost_lvl4'],
                      request.form['aoe_lvl4'],
                      request.form['effect_lvl4'],
                      entries[0]['id_spell']])
        g.db.commit()

@app.route('/post_spell/', methods=['GET', 'POST'])
@app.route('/post_spell/<name>', methods=['GET', 'POST'])
def post_spell(name=None):
    if 'logged_in' in session:
        uid = session['user_id']
        g.db = connect_db(app.config['USER_DB'])
        droits = get_droits(uid)
        g.db.close()
        if droits['adm'] == 1:
            if name == None:
                if (request.method == 'POST'):
                    return redirect(url_for('post_spell',
                                            name = request.form['hero'],
                                            pos = request.form['spell']))
                else:
                    g.db = connect_db(app.config['USER_DB'])
                    cur = g.db.execute('select nam from hero')
                    entries = [dict(name=row[0]) for row in cur.fetchall()]
                    g.db.close()
                    return render_template('post_spell.html', name=name,
                                           entries=entries, len=len(entries),
                                           i=0)
            else:
                if (request.method == 'POST'):
                    g.db = connect_db(app.config['USER_DB'])
                    if request.form['modif'] == '1':
                        add_spell_base(name)            
                    else:
                        update_spell_base(name)
                    cur = g.db.execute('select * from spells where name_hero like ? and pos = ?', [name, request.form['pos_skill']])
                    entries = [dict(id_spell=row[0],
                                    pos=row[7]) for row in cur.fetchall()]
                    post_spell_lvl1(entries)
                    post_spell_lvl2(entries)
                    post_spell_lvl3(entries)
                    post_spell_lvl4(entries)
                    g.db.close()
                    return redirect(url_for('hero', name=name))
                else:
                    g.db = connect_db(app.config['USER_DB'])
                    searchword = request.args.get('pos', '')
                    if searchword != '':
                        pos = int(searchword)
                    else:
                        pos = 1
                    cur = g.db.execute('select * from spells where name_hero like ? and pos = ? order by pos asc', [name, pos])
                    entries = [dict(id_spell=row[0], name_hero=row[1],
                                    nam=row[2], des=row[3],
                                    abi_type=row[4],
                                    tar_type=row[5], allo_tar=row[6],
                                    pos=row[7]) for row in cur.fetchall()]
                    spell1 = recup_spell(1, entries)
                    spell2 = recup_spell(2, entries)
                    spell3 = recup_spell(3, entries)
                    spell4 = recup_spell(4, entries)
                    g.db.close()
                    return render_template('post_spell.html', name=name,
                                           entries=entries,
                                           len_entries=len(entries),
                                           pos=pos, spell1=spell1,
                                           len_spell1=len(spell1),
                                           spell2=spell2,
                                           len_spell2=len(spell2),
                                           spell3=spell3,
                                           len_spell3=len(spell3),
                                           spell4=spell4,
                                           len_spell4=len(spell4))
    return redirect(url_for('default'))
