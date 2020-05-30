import time
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath('../Lab1'))

from wtiproj01_client import RedisQueue

def startSending():
    print("SENDING AT 100Hz")
    queue = RedisQueue(name='lab2Queue')
    df = pd.read_table("../user_ratedmovies.dat", sep="\t")
    queue.flushdb()
    try:
        for index in df.iterrows():
            queue.put(index[1].to_json())
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nSent {0} elements of user_ratedmovies.dat".format(index[0] + 1))


if __name__ == "__main__":
    startSending()
