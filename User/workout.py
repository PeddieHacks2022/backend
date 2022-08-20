from flask import Blueprint, request, jsonify

from db.workout import WorkoutModel

model = WorkoutModel()
workout_blueprint = Blueprint('workout_blueprint', __name__)

PREFIX = "/user/<int:user_id>/workout"

@workout_blueprint.route(PREFIX, methods=["POST"])
def post(user_id: int):

    workout_type = request.json.get("workout_type", None)
    reps = request.json.get("reps", None)

    if not (workout_type and type(workout_type) == str and reps and type(reps) == int):
        return "Malformed Request", 400

    model.create(user_id, workout_type, reps)

    return "Ok", 200

@workout_blueprint.route(f"{PREFIX}/<int:workout_id>", methods=["GET"])
def get(user_id: int, workout_id: int):
    workout = model.get(workout_id)
    return jsonify(workout)

@workout_blueprint.route(f"{PREFIX}/<int:workout_id>", methods=["DELETE"])
def delete(user_id: int, workout_id: int):
    model.delete(workout_id)
    return "Ok", 200
