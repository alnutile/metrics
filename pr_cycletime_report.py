import json
import sys
import time
from datetime import datetime  
from datetime import timedelta
from statistics import mean, median, mode, stdev

if __name__ == "__main__":
    filename = sys.argv[1]
    file = open(filename)
    json_object = json.load(file)
    number = 0
    total_time = 0
    list = []

    for pr in json_object:
      number += 1
      seconds = pr["seconds"]
      list.append(seconds);
      total_time = total_time + seconds
      
    avg_cycle_time = total_time / number
    time = timedelta(avg_cycle_time)
    d = datetime(1,1,1) + time
    med = median(list)

    print(f"Total time: {total_time}")
    print(f"cycle_time: {avg_cycle_time}")
    print(f"Median: {med}")
    days = avg_cycle_time//86400
    hours = (avg_cycle_time - days*86400)//3600
    minutes = (avg_cycle_time - days*86400 - hours*3600)//60
    seconds =  (avg_cycle_time - days*86400 - hours*3600 - minutes*60)

    med_days = med//86400
    med_hours = (med - med_days*86400)//3600
    med_minutes = (med - med_days*86400 - med_hours*3600)//60
    med_seconds =  (med - med_days*86400 - med_hours*3600 - med_minutes*60)
    print(f"Mean: days {days}, hours {hours}, minutes {minutes}, seconds {seconds}")
    print(f"Median: days {med_days}, hours {med_hours}, minutes {med_minutes}, seconds {med_seconds}")



