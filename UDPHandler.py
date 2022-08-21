# imports
import time
from sessionModels import makeSession
from db.workout import WorkoutModel #, get_by_id as getWorkoutById
from flask import Blueprint, request
updupdate_blueprint = Blueprint('updupdate_blueprint', __name__)

# data storage
temporaryData = {}
dataMapping = {}
workoutModel = WorkoutModel()

# Processing UDP updates 
def process(address, data):
    #print("Processing", data, " from", address)
    if type(data) == str:
        userID, workoutID = [int(e) for e in data.split(" ")]
        workout_specs = workoutModel.get_by_id(workoutID)
        mode = workout_specs[3]
        maxReps = workout_specs[4]

        # Add new user 
        session = makeSession(mode, maxReps)
        temporaryData[address[0]] = session
        dataMapping[userID] = address[0]
        print("Starting excersize UDP")
        return
    
    # Process table update
    session = temporaryData[address[0]]
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

    elif change == "Complete": # finished
        # TODO: clear data
        return {"change": "Complete"}

    elif change == "New state":
        print("New State:", session.rep_state, "total reps:", session.reps)
        return {"change": session.rep_state, "reps": session.reps}

    else:
        print("Bad form: ", change)
        return {"change": "bad form", "details": change}
