import sqlite3

database_name = "FitFormV2"

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
        )
    ''')

    print("Migrating workout_template table...")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS workout_template (
            id INT PRIMARY KEY     NOT NULL,
            user_id        INT     NOT NULL,
            name           TEXT    NOT NULL,
            workout_type   TEXT    NOT NULL,
            reps           INT     NOT NULL,
            created_date   TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')

    print("Migrating workout_set table...")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS workout_set (
            id INT PRIMARY KEY     NOT NULL,
            user_id        INT     NOT NULL,
            name           TEXT    NOT NULL,
            created_date   TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id)
        )
    ''')

    print("Migrating workout_set_to_workout_template table...")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS workout_set_to_workout_template (
            id INT PRIMARY KEY             NOT NULL,
            workout_template_id     INT    NOT NULL,
            workout_set_id          INT    NOT NULL,
            ind                     INT    NOT NULL,
            created_date            TEXT   NOT NULL,
            FOREIGN KEY (workout_template_id) REFERENCES workout_template (id),
            FOREIGN KEY (workout_set_id) REFERENCES workout_set (id)
        )
    ''')


def purge():
    conn = connect()

    conn.execute("DROP TABLE IF EXISTS user")
    conn.execute("DROP TABLE IF EXISTS workout_template")
    conn.execute("DROP TABLE IF EXISTS workout_set")
    conn.execute("DROP TABLE IF EXISTS workout_set_to_workout_template")

