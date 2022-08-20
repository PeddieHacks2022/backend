
import numpy as np

import data
from util import bone, angle

LEG_UP_THRESHOLD = 45
LEG_DOWN_THRESHOLD = 10

ARM_UP_THRESHOLD = 130
ARM_DOWN_THRESHOLD = 20

def process_jumping_jack(points):

    left_upLeg_to_left_leg = bone(points, "left_upLeg_joint", "left_leg_joint")
    right_upLeg_to_right_leg = bone(points, "right_upLeg_joint", "right_leg_joint")

    spine_7_to_spine_1 = bone(points, "spine_7_joint", "spine_1_joint")
    left_shoulder_to_left_arm = bone(points, "left_arm_joint", "left_shoulder_1_joint")
    right_shoulder_to_right_arm = bone(points, "right_arm_joint", "right_shoulder_1_joint")

    leg_angle = bone(points, left_upLeg_to_left_leg, right_upLeg_to_right_leg)
    left_arm_angle = bone(points, left_shoulder_to_left_arm, spine_7_to_spine_1)
    right_arm_angle = bone(points, right_shoulder_to_right_arm, spine_7_to_spine_1)

    if (leg_angle > LEG_UP_THRESHOLD and left_arm_angle > ARM_UP_THRESHOLD and right_arm_angle > ARM_UP_THRESHOLD):
        return "up"
    if (leg_angle < LEG_DOWN_THRESHOLD and left_arm_angle < ARM_DOWN_THRESHOLD and right_arm_angle < ARM_DOWN_THRESHOLD):
        return "down"

    return "none"
