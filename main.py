from flask import Flask

import db
from Account.signup import signup_blueprint
from Account.signin import signin_blueprint
from User.workout import workout_blueprint

def intializeBackend():

    # Connect flask and appropriate blueprints
    app = Flask(__name__)
    app.register_blueprint(signup_blueprint)
    app.register_blueprint(signin_blueprint)
    app.register_blueprint(workout_blueprint, url_prefix='/workout/<int:workout_id>')
    app.run()

if __name__ == "__main__":
    app = intializeBackend()

