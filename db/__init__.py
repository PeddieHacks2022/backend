import sqlite3

database_name = "FitFormV1"

def connect():
    return sqlite3.connect(database_name, check_same_thread=False)

