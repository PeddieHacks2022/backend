import socket
import threading
import json
from flask import Flask
from dotenv import load_dotenv
import os

from Account.signup import signup_blueprint
from Account.signin import signin_blueprint
from User.workout import workout_blueprint

load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
HTTP_PORT = int(os.getenv("HTTP_PORT"))
SOCKET_PORT = int(os.getenv("SOCKET_PORT"))

socket_server = None
def intializeBackend():

    # Initiate socket stream
    global socket_server
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    socket_server.bind((SERVER_IP, SOCKET_PORT))

    # Connect flask and appropriate blueprints
    app = Flask(__name__)
    app.register_blueprint(signup_blueprint)
    app.register_blueprint(signin_blueprint)
    app.register_blueprint(workout_blueprint)
    return app

def streamListener():
    global socket_server

    while True:
        print ("Waiting for client...")
        bytesData, addr = socket_server.recvfrom(1024*16)
        data = json.loads(bytesData.decode('utf-8'))
        print("Received Messages:", data, " from", addr)

if __name__ == "__main__":
    app = intializeBackend()
    t1 = threading.Thread(target=streamListener)
    t1.daemon = True
    t1.start()
    app.run(host=SERVER_IP, port=HTTP_PORT)
    
