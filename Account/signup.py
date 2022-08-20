from flask import Blueprint, request
from flask_bcrypt import generate_password_hash
signup_blueprint = Blueprint('signup_blueprint', __name__)

@signup_blueprint.route('/signup', methods=["POST"])
def signup():
    # get relevant information
    email = request.json.get("email", None)
    name = request.json.get("name", None)

    # hash + salt the password before accessing
    password = generate_password_hash(request.json.get("password", None), 10).decode("utf-8")

    # TODO: implement
    print(email, name, password)
    return "Unable to Process", 500