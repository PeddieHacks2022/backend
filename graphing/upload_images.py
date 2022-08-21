from flask import Blueprint, request, send_file

graphing_blueprint = Blueprint('graphing_blueprint', __name__)

@graphing_blueprint.route("/graph/time", methods=["GET"])
def getTimeGraph():
    #img_dir = "./static"
    #img_list = os.listdir(img_dir)
    #img_path = os.path.join(img_dir, random.choice(img_list))
    return