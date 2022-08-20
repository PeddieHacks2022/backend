import numpy as np

import exercise.data
from exercise.util import bone, angle

UP_THRESHOLD = 85
DOWN_THRESHOLD = 140

def process_curl(points):

    left_shoulder_to_left_arm = bone(points, "left_arm_joint", "left_forearm_joint")
    left_arm_to_left_forearm = bone(points, "left_hand_joint", "left_forearm_joint")

    right_shoulder_to_right_arm = bone(points, "right_arm_joint", "right_forearm_joint")
    right_arm_to_right_forearm = bone(points, "right_hand_joint", "right_forearm_joint")

    left_angle = angle(left_shoulder_to_left_arm, left_arm_to_left_forearm)
    right_angle = angle(right_shoulder_to_right_arm, right_arm_to_right_forearm)

    #print(left_angle, right_angle)
    if (left_angle < UP_THRESHOLD and right_angle < UP_THRESHOLD):
        return "up"
    if (left_angle > DOWN_THRESHOLD and right_angle > DOWN_THRESHOLD):
        return "down"

    return "none"

#if __name__ == "__main__":
#    print(process(data.POSE))
