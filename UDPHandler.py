# imports
import time
from exercise import process as processWorkoutChange
from flask import Blueprint, request
updupdate_blueprint = Blueprint('updupdate_blueprint', __name__)

# data storage
temporaryData = {}
dataMapping = {}
class workoutSession:
    time_started =  time.time()
    rep_state = "down"
    reps = 0

    jointTotals = None
    totalToAverage = 1
    rep_progress = 0

# Processing UDP updates 
def process(address, data):
    #print("Processing", data, " from", address)
    if type(data) == str:
        userID, workoutID = [int(e) for e in data.split(" ")]
        mode = "curl" # access dao

        # Add new user 
        session = workoutSession()
        temporaryData[address[0]] = session
        dataMapping[userID] = [address[0], mode]
        print("Made new account")
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
    
    addr, mode = dataMapping[id]
    session = temporaryData[addr]
    if not session.jointTotals:
        return "no data", 400
    
    # Get important specifics for udp
    totals = session.jointTotals
    amount = session.totalToAverage
    #print("changes made:", amount)
    
    # Clear data
    session.jointTotals = None
    session.totalToAverage = 1

    # Average joint locations, update and return info
    for jointName in totals:
        for i in range(3):
            totals[jointName][i] /= amount
    
    
    #print("totals:", totals)
    change = processWorkoutChange(mode, session, totals)
    if not change:
        return {"change": "nothing"}

    elif change == "New state":
        print("New State:", session.rep_state, "total reps:", session.reps)
        return {"change": session.rep_state, "reps": session.reps}

    else:
        print("Bad form: ", change)
        return {"change": "bad form", "details": change}
