import requests

from secret import key

def trigger(event, *values):
    return requests.post(
        url="https://maker.ifttt.com/trigger/{event}/with/key/{key}".format(event=event, key=key),
        json={ "value{idx}".format(idx=idx+1): value for idx, value in enumerate(values) }
    )

if __name__ == "__main__":
    response = trigger("test", "Title", "Text", "Extra")
    print(response.text)
