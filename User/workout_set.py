from flask import Blueprint, request, jsonify

from db.workout_set import WorkoutSetModel

model = WorkoutSetModel()
routine_blueprint = Blueprint('routine_blueprint', __name__)

PREFIX = "/user/<int:user_id>/routine"

@routine_blueprint.route(PREFIX, methods=["POST"])
def post(user_id: int):

    name = request.json.get("name", None)

    if not (name and type(name) == str):
        return "Malformed Request", 400

    model.create(user_id, name)

    return "Ok", 200

@routine_blueprint.route(f"{PREFIX}/<int:routine_id>", methods=["PATCH"])
def patch(user_id: int, routine_id: int):

    workout_id = request.json.get("workout_id", None)

    if not (workout_id and type(workout_id) == int):
        return "Malformed Request", 400

    # TODO verify workout_id is valid
    model.insert_link(routine_id, workout_id)

    return "Ok", 200

@routine_blueprint.route(PREFIX, methods=["GET"])
def get(user_id: int):
    routines = model.get_all_workouts(user_id)
    return jsonify(routines)
