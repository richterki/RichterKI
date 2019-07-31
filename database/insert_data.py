import sqlite3
# Insert EOD stats into the reports table

connectionObject = sqlite3.connect("../db/test.db")
cursorObject = connectionObject.cursor()

insertValues = "INSERT INTO fall values(1,40.1)"
cursorObject.execute(insertValues)


insertValues = "INSERT INTO temperature values(2,65.4)"

# cursorObject.execute(insertValues)


def add_fall():
    fall_id = input("Geben sie die Fall-ID ein: ")
    stadt_id = input("Geben sie die Stadt-ID ein: ")
    urteil = input("Geben sie das Urteil ein: ")
    schlagwoerter = input("Geben sie die Schlagwörter ein: ")

    insertValues = "INSERT INTO fall values(1,40.1)"
    cursorObject.execute(insertValues)


def add_fall_infos():
    pass


def add_namen():
    pass


def add_gesetzbuecher_liste():
    pass


def add_gesetzbuecher():
    pass
