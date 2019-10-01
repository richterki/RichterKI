import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_fall(conn, fall):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO fall(fall_id,stadt_id,verurteilt,urteil,anklage,schlagwoerter)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, fall)
    return cur.lastrowid


def create_fall_infos(conn, fall_infos):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO fall_infos(fall_id,protokoll,anklage,urteil)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, fall_infos)
    return cur.lastrowid


def create_gesetzbuecher(conn, gesetzbuecher):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO gesetzbuecher(buch_id,paragraphen,absatz,inhalt)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, gesetzbuecher)
    return cur.lastrowid


def create_namen(conn, namen):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO namen(fall_id,klaeger,angeklagter,richter)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, namen)
    return cur.lastrowid


def main():
    database = r"D:\\CODE\\Python\\RichterKI\\db\\FallDatabase.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # fall
        print('===FALL===')
        fall = (int(input('fall_id >> ')), int(input('stadt_id >> ')), int(input('verurteilt (0/1) >> ')),
                input('urteil >> '), input('anklage >> '), input('schlagwoerter >> '))
        create_fall(conn, fall)

        # fall_infos
        print('===FALL INFOS===')
        fall_infos = (int(input('fall_id >> ')), input('protokoll >> '),
                      input('anklage >> '), input('urteil >> '))
        create_fall_infos(conn, fall_infos)

        # gesetzbuecher
        print('===GESETZBÜCHER===')
        gesetzbuecher = (int(input('buch_id >> ')), int(input('paragraphen >> ')),
                         input('absatz >> '), input('inhalt >> '))
        create_gesetzbuecher(conn, gesetzbuecher)

        # namen
        print('===NAMEN===')
        namen = (int(input('fall_id >> ')), input('klaeger >> '),
                 input('angeklagter >> '), input('richter >> '))
        create_namen(conn, namen)

        print('Datenbank wurde beschrieben')


if __name__ == '__main__':
    main()
