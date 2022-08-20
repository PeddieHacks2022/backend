import data
import numpy as np

UP_THRESHOLD = 10
DOWN_THRESHOLD = 160

def angle(a, b):
    return np.degrees(np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))))

def process(points):
    def bone(start, end):
        return np.array(points[end]) - np.array(points[start])

    left_shoulder_to_left_arm = bone("left_arm_joint", "left_shoulder_1_joint")
    left_arm_to_left_forearm = bone("left_arm_joint", "left_forearm_joint")

    right_shoulder_to_right_arm = bone("right_arm_joint", "right_shoulder_1_joint")
    right_arm_to_right_forearm = bone("right_arm_joint", "right_forearm_joint")

    left_angle = angle(left_shoulder_to_left_arm, left_arm_to_left_forearm)
    right_angle = angle(right_shoulder_to_right_arm, right_arm_to_right_forearm)

    if (left_angle < UP_THRESHOLD and right_angle < UP_THRESHOLD):
        return "up"
    if (left_angle > DOWN_THRESHOLD and right_angle > DOWN_THRESHOLD):
        return "down"

    return "none"

if __name__ == "__main__":
    print(process(data.POSE))
