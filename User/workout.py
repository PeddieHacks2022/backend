from flask import Blueprint, request

workout_blueprint = Blueprint('workout_blueprint', __name__)

@workout_blueprint.route('/', methods=["POST"])
def post():
    return "", 400

@workout_blueprint.route('/', methods=["GET"])
def get():
    return "", 400
