from exercise.util import bone, angle
import time

class workoutSession:
    time_started =  time.time()
    lastWarned = time.time()
    lastPolled = 0
    reps = 0

    jointTotals = None
    totalToAverage = 1

class curlSession(workoutSession):
    rep_state = "down"
    rep_progress = 0

    UP_THRESHOLD = 80
    DOWN_THRESHOLD = 145
    ANGLE_PROGRESSIONS = 5
    MAX_PROG = (DOWN_THRESHOLD - UP_THRESHOLD)/ANGLE_PROGRESSIONS

    def process_poll(self, points) -> str:
        left_forearm_to_left_arm = bone(points, "left_arm_joint", "left_forearm_joint")
        left_forearm_to_left_hand = bone(points, "left_hand_joint", "left_forearm_joint")

        right_forearm_to_right_arm = bone(points, "right_arm_joint", "right_forearm_joint")
        right_forearm_to_right_hand = bone(points, "right_hand_joint", "right_forearm_joint")

        left_angle = angle(left_forearm_to_left_arm, left_forearm_to_left_hand)
        right_angle = angle(right_forearm_to_right_arm, right_forearm_to_right_hand)

        state = None
        if (left_angle < self.UP_THRESHOLD and right_angle < self.UP_THRESHOLD):
            state = "up"
        if (left_angle > self.DOWN_THRESHOLD and right_angle > self.DOWN_THRESHOLD):
            state = "down"

        if state:
            if self.rep_state != state:
                self.reps += 1
                self.rep_state = state
                self.rep_progress = 0
                return "New state"
            return None # No progress
        
        progressLeft  = max(0, min(self.MAX_PROG, (left_angle - self.UP_THRESHOLD)//self.ANGLE_PROGRESSIONS)) + 1
        progressRight = max(0, min(self.MAX_PROG, (right_angle - self.UP_THRESHOLD)//self.ANGLE_PROGRESSIONS)) + 1
        if self.rep_state == "down":
            progressLeft =  (self.MAX_PROG + 2) - progressLeft
            progressRight = (self.MAX_PROG + 2) - progressRight
        
        # Check for syncing (max 2 offset)
        if abs(progressLeft - progressRight) > 2:
            if time.time() - self.lastWarned > 2:
                self.lastWarned = time.time()
                return "Keep your hands aligned"
            return

        # Consider lower progress for overall progress
        progress = min(progressLeft, progressRight)
        if progress < self.rep_progress - 1:
            self.rep_progress = progress
            
            if time.time() - self.lastWarned > 2:
                self.lastWarned = time.time()
                return self.rep_state == "down" and "finish your rep" or "go all the way down"

        elif progress > self.rep_progress:
            self.rep_progress = progress
        return


def makeSession(mode: str) -> workoutSession:
    if mode == "curl":
        return curlSession()
        