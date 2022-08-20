from exercise.util import bone, angle

UP_THRESHOLD = 85
DOWN_THRESHOLD = 140

def process_curl(session, points):

    left_forearm_to_left_arm = bone(points, "left_arm_joint", "left_forearm_joint")
    left_forearm_to_left_hand = bone(points, "left_hand_joint", "left_forearm_joint")

    right_forearm_to_right_arm = bone(points, "right_arm_joint", "right_forearm_joint")
    right_forearm_to_right_hand = bone(points, "right_hand_joint", "right_forearm_joint")

    left_angle = angle(left_forearm_to_left_arm, left_forearm_to_left_hand)
    right_angle = angle(right_forearm_to_right_arm, right_forearm_to_right_hand)

    state = None
    if (left_angle < UP_THRESHOLD and right_angle < UP_THRESHOLD):
        state = "up"
    if (left_angle > DOWN_THRESHOLD and right_angle > DOWN_THRESHOLD):
        state = "down"

    if state:
        if session.rep_state != state:
            session.reps += 1
            session.rep_state = state
            session.rep_progress = 0
            return "New state"
        return None # No progress
    
    progress = (angle - UP_THRESHOLD)//5 + 1
    if session.rep_state == "up":
        max_progress = (DOWN_THRESHOLD - UP_THRESHOLD)//5 + 2
        progress = max_progress - progress
    
    if progress < session.rep_progress:
        session.rep_progress = progress
        stateFlips = {"up":"down", "down":"up"}
        return "Keep going " + stateFlips[session.rep_state]
    
    session.rep_progress = progress
    return None

#if __name__ == "__main__":
#    print(process_curl(data.POSE))
