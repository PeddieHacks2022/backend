# Imports
import sqlite3

# Setup database connection
conn = None
def connectToDatabase(databaseName: str) -> None:
    global conn
    conn = sqlite3.connect(databaseName)
    return

class UserDAO:
    def emailExists(self, email: str) -> bool:
        # TODO: implement
        return False