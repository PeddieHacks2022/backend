import socket
import threading
import json
import UDPHandler
from flask import Flask
from dotenv import load_dotenv
import os

from db import migrate
from graphing.upload_images import graphing_blueprint
from Account.signup import signup_blueprint
from Account.signin import signin_blueprint
from UDPHandler import updupdate_blueprint
from User.workout import workout_blueprint
from User.workout_set import routine_blueprint
from db.statistics import init as statInit

load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
HTTP_PORT = int(os.getenv("HTTP_PORT"))
SOCKET_PORT = int(os.getenv("SOCKET_PORT"))

socket_server = None
def intializeBackend():
    # initialize database
    migrate()

    # Initiate socket stream
    global socket_server
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    socket_server.bind((SERVER_IP, SOCKET_PORT))

    # Connect flask and appropriate blueprints
    app = Flask(__name__)
    app.register_blueprint(signup_blueprint)
    app.register_blueprint(graphing_blueprint)
    app.register_blueprint(signin_blueprint)
    app.register_blueprint(workout_blueprint)
    app.register_blueprint(updupdate_blueprint)
    app.register_blueprint(routine_blueprint)
    return app

def streamListener():
    global socket_server

    while True:
        #print ("Waiting for client...")
        bytesData, addr = socket_server.recvfrom(1024*16)
        data = bytesData.decode('utf-8')
        
        try: # in case its a json table
            data = json.loads(data)
        except:
            pass

        UDPHandler.process(addr, data)

if __name__ == "__main__":
    app = intializeBackend()
    #statInit()
    t1 = threading.Thread(target=streamListener)
    t1.daemon = True
    t1.start()
    app.run(host=SERVER_IP, port=HTTP_PORT)
    
