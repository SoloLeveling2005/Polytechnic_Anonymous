import time
import sqlite3 as sql
import threading


def application_threading():
    applications_thread = threading.Thread(target=application)
    applications_thread.daemon = True
    applications_thread.start()


def application():
    while True:
        with sql.connect('todo.db') as con:
            cur = con.cursor()
            cur.execute(f"""
                          SELECT * FROM requests;
                          """)
            requests_users = cur.fetchall()
            if len(requests_users) > 1:
                one_id = requests_users[0][0]
                two_id = requests_users[1][0]
                with sql.connect("todo.db") as con:
                    cur = con.cursor()
                    cur.execute(f"""
                            INSERT INTO connections (first,second) VALUES({one_id},{two_id})
                            """)
                    print("Данные добавлены в таблицу connections")
                with sql.connect('todo.db') as con:
                    cur = con.cursor()
                    cur.execute(f"""
                                      DELETE FROM requests WHERE id_user = {one_id};
                                      """)
                    print("Данные удалены с таблицы requests")
                with sql.connect('todo.db') as con:
                    cur = con.cursor()
                    cur.execute(f"""
                                  DELETE FROM requests WHERE id_user = {two_id};
                                  """)
                    print( "Данные удалены с таблицы requests")
        time.sleep(3)
