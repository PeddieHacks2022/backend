import data
import numpy as np

def angle(a, b):
    return np.degrees(np.arccos(np.dot(a, b)/ (np.linalg.norm(a) * np.linalg.norm(b))))

def preprocess(points):
    def bone(start, end):
        return np.array(points[end]) - np.array(points[start])

    left_shoulder_to_left_arm = bone("left_shoulder_1_joint", "left_arm_joint")
    left_arm_to_left_forearm = bone("left_arm_joint", "left_forearm_joint")

    right_shoulder_to_right_arm = bone("right_shoulder_1_joint", "right_arm_joint")
    right_arm_to_right_forearm = bone("right_arm_joint", "right_forearm_joint")

    print(angle(left_shoulder_to_left_arm, left_arm_to_left_forearm))

if __name__ == "__main__":
    preprocess(data.T_POSE)
