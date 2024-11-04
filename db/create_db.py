import sqlite3 as sq3

con = sq3.connect("data_test.db")
cur = con.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS direction(
id_direction INTEGER PRIMARY KEY,
code_direction TEXT NOT NULL,
title_direction TEXT NOT NULL
)''') # Направление

cur.execute('''
CREATE TABLE IF NOT EXISTS profile(
code_profile INTEGER PRIMARY KEY,
title_profile TEXT NOT NULL,
title_faculty TEXT NOT NULL,
id_direction  INTEGER,
FOREIGN KEY(id_direction ) REFERENCES direction(id_direction )
)''') # Профиль

cur.execute('''
CREATE TABLE IF NOT EXISTS basket(
id_basket INTEGER PRIMARY KEY,
id_direction INTEGER,
id_user INTEGER,
FOREIGN KEY(id_direction) REFERENCES direction(id_direction),
FOREIGN KEY(id_user) REFERENCES direction(id_user)
)''') # Корзина

cur.execute('''
CREATE TABLE IF NOT EXISTS basket_profile(
id_basket_profile INTEGER PRIMARY KEY,
code_profile INTEGER,
id_basket INTEGER,
FOREIGN KEY(code_profile) REFERENCES profile(code_profile),
FOREIGN KEY(id_basket) REFERENCES basket(id_basket)
)''') # Корзина профилей

cur.execute('''
CREATE TABLE IF NOT EXISTS user(
id_user INTEGER PRIMARY KEY,
surname_user TEXT,
name_user TEXT,
midle_name_user TEXT
)''') # Пользователь

con.commit()
cur.close()
con.close()