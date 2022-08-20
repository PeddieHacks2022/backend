# Imports
import sqlite3
import random
from typing import List

# Setup database connection
conn = None

def connectToDatabase(databaseName: str) -> None:
    # Establish connection
    global conn
    conn = sqlite3.connect(databaseName, check_same_thread=False)

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

    return

class AccountDAO:
    def getUserByEmail(self, email: str) -> List[str]:
        resultSet = conn.execute(f"SELECT * FROM USER WHERE EMAIL = '{email}';").fetchone()
        return resultSet

    def getUserByID(self, id: int) -> List[str]:
        resultSet = conn.execute(f"SELECT * FROM USER WHERE ID = {id};").fetchone()
        return resultSet

    def createUser(self, name: str, email: str, password: str) -> int:
        id = random.randint(1, 100000000)
        while (self.getUserByID(id)):
            print("ID conflict, trying again")
            id = random.randint(1, 100000000)

        command = f"INSERT INTO USER (ID,NAME,EMAIL,PASSWORD) VALUES ({id}, '{name}', '{email}', '{password}')"
        conn.execute(command);
        conn.commit()
        return id
