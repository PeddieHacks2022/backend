from flask import Blueprint, request
from flask_bcrypt import generate_password_hash
from DAOs import AccountDAO
accountDAO = AccountDAO()

signup_blueprint = Blueprint('signup_blueprint', __name__)

@signup_blueprint.route('/signup', methods=["POST"])
def signup():
    # Get relevant information
    email = request.json.get("email", None)
    name = request.json.get("name", None)
    password = request.json.get("password", None)

    # Verify json body is sent
    if not (email and type(email) == str and name and type(name) == str and password and type(password) == str):
        return "Malformed Request", 400

    # Verify if email already exists
    if accountDAO.getUserByEmail(email):
        return "Email already registered", 403

    # hash + salt the password
    password = generate_password_hash(password, 10).decode("utf-8")

    # Register user
    id = accountDAO.createUser(name, email, password)
    return {"ID": id}