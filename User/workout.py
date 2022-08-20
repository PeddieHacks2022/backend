from flask import Blueprint, request, jsonify

from db.workout import WorkoutModel

model = WorkoutModel()
workout_blueprint = Blueprint('workout_blueprint', __name__)

PREFIX = "/user/<int:user_id>/workout"

@workout_blueprint.route(PREFIX, methods=["POST"])
def post(user_id: int):
    print(request.json)
    name = request.json.get("name", None)
    workout_type = request.json.get("type", None)
    reps = request.json.get("repCount", None)

    if not (name and type(name) == str and workout_type and type(workout_type) == str and reps and type(reps) == int):
        return "Malformed Request", 400

    model.create(user_id, name, workout_type, reps)

    return "Ok", 200

@workout_blueprint.route(PREFIX, methods=["GET"])
def get(user_id: int):
    workouts = model.get_by_user(user_id)
    return jsonify({"workouts": [{"id": workout[0], "name": workout[1], "workoutType": workout[2], "reps": workout[3], "createdDate": workout[4]} for workout in workouts]})

@workout_blueprint.route(f"{PREFIX}/<int:workout_id>", methods=["DELETE"])
def delete(user_id: int, workout_id: int):
    model.delete(workout_id)
    return "Ok", 200
