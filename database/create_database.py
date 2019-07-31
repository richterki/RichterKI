import sqlite3


connectionObject = sqlite3.connect("../db/test.db")
cursorObject = connectionObject.cursor()


createTable_fall = "CREATE TABLE IF NOT EXISTS fall(fall_id int, stadt_id int, urteil varchar, schlagwoerter varchar(3,1))"
cursorObject.execute(createTable_fall)

createTable_fall_infos = "CREATE TABLE IF NOT EXISTS fall_infos(fall_id int, protokoll varchar, urteil varchar(3,1))"
cursorObject.execute(createTable_fall_infos)

createTable_namen = "CREATE TABLE IF NOT EXISTS namen(fall_id int, klaeger varchar, angeklagter varchar, richter varchar(3,1))"
cursorObject.execute(createTable_namen)

createTable_gesetzbuecher_liste = "CREATE TABLE IF NOT EXISTS gesetzbuecher_liste(buch_id int, name varchar, justiz_bereich varchar(3,1))"
cursorObject.execute(createTable_gesetzbuecher_liste)

createTable_gesetzbuecher = "CREATE TABLE IF NOT EXISTS gesetzbuecher(buch_id int, paragraphen int, absatz varchar, inhalt varchar(3,1))"
cursorObject.execute(createTable_gesetzbuecher)

# Insert EOD stats into the reports table

# insertValues = "INSERT INTO temperature values(1,40.1)"

# cursorObject.execute(insertValues)


# insertValues = "INSERT INTO temperature values(2,65.4)"


# cursorObject.execute(insertValues)


# Select from the temperature table

queryTable_fall = "SELECT * from fall"
queryResults_fall = cursorObject.execute(queryTable_fall)

queryTable_fall_infos = "SELECT * from fall_infos"
queryResults_fall_infos = cursorObject.execute(queryTable_fall_infos)

queryTable_namen = "SELECT * from namen"
queryResults_namen = cursorObject.execute(queryTable_namen)

queryTable_gesetzbuecher_liste = "SELECT * from gesetzbuecher_liste"
queryResults_gesetzbuecher_liste = cursorObject.execute(queryTable_gesetzbuecher_liste)

queryTable_gesetzbuecher = "SELECT * from gesetzbuecher"
queryResults_gesetzbuecher = cursorObject.execute(queryTable_gesetzbuecher)


# Print the Temperature records

print("(CityId, Temperature)")

for result in queryResults_fall:
    print(result)

for result in queryResults_fall_infos:
    print(result)

for result in queryResults_namen:
    print(result)

for result in queryResults_gesetzbuecher_liste:
    print(result)

for result in queryResults_gesetzbuecher:
    print(result)


connectionObject.close()
