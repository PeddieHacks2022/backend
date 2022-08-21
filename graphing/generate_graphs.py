import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

def generate_time_graph(dates, timeInMinutes):
  x = [dt.datetime.strptime(d, "%m/%d/%Y").date() for d in dates]
  #print(x)
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
  plt.gca().xaxis.set_major_locator(mdates.DayLocator())
  line = plt.plot(x,timeInMinutes)
  plt.title('Time Spent Exercising in Last Week')
  plt.xlabel('Date')
  plt.ylabel('Time in Minutes')
  plt.gcf().autofmt_xdate()
  plt.savefig('./statistics/graphs/time_graph.png')
  line = line.pop(0)
  line.remove()

def generate_reps_graph(dates, repsPerDay):
  prev = np.array([0 for i in range(len(dates))])
  x = [dt.datetime.strptime(d, "%m/%d/%Y").date() for d in dates]
  #print(x)
  for key in repsPerDay:
    repsPerDay[key] = np.array(repsPerDay[key])
    print(repsPerDay[key])
    print(prev)
    plt.bar(x, repsPerDay[key], bottom = prev)
    prev += repsPerDay[key]
  plt.ylabel('Reps')
  plt.xlabel('Date')
  plt.legend(repsPerDay.keys())
  plt.ylim([0, max(prev) * 1.25])
  plt.title('Exercises by Rep Done in Last Week')
  plt.savefig('./statistics/graphs/reps_graph.png')

if __name__ == "__main__":
    dates = ['01/02/1991','01/03/1991','01/04/1991']
    timeInMinutes = [60, 70, 80]
    repsPerDay = {"Pushups": [20, 35, 50], "Situps": [55, 60, 0], "Planks": [0, 0, 10]}
    generate_time_graph(dates, timeInMinutes)
    generate_reps_graph(dates, repsPerDay)