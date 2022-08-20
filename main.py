from flask import Flask
from Account.signup import signup_blueprint

def intializeBackend():
    app = Flask(__name__)
    app.register_blueprint(signup_blueprint)
    return app

if __name__ == "__main__":
    app = intializeBackend()
    app.run()