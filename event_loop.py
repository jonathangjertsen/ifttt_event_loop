from datetime import datetime
from time import sleep
import sys

from ifttt import trigger
from event_cfg import events
from secret import debug

def run_loop(sleep_time):
    counters = {}
    timeofdays = {}
    for event in events:
        conditions = events[event]["conditions"]
        if "periodic" in conditions:
            counters[event] = 0
        if "time of day" in conditions:
            timeofdays[event] = False

    while True:
        sleep(sleep_time)
        for event in events:
            do_check = False
            conditions = events[event]["conditions"]

            # Check periodic triggers
            if "periodic" in conditions:
                counters[event] += sleep_time
                if counters[event] >= conditions["periodic"]:
                    counters[event] = 0
                    do_check = True

            # Check time-of-day triggers
            if "time of day" in conditions:
                if not timeofdays[event]:
                    trigger_time = datetime.strptime(conditions["time of day"], "%H:%M").time()
                    if trigger_time >= datetime.now().time():
                        do_check = True
                        timeofdays[event] = True

            # Run triggered events
            if do_check:
                func = events[event]["func"]
                args = events[event]["args"]
                do_trigger, data = func(**args)
                if debug:
                    print("Event data: ", data)
                if do_trigger:
                    response = trigger(event, *data)
                    if debug:
                        print("IFTT response: {response}".format(response=response.text))

if __name__ == "__main__":
    run_loop(max(10, int(sys.argv[1])))
