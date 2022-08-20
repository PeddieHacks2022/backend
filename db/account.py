from typing import List

from . import connect
from db.utils import generate_id

class AccountModel:

    def getUserByEmail(self, email: str) -> List[str]:
        resultSet = connect().execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
        return resultSet

    def getUserByID(self, id: int) -> List[str]:
        resultSet = connect().execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
        return resultSet

    def createUser(self, name: str, email: str, password: str) -> int:
        id = generate_id()

        conn = connect()
        conn.execute(
            "INSERT INTO user VALUES (:id, :name, :email, :password)",
            {"id": id, "name": name, "email": email, "password": password}
        );
        conn.commit()
        return id
