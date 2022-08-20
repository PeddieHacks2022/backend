# Imports
import DAOs
import socket
import threading
import json
from flask import Flask
from Account.signup import signup_blueprint
from Account.signin import signin_blueprint

socket_server = None
def intializeBackend():
    # Connect database 
    DAOs.connectToDatabase("FitFormV1")

    # Initiate socket stream
    global socket_server
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    socket_server.bind(("192.168.2.100", 8001))

    # Connect flask and appropriate blueprints
    app = Flask(__name__)
    app.register_blueprint(signup_blueprint)
    app.register_blueprint(signin_blueprint)
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
    app.run(host="192.168.2.100", port=8000)
