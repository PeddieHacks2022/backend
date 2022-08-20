
import datetime

from db import connect
from db.utils import generate_id

class WorkoutSetModel:

    def create(self, user_id: int, name: string) -> int:
        id = generate_id()

        conn = connect()
        conn.execute(
            "INSERT INTO workout_set VALUES (:id, :user_id, :name, :created_date)",
            {"id": id, "user_id": user_id, "name": name, "created_date": datetime.datetime.now()}
        );
        conn.commit()
        return id

    def insert_link(self, workout_set_id: int, workout_template_id: int) -> int:
        id = generate_id()

        conn = connect()
        conn.execute(
            "INSERT INTO workout_set_to_workout_template VALUES (:id, :workout_template_id, :workout_set_id)",
            {"id": id, "workout_template_id": workout_template_id, "workout_set_id": workout_set_id, "created_date": datetime.datetime.now()}
        );
        conn.commit()
        return id

    def get_workouts(self, workout_set_id: int):

        pass
        # conn = connect()
        # conn.execute("""
        #     SELECT * FROM workout_set_to_workout_template INNER JOIN ON workout_template
        #     WHERE workout_set_to_workout_template.
        # """)
