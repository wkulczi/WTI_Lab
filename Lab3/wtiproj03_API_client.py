import json
import time

import requests


def printdata(data:requests):
    print("========================================================================")
    print("request.url: %s" %data.url)
    print("request.status_code %s" %data.status_code)
    print("request.headers %s" %data.headers)
    print("request.text %s" %data.text)
    print("request.request.body %s" %data.request.body)
    print("request.request.headers %s" %data.request.headers)
    print("========================================================================")


def main():
    delete_data = {"userID": 71510.0, "movieID": 3}
    add_data = {"userID": 71510.0, "movieID": 3.0, "rating": 3.0, "Action": 0.0, "Adventure": 0.0, "Animation": 0.0,
                "Children": 0.0, "Comedy": 1.0, "Crime": 0.0, "Documentary": 0.0, "Drama": 0.0, "Fantasy": 0.0,
                "Film-Noir": 0.0, "Horror": 0.0, "IMAX": 0.0, "Musical": 0.0, "Mystery": 0.0, "Romance": 1.0,
                "Sci-Fi": 0.0, "Short": 0.0, "Thriller": 0.0, "War": 0.0, "Western": 0.0}

    post = requests.post('http://127.0.0.1:5000/rating', data=json.dumps(add_data))
    printdata(post)
    time.sleep(0.01)
    delete = requests.delete('http://127.0.0.1:5000/ratings', data=json.dumps(delete_data))
    time.sleep(0.01)
    printdata(delete)
    getratings = requests.get('http://127.0.0.1:5000/ratings')
    time.sleep(0.01)
    printdata(getratings)
    getavggenre = requests.get('http://127.0.0.1:5000/avg-genre-ratings/all-users')
    time.sleep(0.01)
    printdata(getavggenre)
    getuseravg = requests.get('http://127.0.0.1:5000/avg-genre-ratings/user71510')
    time.sleep(0.01)
    printdata(getuseravg)

if __name__ == "__main__":
    main()
