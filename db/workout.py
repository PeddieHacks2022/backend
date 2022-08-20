
import datetime

from db import connect
from db.utils import generate_id

class WorkoutModel:

    def create(self, user_id: int, name: str, workout_type: str, reps: int) -> int:
        id = generate_id()

        conn = connect()
        conn.execute(
            "INSERT INTO workout_template VALUES (:id, :user_id, :name, :workout_type, :reps, :created_date)",
            {"id": id, "user_id": user_id, "name": name, "workout_type": workout_type, "reps": reps, "created_date": datetime.datetime.now()}
        );
        conn.commit()
        return id

    def get_by_id(self, workout_id: int):
        return connect().execute("SELECT * FROM workout_template WHERE id = ?", (workout_id,)).fetchone()

    def get_by_user(self, user_id: int):
        return connect().execute("""
            SELECT workout_template.id, workout_template.name, workout_type, reps, created_date
            FROM user INNER JOIN workout_template ON user.id = workout_template.user_id WHERE user.id = ?
        """, (user_id,)).fetchall()

    def delete(self, id: int):
        return connect().execute("DELETE FROM workout_template WHERE id = ?", (id,))

