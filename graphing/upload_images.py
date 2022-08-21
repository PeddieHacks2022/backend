from flask import Blueprint, request, send_file
import os

graphing_blueprint = Blueprint('graphing_blueprint', __name__)

@graphing_blueprint.route("/graph/time", methods=["GET"])
def getTimeGraph():
    img_path = "D:\\Coding\\PeddieHacks2022\\backend\\graphing\\graphs\\time_graph.png" #os.path.join(os.getcwd(), "/graphs/time_graph.png")
    return send_file(img_path, mimetype='image/png')

@graphing_blueprint.route("/graph/reps", methods=["GET"])
def getRepsGraph():
    img_path = "D:\\Coding\\PeddieHacks2022\\backend\\graphing\\graphs\\reps_graph.png" #os.path.join(os.getcwd(), "/graphs/time_graph.png")
    return send_file(img_path, mimetype='image/png')