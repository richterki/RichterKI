import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_fall(conn, fall):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO fall(fall_id,stadt_id,urteil,schlagwoerter)
              VALUES(?,?,?,?) '''
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

    sql = ''' INSERT INTO fall_infos(fall_id,protokoll,urteil)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, fall_infos)
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


def create_gesetzbuecher_liste(conn, gesetzbuecher_liste):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO gesetzbuecher_liste(buch_id,name,justiz_bereich)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, gesetzbuecher_liste)
    return cur.lastrowid


def create_gesetzbuecher(conn, gesetzbuecher):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO gesetzbuecher(buch_id,paragraphen,absatz,inhalt,end_date)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, gesetzbuecher)
    return cur.lastrowid


def main():
    database = "db/pythonsqlite_neu.db"

    # create a database connection
    conn = create_connection(database)

    with conn:
        # create a new project

        """

        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
        project_id = create_project(conn, project)

        # tasks
        task_1 = ('Analyze the requirements of the app', 1,
                  1, project_id, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm with user about the top requirements',
                  1, 1, project_id, '2015-01-03', '2015-01-05')

        # create tasks
        create_task(conn, task_1)
        create_task(conn, task_2)

        """
        # Fall
        fall = ('', '', '', '')
        create_fall(conn, fall)
        # (fall_id,stadt_id,urteil,schlagwoerter)

        # Fall_infos
        fall_infos = ('', '', '')
        create_fall_infos(conn, fall_infos)
        # (fall_id,protokoll,urteil)

        # Namen
        namen = ('', '', '', '')
        create_namen(conn, namen)
        # (fall_id,klaeger,angeklagter,richter)

        # Gesetzbücherliste
        gesetzbuecher_liste = ('', '', '')
        create_gesetzbuecher_liste(conn, gesetzbuecher_liste)
        # (buch_id, name, justiz_bereich)

        # Gesetzbücher
        gesetzbuecher = ('', '', '', '', '')
        create_gesetzbuecher(conn, gesetzbuecher)
        # (buch_id,paragraphen,absatz,inhalt,end_date)


if __name__ == '__main__':
    main()
