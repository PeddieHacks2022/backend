# imports
import time
from sessionModels import makeSession
from db.workout import WorkoutModel #, get_by_id as getWorkoutById
from db.workout_set import WorkoutSetModel
from flask import Blueprint, request
updupdate_blueprint = Blueprint('updupdate_blueprint', __name__)

# data storage
temporaryData = {}
dataMapping = {}
workoutModel = WorkoutModel()
workoutSetModel = WorkoutSetModel()

# Processing UDP updates 
def process(address, data):
    #print("Processing", data, " from", address)
    #print(data)
    if type(data) == str:
        userID, isRoutine, workoutOrRoutineID = [int(e) for e in data.split(" ")]
        print("GOT FIRST: ", userID, isRoutine, workoutOrRoutineID)

        if isRoutine:
            routine_data = workoutSetModel.get_workouts_of_routine(workoutOrRoutineID)
            mode = routine_data[0]["workoutType"]
            maxReps = routine_data[0]["reps"]
            print("Routine of length", len(routine_data))

        else:
            routine_data = []
            workout_specs = workoutModel.get_by_id(workoutOrRoutineID)
            mode = workout_specs[3]
            maxReps = workout_specs[4]

        # Add new user 
        session = makeSession(mode, maxReps, routine_data, 0)
        temporaryData[address[0]] = session
        dataMapping[userID] = address[0]
        return
    
    # Process table update
    try:
        session = temporaryData[address[0]]
        
        if session == None:
            print("GETTING UDP WITH NONE SESSION")
            return
    except:
        print("GETTING UDP WITHOUT SESSION")
        return
    
    if not session.jointTotals: # initialize iteration table
        session.jointTotals = data
        return

    for jointName in data:
        for i in range(3):
            session.jointTotals[jointName][i] += data[jointName][i]
    session.totalToAverage += 1

# Allow for http polling
@updupdate_blueprint.route('/udp/update', methods=["POST"])
def poll():
    id = request.json.get("ID", None)
    if not (id and type(id) == int):
        return "Malformed Request", 400
    
    addr = dataMapping[id]
    session = temporaryData[addr]

    # Limit polling to 100ms
    if time.time() - session.lastPolled > 0.1:
        session.lastPolled = time.time()
    else:
        return {"change": "nothing"}

    # Ensure we have recieved udp since last poll
    if not session.jointTotals:
        return "no data", 401
    
    # Get important specifics for udp
    totals = session.jointTotals
    amount = session.totalToAverage
    
    # Clear data
    session.jointTotals = None
    session.totalToAverage = 1

    # Average joint locations, update and return info
    for jointName in totals:
        for i in range(3):
            totals[jointName][i] /= amount
    
    #print("totals:", totals)
    change = session.process_poll(totals)
    if not change:
        return {"change": "nothing"}

    elif change == "complete": # finished
        dataMapping[id] = None
        temporaryData[addr] = None
        print("FINISHED!!!!!!!!!!!!!!!!")
        return {"change": "complete"}

    elif change == "next routine":
        next_workout_data = session.routine_data[session.routine_counter]
        mode = next_workout_data["workoutType"]
        maxReps = next_workout_data["reps"]

        session = makeSession(mode, maxReps, session.routine_data, session.routine_counter)
        temporaryData[addr] = session

        return {"change": "message", "details": f"Set complete. Next workout is {maxReps} reps of {mode}"}

    elif change == "new state":
        print("New State:", session.rep_state, "total reps:", session.reps)
        return {"change": session.rep_state, "reps": session.reps}

    else:
        print("Bad form: ", change)
        return {"change": "message", "details": change}
