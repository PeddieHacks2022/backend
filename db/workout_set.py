
import datetime

from db import connect
from db.utils import generate_id

class WorkoutSetModel:

    def create(self, user_id: int, name: str) -> int:
        id = generate_id()

        conn = connect()
        conn.execute(
            "INSERT INTO workout_set VALUES (:id, :user_id, :name, :created_date)",
            {"id": id, "user_id": user_id, "name": name, "created_date": datetime.datetime.now()}
        );
        conn.commit()
        return id

    def insert_link(self, workout_set_id: int, workout_template_id: int, index: int) -> int:
        id = generate_id()

        conn = connect()
        conn.execute(
            "INSERT INTO workout_set_to_workout_template VALUES (:id, :workout_template_id, :workout_set_id, :ind, :created_date)",
            {"id": id, "workout_template_id": workout_template_id, "workout_set_id": workout_set_id, "ind": index, "created_date": datetime.datetime.now()}
        );
        conn.commit()
        return id

    def get_all_workouts(self, user_id: int):

        # get all workout routines
        conn = connect()

        routines = conn.execute("""
            SELECT id, name
            FROM workout_set
            WHERE user_id = ?
        """, (user_id,)).fetchall()

        output_routines = []

        for routine in routines:
            routine_id = routine[0]
            routine_name = routine[1]

            print("routine_id", routine_id)

            workouts = connect().execute("""
                SELECT workout_template.id, workout_template.name, workout_type, reps, workout_template.created_date
                FROM workout_set_to_workout_template INNER JOIN workout_template
                ON workout_set_to_workout_template.workout_template_id = workout_template.id
                WHERE workout_template.user_id == ? AND workout_set_to_workout_template.workout_set_id = ?
                ORDER BY workout_set_to_workout_template.ind ASC
            """, (user_id, routine_id,)).fetchall()
            workout_json = [{"id": workout[0], "name": workout[1], "workoutType": workout[2], "reps": workout[3], "createdDate": workout[4]} for workout in workouts]
            routine_json = {"id": routine_id, "name": routine_name, "workouts": workout_json}

            output_routines.append(routine_json)

        return output_routines

    def get_workouts_of_routine(self, workout_set_id: int):
        # get all workout routines
        conn = connect()

        workouts = conn.execute("""
            SELECT workout_template.id, workout_template.name, workout_type, reps, workout_template.created_date
            FROM workout_set_to_workout_template INNER JOIN workout_template
            ON workout_set_to_workout_template.workout_template_id = workout_template.id
            WHERE workout_set_to_workout_template.workout_set_id = ?
            ORDER BY workout_set_to_workout_template.ind ASC
        """, (workout_set_id,)).fetchall()
        workout_json = [{"id": workout[0], "name": workout[1], "workoutType": workout[2], "reps": workout[3], "createdDate": workout[4]} for workout in workouts]

        return workout_json
