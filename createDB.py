import sqlite3 as sql

con = sql.connect("database.db")
cursor = con.cursor()
#cursor.execute("DROP TABLE IF EXISTS cart")
sql ="""
        CREATE TABLE IF NOT EXISTS cart(
        pid INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        quantity INTEGER,
        total REAL 
        )
"""
cursor.execute(sql)
con.commit()
print("Table Created Successfully")
con.close()