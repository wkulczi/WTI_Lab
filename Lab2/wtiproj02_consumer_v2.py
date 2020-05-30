import json
import time

from Lab1.wtiproj01_client import RedisQueue


def list_summary(datalist):
    return "\nEmpty elements fetched: {0}\nNon empty elements in list: {1}\n".format(datalist.count([]),
                                                                                     (len(datalist) - datalist.count(
                                                                                         [])))


def receive():
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
