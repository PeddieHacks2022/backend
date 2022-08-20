from flask import Blueprint, request
from flask_bcrypt import generate_password_hash
from DAOs import AccountDAO
accountDAO = AccountDAO()

signin_blueprint = Blueprint('signin_blueprint', __name__)

@signin_blueprint.route('/signin', methods=["POST"])
def signin():
    # Get relevant information
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Verify json body is sent
    if not (email and type(email) == str and password and type(password) == str):
        return "Malformed Request", 400
    
    account = accountDAO.getUserByEmail(email)
    if not account: # Verify if account exists
        return "Email does not exist", 404

    return {"ID": account[0]}