import json

import pandas as pd
from flask import Flask, request
import numpy as np
from Lab3.wtiproj03_ETL import prepare_data


class Controller:
    def __init__(self):
        self.table = prepare_data()

    def append(self, datadict):
        self.table = self.table.append(datadict, ignore_index=True)

    def return_dataframe_json(self):
        return self.table.head(50).to_json(orient='records')

    def find_row(self, userid, movieid):
        return self.table.loc[(self.table['userID'] == userid) & (self.table['movieID'] == movieid)]

    def delete_row(self, userid, movieid):
        row_index = self.find_row(userid, movieid).index[0]
        self.table = self.table.drop(row_index, axis=0)

    def random_genre_ratings(self, **kwargs):
        cols = ["genre-" + x for x in self.table.columns[3:]]
        vals = np.random.rand(20)
        if "userID" in kwargs.keys():
            cols.append("userID")
            vals = np.append(vals, kwargs["userID"])
        return pd.DataFrame(columns=cols, data=[vals])


app = Flask(__name__)

app.config['FLASK_DEBUG'] = True

controller = Controller()


# Używając biblioteki Flask przygotuj uproszczoną, jednowątkową implementację
# interfejsu typu Web API (zbliżonego do usługi REST, ale nie spełniającej założenia
# HATEOAS) bazującego na reprezentacji danych w formacie JSON. Interfejs ten (tj. API)
# powinien umożliwiać
# zapis (z użyciem metody POST do punktu końcowego /rating) kolejnych wierszy tabeli uzyskanej w poprzednim kroku ćwiczenia,
# odczyt (z użyciem metody GET, z punktu końcowego usługi /ratings),
# kasowanie (z użyciem metody DELETE w punkcie końcowym usługi /ratings)
# oraz odczyt (z użyciem metody GET, z punktu końcowego usługi wspólnego dla wszystkich użytkowników /avg-genre-ratings/all-users) słownika zawierającego “zaślepkowe”
# (np. losowe) “średnie” oceny udzielone (przez wszystkich użytkowników) filmom poszczególnych gatunków,
# jak również odczyt aktualnego (również zaślepkowego, np. o losowych wartościach “udających” średnie oceny udzielone filmom poszczególnych gatunków)
# profilu użytkownika z użyciem metody GET, z punktu końcowego usługi o adresie
# właściwym dla danego identyfikatora użytkownika (identyfikatora wg. danych pliku user_ratedmovies.dat) /avg-genre-ratings/user<userID>.

# /ratings get
# /ratings delete

# zapis (z użyciem metody POST do punktu końcowego /rating) kolejnych wierszy tabeli uzyskanej w poprzednim kroku ćwiczenia,
@app.route('/rating', methods=['POST'])
def postRating():
    try:
        print(request.data)
        data = json.loads(request.data)
        if ('userID' or 'movieID') not in data:
            raise Exception("ERR: No userID or movieID info provided")
        controller.append(data)
        return json.dumps(data)
    except Exception as e:
        return str(e)


# odczyt (z użyciem metody GET, z punktu końcowego usługi /ratings),
@app.route('/ratings', methods=['GET'])
def getRatings():
    return controller.return_dataframe_json()


# kasowanie (z użyciem metody DELETE w punkcie końcowym usługi /ratings)
@app.route('/ratings', methods=['DELETE'])
def deleteRating():
    try:
        data = json.loads(request.data)
        if ("userID" and "movieID") not in data:
            raise Exception("ERR, please specify userID and movieID to delete")
        controller.delete_row(data["userID"], data["movieID"])
        return json.dumps({"Operation status":"Deleted"})

    except Exception as e:
        return str(e)


# oraz odczyt (z użyciem metody GET, z punktu końcowego usługi wspólnego dla wszystkich użytkowników /avg-genre-ratings/all-users) słownika zawierającego “zaślepkowe”...
@app.route('/avg-genre-ratings/all-users', methods=['GET'])
def average_all_users():
    return controller.random_genre_ratings().to_json(orient="records")


# jak również odczyt aktualnego (również zaślepkowego, np. o losowych wartościach “udających” średnie oceny udzielone filmom poszczególnych gatunków)...
# i mimo tego, że w zadaniu 3 jest napisane, ze ma być /user<userID> to w 4 już jest /<userID> -.-
@app.route('/avg-genre-ratings/<userID>', methods=['GET'])
def avg_user(userID):
    return controller.random_genre_ratings(userID=userID).to_json(orient="records")
