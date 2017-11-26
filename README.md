# IFTTT event loop

Monitor stuff and send IFTTT maker webhooks when something interesting happens

## Requirements

* Python 3
* requests

## Installation

TODO: make a package, if anyone cares

* Copy contents of `secret_empty.py` to `secrets.py` and add the IFTTT maker webhook key
* Make a Python file in the `triggers/` folder
* Define a function there where the first return value is whether to trigger a webhook, and the second return value is a tuple with up to three values to include in the webhook
* Copy contents of `event_cfg_empty.py` to `event_cfg.py` and adjust it to work with the function defined in the `triggers/` folder

## Usage

### Command line

To check all triggers every `<interval>` seconds:

`python event_loop.py <interval>`

### As a library

TODO
