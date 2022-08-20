import sqlite3

database_name = "FitFormV2"

def connect():
    return sqlite3.connect(database_name, check_same_thread=False)

def migrate():
    conn = connect()

    print("Creating user table")
    conn.execute('''CREATE TABLE IF NOT EXISTS USER
(ID INT PRIMARY KEY     NOT NULL,
NAME           TEXT    NOT NULL,
EMAIL          TEXT    NOT NULL,
PASSWORD       TEXT    NOT NULL);''')

