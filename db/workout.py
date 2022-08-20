
import datetime

from db import connect
from db.utils import generate_id

class WorkoutModel:

    def create(self, user_id: int, workout_type: str, reps: int) -> int:
        id = generate_id()

        conn = connect()
        conn.execute(
            "INSERT INTO workout_template VALUES (:id, :user_id, :workout_type, :reps, :created_date)",
            {"id": id, "user_id": user_id, "workout_type": workout_type, "reps": reps, "created_date": datetime.datetime.now()}
        );
        conn.commit()
        return id

    def get(self, id: int):
        return connect().execute("SELECT * FROM workout_template WHERE id = ?", (id,)).fetchone()
