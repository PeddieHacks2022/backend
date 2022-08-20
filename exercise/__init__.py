from exercise.curl import process_curl
from exercise.jumping_jack import process_jumping_jack

def process(mode, session, joint_points):
    if (mode == "curl"):
        return process_curl(session, joint_points)
    if (mode == "jumping_jack"):
        return process_jumping_jack(session, joint_points)


