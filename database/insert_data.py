import sqlite3
# Insert EOD stats into the reports table

connectionObject = sqlite3.connect("../db/test.db")
cursorObject = connectionObject.cursor()

insertValues = "INSERT INTO temperature values(1,40.1)"

cursorObject.execute(insertValues)


insertValues = "INSERT INTO temperature values(2,65.4)"

# cursorObject.execute(insertValues)
