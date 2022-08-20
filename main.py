# Imports
import DAOs
from flask import Flask
from Account.signup import signup_blueprint

def intializeBackend():
    # Connect database 
    DAOs.connectToDatabase("FitFormV1")

    # Connect flask
    app = Flask(__name__)
    app.register_blueprint(signup_blueprint)
    app.run()

if __name__ == "__main__":
    app = intializeBackend()

