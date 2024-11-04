import pathlib
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import sqlite3 as sq3

app = Flask(__name__)

path_db = pathlib.Path('..') / 'db' / 'data_test.db'

def check_auto(id_user):
    con = sq3.connect(path_db)
    cur = con.cursor()
    cur.execute('''SELECT EXISTS (SELECT 1 FROM user WHERE id_user = ?)''', id_user)
    r = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return r[0][0] > 0


def get_user_name(id_user):
    con = sq3.connect(path_db)
    cur = con.cursor()
    cur.execute('''SELECT name_user FROM user WHERE id_user = ?''', id_user)
    r = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return r[0][0]


def get_direction():
    con = sq3.connect(path_db)
    cur = con.cursor()
    cur.execute('''SELECT id_direction, code_direction, title_direction
                FROM direction''')
    directions = cur.fetchall()
    dict_direction = {}
    dict_profile = {}
    for direction in directions:
        dict_direction[direction[0]] = direction[1:]
        cur.execute('''SELECT code_profile, title_profile, title_faculty, id_direction
                        FROM profile
                        WHERE id_direction = ?''', str(direction[0]))
        profiles = cur.fetchall()
        for profile in profiles:
            dict_profile[profile[0]] = profile[1:]
    con.commit()
    cur.close()
    con.close()
    return (dict_direction, dict_profile)

def get_user_basket(id_user):
    con = sq3.connect(path_db)
    cur = con.cursor()
    cur.execute('''SELECT id_basket, direction.id_direction, code_direction, title_direction
            FROM basket, direction, user
            WHERE basket.id_user = ? AND direction.id_direction = basket.id_direction
            GROUP BY id_basket''', id_user)
    basket_directions = cur.fetchall()
    dict_basket_direction = {}
    dict_basket_profile = {}
    for direction in basket_directions:
        dict_basket_direction[direction[0]] = direction[1:]
        cur.execute('''SELECT id_basket_profile, basket_profile.code_profile, title_profile, title_faculty
                           FROM basket, profile, basket_profile
                           WHERE profile.code_profile = basket_profile.code_profile AND basket_profile.id_basket = ?
                           GROUP BY id_basket_profile''', str(direction[0]))
        profiles = cur.fetchall()
        for profile in profiles:
            dict_basket_profile[profile[0]] = profile[1:] + (direction[1], )
    con.commit()
    cur.close()
    con.close()
    return (dict_basket_direction, dict_basket_profile)

def delete_user_basket(id_user):
    con = sq3.connect(path_db)
    cur = con.cursor()
    cur.execute('''SELECT id_basket 
                            FROM basket
                            WHERE id_user = ?''', id_user)
    id_basket = cur.fetchall()
    for ib in id_basket:
        cur.execute('''SELECT id_basket_profile 
                                    FROM basket_profile
                                    WHERE id_basket = ?''', ib)
        id_basket_profile = cur.fetchall()
        for ibp in id_basket_profile:
            cur.execute('''DELETE FROM basket_profile
                            WHERE id_basket_profile = ?''', ibp)
        cur.execute('''DELETE FROM basket
                            WHERE id_basket = ?''', ib)
    con.commit()
    cur.close()
    con.close()

def add_user_basket(id_user, dict_basket):
    con = sq3.connect(path_db)
    cur = con.cursor()
    for id_direction in dict_basket:
        cur.execute('INSERT INTO basket (id_direction, id_user) VALUES (?, ?)', (id_direction, id_user))
        cur.execute('''SELECT id_basket
                        FROM basket
                        WHERE id_direction = ? AND id_user = ?''', (id_direction, id_user))
        id_basket = cur.fetchall()
        for code_profile in dict_basket[id_direction]:
           cur.execute('INSERT INTO basket_profile (code_profile, id_basket) VALUES (?, ?)', (code_profile, id_basket[0][0]))
    con.commit()
    cur.close()
    con.close()


@app.route('/', methods=['GET', 'POST'])
@app.route('/authorization', methods=['GET', 'POST'])
def autorization():
    if request.method == 'POST':
        id_user = request.form.get('id_user')
        if check_auto(id_user):
            return redirect(url_for('basket', id_user = id_user))
    return render_template('authorization.html')


@app.route('/basket/<id_user>', methods=['GET', 'POST'])
def basket(id_user):
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            delete_user_basket(id_user)
            if len(data) != 0:
                correct_data = dict(zip(data['array_id_dir'], data['array_id_pro']))
                add_user_basket(id_user, correct_data)
    str_name = get_user_name(id_user)
    # Получаем направления и профили
    directions = get_direction()
    data_direction, data_profile = directions
    baskets = get_user_basket(id_user)
    data_basket, data_basket_profile = baskets
    return render_template('basket.html',
                           id_user = id_user,
                           name = str_name,
                           direction = data_direction,
                           profile = data_profile,
                           basket = data_basket,
                           basket_profile = data_basket_profile)


if __name__ == '__main__':
    app.run(debug=True)