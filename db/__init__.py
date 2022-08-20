import sqlite3

database_name = "FitFormV1"

def connect():
    return sqlite3.connect(database_name, check_same_thread=False)

def migrate():
    conn = connect()

    print("Migrating user table...")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INT PRIMARY KEY     NOT NULL,
            name           TEXT    NOT NULL,
            email          TEXT    NOT NULL,
            password       TEXT    NOT NULL
        );
    ''')

    print("Migrating workout_template table...")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS workout_template (
            id INT PRIMARY KEY     NOT NULL,
            user_id        INT     NOT NULL,
            workout_type   TEXT    NOT NULL,
            reps           INT     NOT NULL,
            created_date   TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        );
    ''')

def purge():
    conn = connect()

    conn.execute("DROP TABLE user, workout_template")
