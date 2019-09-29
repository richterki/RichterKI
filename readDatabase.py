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

    for row in rows:
        # print(row)
        return str(row)


def select_fall_infos(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
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
        return str(select_fall(conn))


if __name__ == '__main__':
    main()
