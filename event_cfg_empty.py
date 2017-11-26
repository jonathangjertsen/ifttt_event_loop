from triggers.example import *

events = {
    "test": {
        "func": trigger_example,
        "args": {
            "do_it": True
        },
        "conditions": {
            "periodic": 10
        },
    },
}
