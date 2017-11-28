from triggers.example import *

events = {
    "test": {
        "func": trigger_example,
        "args": {
            "do_it": True
        },
        "conditions": {
            # Do it every 10 seconds
            "periodic": 10,

            # Do it at 17:12 every day
            "time of day": "17:12",

            # Do it every minute but it's like cron
            "cron": "*/1 * * * *"
        },
    },
}
