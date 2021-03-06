from datetime import datetime
from time import sleep
import sys

from croniter import croniter

from ifttt import trigger
from event_cfg import events
from secret import debug

def run_loop(sleep_time):
    """
    Check triggers, act on triggers

    :param sleep_time: Time to sleep between each iteration
    :return:
    """
    def default_counters():
        return { event: 0 for event in events if "periodic" in events[event]["conditions"] }

    def default_timeofdays():
        return { event: False for event in events if "time of day" in events[event]["conditions"] }

    def default_crons():
        base_time = datetime.now()
        crons = {}
        for event in events:
            if "cron" in events[event]["conditions"]:
                cron_string = events[event]["conditions"]["cron"]
                if croniter.is_valid(cron_string):
                    crons[event] = croniter(cron_string, base_time)
                    # Advance the iterator once so the first call to
                    # get_current() doesn't return the current time
                    crons[event].get_next()
                else:
                    raise ValueError("Invalid cron string specified for event {event}".format(event=event))
        return crons

    counters = default_counters()
    timeofdays = default_timeofdays()
    crons = default_crons()

    datetime_after_sleep = datetime.now()
    while True:
        # In case we did something time consuming, remove the time it took from the sleep time
        true_sleep_time = sleep_time - (datetime.now() - datetime_after_sleep).seconds

        # Goodnight
        sleep(max(true_sleep_time, 0))
        datetime_after_prev_sleep = datetime_after_sleep
        datetime_after_sleep = datetime.now()

        # Reset time-of-day flags
        if datetime_after_sleep.date() != datetime_after_prev_sleep.date():
            timeofdays = default_timeofdays()

        # Check all the triggers
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
                    if trigger_time >= datetime_after_sleep.time():
                        do_check = True
                        timeofdays[event] = True

            # Check cron-like triggers
            if "cron" in conditions:
                if crons[event].get_current(datetime) <= datetime_after_sleep:
                    do_check = True
                    crons[event].get_next(datetime)

            # Run triggered events
            if do_check:
                func = events[event]["func"]
                args = events[event]["args"]
                data = func(**args)
                if debug:
                    print("Event data: ", data)
                if data is not None:
                    response = trigger(event, *data)
                    if debug:
                        print("IFTT response: {response}".format(response=response.text))

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1].isdigit():
        sleep_time = int(sys.argv[1])
    else:
        print("No valid sleep time set, will default to 5 seconds")
        sleep_time = 5

    run_loop(sleep_time)
