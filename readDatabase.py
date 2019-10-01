import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_fall(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM fall")

    rows = cur.fetchall()

    fall_liste_tp = []

    for row in rows:
        fall_liste_tp.append(row)

    fall_liste = [list(elem) for elem in fall_liste_tp]
    return fall_liste


def select_fall_infos(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    cur.execute("SELECT * FROM fall_infos")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_gesetzbuecher(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM gesetzbuecher")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_namen(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM namen")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    database = r"D:\\CODE\\Python\\RichterKI\\db\\FallDatabase.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("fall")
        select_fall(conn)
        print("")

        print("fall_infos")
        select_fall_infos(conn)
        print("")

        print("gesetzbuecher")
        select_gesetzbuecher(conn)
        print("")

        print("namen")
        select_namen(conn)
        print("")


def getFall():
    database = r"D:\\CODE\\Python\\RichterKI\\db\\FallDatabase.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # print("fall")

        # print("")
        return select_fall(conn)


def fall_id(conn):
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    cur.execute("SELECT * FROM fall")

    # rows = cur.fetchall()

    zlist = []

    tupls = cur.fetchall()

    for tup in tupls:

        t = str(tup).replace("('", "").replace("',)", "")

        zlist.append(t)

        return zlist

    # for row in rows:
    #     print(row)
    #    return row


def get_fall_id():
    database = r"D:\\CODE\\Python\\RichterKI\\db\\FallDatabase.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        return fall_id(conn)


if __name__ == '__main__':
    main()
