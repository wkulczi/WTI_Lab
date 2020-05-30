import json
import time

import sys
import os
sys.path.append(os.path.abspath('../Lab1'))

from wtiproj01_client import RedisQueue


def list_summary(datalist):
    return "\nRECEIVING AT 4Hz\nEmpty elements fetched: {0}\nNon empty elements in list: {1}\n".format(datalist.count([]),
                                                                                     (len(datalist) - datalist.count(
                                                                                         [])))


def receive():
    print("RECEIVING AT 4Hz")
    queue = RedisQueue(name='lab2Queue')
    queue.ltrim(0, 50)
    datalist = []
    start_time = time.time()
    try:
        while True:
            data = queue.lrange(0, 0)
            datalist.append(data)
            if len(data) > 0:
                print(json.loads(data[0]))
                queue.ltrim(1, -1)
            time.sleep(0.25)
            if time.time() - start_time >= 10:
                print(list_summary(datalist))
                break
    except KeyboardInterrupt:
        print(list_summary(datalist))


if __name__ == "__main__":
    receive()
