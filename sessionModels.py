from exercise.util import bone, angle
import time

class workoutSession:
    def __init__(self, max_reps, routine_data, routine_counter):
        self.max_reps = max_reps
        self.routine_data = routine_data
        self.routine_counter = routine_counter

    time_started =  time.time()
    lastWarned = time.time()
    lastPolled = 0
    reps = 0

    jointTotals = None
    totalToAverage = 1

class curlSession(workoutSession):
    def __init__(self, max_reps, routine_data, routine_counter, 
        rightEnabled, leftEnabled, overheadEnabled):
        super().__init__(max_reps, routine_data, routine_counter)
        self.rightEnabled = rightEnabled
        self.leftEnabled = leftEnabled
        self.overheadEnabled = overheadEnabled

    rep_state = None
    rep_progress = 0

    UP_THRESHOLD = 80
    DOWN_THRESHOLD = 135
    ANGLE_PROGRESSIONS = 5
    MAX_PROG = (DOWN_THRESHOLD - UP_THRESHOLD)/ANGLE_PROGRESSIONS

    def process_poll(self, points) -> str:
        left_forearm_to_left_arm = bone(points, "left_arm_joint", "left_forearm_joint")
        left_forearm_to_left_hand = bone(points, "left_hand_joint", "left_forearm_joint")

        right_forearm_to_right_arm = bone(points, "right_arm_joint", "right_forearm_joint")
        right_forearm_to_right_hand = bone(points, "right_hand_joint", "right_forearm_joint")

        left_angle = angle(left_forearm_to_left_arm, left_forearm_to_left_hand)
        right_angle = angle(right_forearm_to_right_arm, right_forearm_to_right_hand)

        if not self.rightEnabled:
            right_angle = left_angle
        elif not self.leftEnabled:
            left_angle = right_angle

        state = None
        if (left_angle < self.UP_THRESHOLD and right_angle < self.UP_THRESHOLD):
            state = "up"
        if (left_angle > self.DOWN_THRESHOLD and right_angle > self.DOWN_THRESHOLD):
            state = "down"
        if (self.overheadEnabled):
            state = state == "up" and "down" or "up"

        if not self.rep_state:
            # intialize repstate
            self.rep_state = state or "down"
            return 
        
        if state:
            if self.rep_state != state:
                if state == "up":
                    self.reps += 1
                self.rep_state = state
                self.rep_progress = 0

                if self.max_reps == self.reps:
                    self.routine_counter += 1
                    if self.routine_counter >= len(self.routine_data):
                        return "complete"
                    return "next routine"

                return "new state"
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


def makeSession(mode: str, max_reps, routine_data, routine_counter) -> workoutSession:
    if mode.find("Bicep") > -1 or mode.find("Overhead") > -1:
        session = curlSession(max_reps, routine_data, routine_counter, mode.find("Right") > -1, mode.find("Left") > -1, mode.find("Overhead") > -1)
        return session

    else:
        print("NOT BICEPS")
        