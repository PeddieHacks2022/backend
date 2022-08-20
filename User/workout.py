from flask import Blueprint, request

from db.workout import WorkoutModel

model = WorkoutModel()
workout_blueprint = Blueprint('workout_blueprint', __name__)

@workout_blueprint.route('/', methods=["POST"])
def post():

    # get user id from request
    user_id = "1"

    workout_type = request.json.get("workout_type", None)
    reps = request.json.get("reps", None)

    if not (workout_type and type(workout_type) == str and reps and type(reps) == int):
        return "Malformed Request", 400

    # model.create(user_id, workout_type, reps)

    return "Ok", 200

@workout_blueprint.route('/', methods=["GET"])
def get():
    return "", 400
