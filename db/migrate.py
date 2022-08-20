
from . import connect

def migrate():
    conn = connect()

    print("Creating user table")
    conn.execute('''CREATE TABLE USER
(ID INT PRIMARY KEY     NOT NULL,
NAME           TEXT    NOT NULL,
EMAIL          TEXT    NOT NULL,
PASSWORD       TEXT    NOT NULL);''')

