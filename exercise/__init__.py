
import data

from curl import process_curl
from jumping_jack import process_jumping_jack

def process(mode, points):
    if (mode == "curl"):
        return process_curl(points)
    if (mode == "jumping_jack"):
        return process_jumping_jack(points)

if __name__ == "__main__":
    print(process("curl", data.POSE))
