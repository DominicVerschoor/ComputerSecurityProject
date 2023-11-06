import sqlite3
from database.set_up import create_table_cmd, insert_table_cmd


def connect_sqlite_db(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'Successfully connected to SQLite db version: {sqlite3.version}')
    except sqlite3.Error as e:
        print(f'Failed to connect with error: {e}')
    finally:
        if conn:
            c = conn.cursor()
            c.close()
            return conn


def set_up_sqlite_db(conn):
    try:
        cur = conn.cursor()
        cur.executescript(create_table_cmd)

        print(f'Successfully creating table.')
        cur.close()
    except sqlite3.Error as e:
        print(f'Error creating table: f{e}')


def insert_sqlite_db(conn, id, password, value=1):

    try:
        cur = conn.cursor()
        cur.execute(insert_table_cmd.format(id, password, value))
        conn.commit()

        print(f'Successfully inserting table.')
        cur.close()

    except sqlite3.Error as e:
        print(f'Error inserting table: f{e}')


if __name__ == '__main__':

    conn = connect_sqlite_db('database/server.db')
    set_up_sqlite_db(conn)
    insert_sqlite_db(conn, 1, "test_pass")

