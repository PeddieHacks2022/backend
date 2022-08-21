#import string
from datetime import datetime, timedelta
from graphing.generate_graphs import generate_time_graph, generate_reps_graph
from db import connect
from db.utils import generate_id


WORKOUT_MODES = ["Bicep Curl", "Left Bicep Curl", "Right Bicep Curl", "Overhead Press", "Left Overhead Press", "Right Overhead Press"]
class StatisticsModel:
    def grab_data(self, user_id: int, date_index: str):
        return connect().execute("""
        SELECT * FROM statistics WHERE user_id = ? AND date = ?
        """, (user_id, date_index)).fetchone()

    def verify_exists(self, user_id: int, date_index: str):
        node = self.grab_data(user_id, date_index)

        if node == None:
            # Create node for the day
            print("Creating stat node")
            conn = connect()
            conn.execute(
                "INSERT INTO statistics VALUES (:id, :date, :data, :user_id)",
                {"id": generate_id(), "date": date_index, "data": ",".join(["0" for i in range(13)]), "user_id": user_id}
            );
            conn.commit()
            print("Created stat node")

    def updateStats(self, user_id: int, mode: str, reps: int, minutes_taken: int, date_index: str):
        # Check if user id node for today exists
        self.verify_exists(user_id, date_index)

        # Update today's node
        #today = datetime.today().strftime('%d-%m-%Y')
        node = self.grab_data(user_id, date_index)
        ind_change = WORKOUT_MODES.index(mode)
        listing = [int(e) for e in node[2].split(",")]
        listing[ind_change] += reps
        listing[ind_change + 6] += minutes_taken
        listing[12] += 1
        new_val = ",".join([str(e) for e in listing])
        
        # Update in DB
        conn = connect()
        conn.execute("UPDATE statistics SET data = ? WHERE user_id = ? AND date = ?;", (new_val, user_id, date_index));
        conn.commit()
        print("updated", new_val)
        return

"""
 id INT PRIMARY KEY          NOT NULL,
            date                TEXT    NOT NULL,
            data                TEXT    NOT NULL,
            user_id             INT     NOT NULL
"""

def init():
    print("Running stat mock data creation")            # adds previous days of the week (as we cant add it ourselves)
    statisticsModel = StatisticsModel()
    # user id, mode,        reps, minutes_taken, day
    """
    d = datetime(2022, 8, 15).strftime('%d-%m-%Y')
    statisticsModel.updateStats(1500, "Bicep Curl",             15, 10, d)
    statisticsModel.updateStats(1500, "Left Bicep Curl",        15, 7, d)
    statisticsModel.updateStats(1500, "Right Bicep Curl",       15, 8, d)
    statisticsModel.updateStats(1500, "Overhead Press",         15, 18, d)
    statisticsModel.updateStats(1500, "Left Overhead Press",    15, 12, d)
    statisticsModel.updateStats(1500, "Right Overhead Press",   15, 23, d)
    statisticsModel.updateStats(1500, "Bicep Curl",             5, 15, d)

    
    d = datetime(2022, 8, 16).strftime('%d-%m-%Y')
    statisticsModel.updateStats(1500, "Bicep Curl",             15, 9, d)
    statisticsModel.updateStats(1500, "Left Bicep Curl",        16, 9, d)
    statisticsModel.updateStats(1500, "Overhead Press",         18, 15, d)
    statisticsModel.updateStats(1500, "Left Overhead Press",    20, 18, d)
    statisticsModel.updateStats(1500, "Bicep Curl",             10, 25, d)

    
    d = datetime(2022, 8, 17).strftime('%d-%m-%Y')
    statisticsModel.updateStats(1500, "Overhead Press",         25, 15, d)
    statisticsModel.updateStats(1500, "Left Overhead Press",    30, 20, d)
    statisticsModel.updateStats(1500, "Right Overhead Press",   30, 35, d)

    d = datetime(2022, 8, 18).strftime('%d-%m-%Y')
    statisticsModel.updateStats(1500, "Bicep Curl",             16, 9, d)
    statisticsModel.updateStats(1500, "Left Bicep Curl",        17, 6, d)
    statisticsModel.updateStats(1500, "Right Bicep Curl",       16, 7, d)
    statisticsModel.updateStats(1500, "Overhead Press",         16, 17, d)
    statisticsModel.updateStats(1500, "Left Overhead Press",    16, 11, d)
    statisticsModel.updateStats(1500, "Right Overhead Press",   16, 22, d)
    statisticsModel.updateStats(1500, "Bicep Curl",             6, 14, d)

    # ignore 19th

    d = datetime(2022, 8, 20).strftime('%d-%m-%Y')
    statisticsModel.updateStats(1500, "Bicep Curl",             18, 8, d)
    statisticsModel.updateStats(1500, "Left Bicep Curl",        18, 5, d)
    statisticsModel.updateStats(1500, "Right Bicep Curl",       18, 6, d)
    statisticsModel.updateStats(1500, "Overhead Press",         18, 15, d)
    statisticsModel.updateStats(1500, "Left Overhead Press",    18, 10, d)
    statisticsModel.updateStats(1500, "Right Overhead Press",   18, 10, d)
    statisticsModel.updateStats(1500, "Bicep Curl",             20, 20, d)

    
    d = datetime(2022, 8, 21).strftime('%d-%m-%Y')
    statisticsModel.updateStats(1500, "Bicep Curl",             20, 8, d)
    statisticsModel.updateStats(1500, "Left Bicep Curl",        21, 5, d)
    statisticsModel.updateStats(1500, "Right Bicep Curl",       22, 6, d)
    statisticsModel.updateStats(1500, "Overhead Press",         23, 15, d)
    statisticsModel.updateStats(1500, "Left Overhead Press",    15, 10, d)
    statisticsModel.updateStats(1500, "Right Overhead Press",   18, 10, d)
    statisticsModel.updateStats(1500, "Bicep Curl",             30, 1, d)
    """

    
    start_date = datetime(2022, 8, 15)
    dates = [(start_date + timedelta(days=i)).strftime('%m/%d/%Y') for i in range(7)]
    total_times = [0 for i in range(7)]
    rep_counts = {e : [0 for i in range(7)] for e in WORKOUT_MODES}

    # update
    for i in range(7):
        d = (datetime(2022, 8, 15) + timedelta(days=i)).strftime('%d-%m-%Y')
        node = statisticsModel.grab_data(1500, d)
        if node:
            data = [int(e) for e in node[2].split(",")]
            total_times[i] += sum(data[5:12])
            for m in range(6):
                mode = WORKOUT_MODES[m]
                rep_counts[mode][i] += data[i]
            
    
    #print(dates)
    #print(total_times)
    #print(rep_counts)

    generate_time_graph(dates, total_times)
    generate_reps_graph(dates, rep_counts)
    