import sqlite3

database_name = "FitFormV1"

def connect():
    conn = sqlite3.connect(database_name, check_same_thread=False)

    # Ensure tables exist in the database
    try:
        conn.execute("SELECT * FROM USER").fetchone()
    except:
        print("USER table does not exist, creating one")
        conn.execute('''CREATE TABLE USER
(ID INT PRIMARY KEY     NOT NULL,
NAME           TEXT    NOT NULL,
EMAIL          TEXT    NOT NULL,
PASSWORD       TEXT    NOT NULL);''')
        print("Table created")

    return conn

