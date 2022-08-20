from typing import List
import random

from . import connect

class AccountModel:

    def getUserByEmail(self, email: str) -> List[str]:
        resultSet = connect().execute(f"SELECT * FROM USER WHERE EMAIL = '{email}';").fetchone()
        return resultSet

    def getUserByID(self, id: int) -> List[str]:
        resultSet = connect().execute(f"SELECT * FROM USER WHERE ID = {id};").fetchone()
        return resultSet

    def createUser(self, name: str, email: str, password: str) -> int:
        id = random.randint(1, 100000000)
        while (self.getUserByID(id)):
            print("ID conflict, trying again")
            id = random.randint(1, 100000000)

        conn = connect()
        command = f"INSERT INTO USER (ID,NAME,EMAIL,PASSWORD) VALUES ({id}, '{name}', '{email}', '{password}')"
        conn.execute(command);
        conn.commit()
        return id
