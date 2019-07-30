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


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "db/pythonsqlite_neu.db"

    sql_create_fall_table = """ CREATE TABLE IF NOT EXISTS fall (
                                        fall_id integer PRIMARY KEY,
                                        stadt_id text NOT NULL,
                                        urteil text,
                                        schlagwoerter text
                                    ); """

    sql_create_fall_infos_table = """CREATE TABLE IF NOT EXISTS fall_infos (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    sql_create_namen_table = """CREATE TABLE IF NOT EXISTS namen (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    sql_create_gesetzbuecher_liste_table = """CREATE TABLE IF NOT EXISTS gesetzbuecher_liste (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    sql_create_gesetzbuecher_table = """CREATE TABLE IF NOT EXISTS gesetzbuecher (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create fall table
        create_table(conn, sql_create_fall_table)
        # create fall_infos table
        create_table(conn, sql_create_fall_infos_table)
        # create namen table
        create_table(conn, sql_create_namen_table)
        # create gesetzbuecher_liste table
        create_table(conn, sql_create_gesetzbuecher_liste_table)
        # create gesetzbuecher table
        create_table(conn, sql_create_gesetzbuecher_table)
    else:
        print("Error! cannot create the database connection.")
