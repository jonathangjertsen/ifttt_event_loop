"""
from triggers.<your file> import *

events = {
    <IFTTT event name>: {
        "func": <trigger function>,
        "args": <dict with arguments to trigger function>,
        "conditions": {
            "time of day": <time of day in %H:%M format>, # OPTIONAL
            "period": <period in second>, # OPTIONAL
        },
    },
}
"""
