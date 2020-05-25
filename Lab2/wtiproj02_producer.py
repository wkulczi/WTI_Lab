import itertools
import json
import time

from Lab1.wtiproj01_client import RedisQueue


def startSending():
    queue = RedisQueue(name='lab2Queue')
    for i in itertools.count():
        queue.put(json.dumps({"iteration number": i}))
        time.sleep(0.01)


if __name__ == "__main__":
    startSending()
