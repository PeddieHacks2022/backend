
import datetime

from . import connect
from db.utils import generate_id

class WorkoutModel:

    def create(self, user_id: int, workout_type: str, reps: int) -> int:
        id = generate_id()

        conn = connect()
        conn.execture(
            "INSERT INTO workout_template VALUES (:id, :user_id, :workout_type, :reps, :created_date)",
            {"id": id, "user_id": user_id, "workout_type": workout_type, "reps": reps, "created_date": datetime.datetime.now()}
        );
        conn.commit()
        return id
