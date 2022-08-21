import time
from exercise.util import bone, angle

UP_THRESHOLD = 85
DOWN_THRESHOLD = 140
ANGLE_PROGRESSIONS = 5
MAX_PROG = (DOWN_THRESHOLD - UP_THRESHOLD)/ANGLE_PROGRESSIONS

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
    
    progressLeft  = max(0, min(MAX_PROG, (left_angle - UP_THRESHOLD)//ANGLE_PROGRESSIONS)) + 1
    progressRight = max(0, min(MAX_PROG, (right_angle - UP_THRESHOLD)//ANGLE_PROGRESSIONS)) + 1
    if session.rep_state == "up":
        progressLeft =  (MAX_PROG + 2) - progressLeft
        progressRight = (MAX_PROG + 2) - progressRight
    
    # Check for syncing (max 1 offset)
    if abs(progressLeft - progressRight) > 1:
        if time.time() - session.lastWarned > 2:
            session.lastWarned = time.time()
            return "Keep your hands alligned"
        return

    # Consider lower progress for overall progress
    progress = min(progressLeft, progressRight)
    if progress < session.rep_progress:
        session.rep_progress = progress
        
        if time.time() - session.lastWarned > 2:
            session.lastWarned = time.time()
            stateFlips = {"up":"down", "down":"up"}
            return "Keep going " + stateFlips[session.rep_state]
    
    session.rep_progress = progress
    return

#if __name__ == "__main__":
#    print(process_curl(data.POSE))
