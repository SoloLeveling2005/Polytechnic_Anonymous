import sqlite3 as sql




def create_db():
    with sql.connect("todo.db") as con:
        cur = con.cursor()
        cur.execute(f"""
                CREATE TABLE IF NOT EXISTS connections (
                    ID INTEGER NOT NULL,
                    first INT NOT NULL,
                    second INT NOT NULL,

                    PRIMARY KEY(ID AUTOINCREMENT)
                )
                """)
    with sql.connect("todo.db") as con:
        cur = con.cursor()
        cur.execute(f"""
                CREATE TABLE IF NOT EXISTS requests (
                    id_user INTEGER NOT NULL,

                    PRIMARY KEY(id_user)
                )
                """)
    # with sql.connect("todo.db") as con:
    #     cur = con.cursor()
    #     cur.execute(f"""
    #             CREATE TABLE IF NOT EXISTS applications (
    #                 id_user INTEGER NOT NULL
    #
    #             )
    #             """)
    # with sql.connect("todo.db") as con:
    #     cur = con.cursor()
    #     cur.execute(f"""
    #             CREATE TABLE IF NOT EXISTS users (
    #                 id_user INTEGER NOT NULL,
    #                 step VARCHAR(30) NOT NULL
    #
    #             )
    #             """)