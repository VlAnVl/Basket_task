import sqlite3 as sq3

con = sq3.connect("data_test.db")
cur = con.cursor()

direction_info = [('080200.62', 'Менеджмент'),
                  ('030900.62', 'Юриспруденция'),
                  ('210700.62', 'Информационные технологии')]
for di in direction_info:
    cur.execute('INSERT INTO direction (code_direction, title_direction) VALUES (?, ?)', di)

profile_info = [('Информационный менеджмент', 'РТФ', 1),
                ('Управление проектом', 'ЭФ', 1),
                ('Информационный менеджмент', 'РТФ', 2),
                ('Оптические системы и сети связи', 'РТФ', 3),
                ('Системы радиосвязи и радиодоступа', 'РТФ', 3),
                ('Системы мобильной связи', 'РТФ', 3)]
for pi in profile_info:
    cur.execute('INSERT INTO profile (title_profile, title_faculty, id_direction) VALUES (?, ?, ?)', pi)

user_info = [('Иванов', 'Максим', 'Викторович'),
             ('Петров', 'Артем', 'Алексеевич'),
             ('Сидорова', 'Мария', 'Владимировна')]
for ui in user_info:
    cur.execute('INSERT INTO user (surname_user, name_user, midle_name_user) VALUES (?, ?, ?)', ui)

basket_info = [(1, 1),
               (2, 1),
               (3, 1)]
for bi in basket_info:
    cur.execute('INSERT INTO basket (id_direction, id_user) VALUES (?, ?)', bi)

basket_profile_info = [(1, 1),
                       (2, 1),
                       (3, 2),
                       (4, 3),
                       (5, 3),
                       (6, 3)]
for bpi in basket_profile_info:
    cur.execute('INSERT INTO basket_profile (code_profile, id_basket) VALUES (?, ?)', bpi)

con.commit()
cur.close()
con.close()