# Imports
import DAOs
from flask import Flask
from Account.signup import signup_blueprint
from Account.signin import signin_blueprint

def intializeBackend():
    # Connect database 
    DAOs.connectToDatabase("FitFormV1")

    # Connect flask and appropriate blueprints
    app = Flask(__name__)
    app.register_blueprint(signup_blueprint)
    app.register_blueprint(signin_blueprint)
    app.run()

if __name__ == "__main__":
    intializeBackend()