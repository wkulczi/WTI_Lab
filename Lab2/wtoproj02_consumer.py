import json
import time

from Lab1.wtiproj01_client import RedisQueue


def receive():
    queue = RedisQueue(name='lab2Queue')
    queue.ltrim(0, 50)
    while True:
        data = queue.lrange(0, 0)
        if len(data) > 0:
            print(json.loads(data[0]))
            queue.ltrim(1,-1)
        time.sleep(0.01)


if __name__ == "__main__":
    receive()