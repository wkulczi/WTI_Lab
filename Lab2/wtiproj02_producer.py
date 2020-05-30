import itertools
import json
import time
import pandas as pd
from Lab1.wtiproj01_client import RedisQueue


def startSending():
    queue = RedisQueue(name='lab2Queue')
    df = pd.read_table("../user_ratedmovies.dat", sep="\t")
    queue.flushdb()
    try:
        for index in df.iterrows():
            queue.put(index[1].to_json())
            time.sleep(0.6)
    except KeyboardInterrupt:
        print("Sent {0} elements of user_ratedmovies.dat".format(index[0]+1))

if __name__ == "__main__":
    startSending()
