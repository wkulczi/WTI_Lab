import json

import cherrypy as cherrypy
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


controller = Controller()


class Ratings(object):
    exposed = True
    _cp_config = {"request.methods_with_bodies": ("DELETE")}

    def GET(self):
        return controller.return_dataframe_json()

    def DELETE(self):
        rawData = cherrypy.request.body.read(int(cherrypy.request.headers['Content-Length']))
        try:
            b = json.loads(rawData)
            controller.delete_row(b['userID'], b['movieID'])
        except Exception as e:
            return json.dumps({"Operation status": e})


class Rating(object):
    exposed = True

    def POST(self):
        rawData = cherrypy.request.body.read(int(cherrypy.request.headers['Content-Length']))
        b = json.loads(rawData)
        controller.append(b)
        return b

    pass


class AvgGenreRatings(object):
    exposed = True

    def GET(self):
        return controller.random_genre_ratings().to_json(orient="records")


@cherrypy.popargs('index')
class AvgGenreRatingsForUser(object):
    exposed = True

    def GET(self, index):
        return controller.random_genre_ratings(userID=index).to_json(orient="records")


if __name__ == "__main__":
    cherrypy.tree.mount(Rating(), '/rating', {
        '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    })
    cherrypy.tree.mount(Ratings(), '/ratings', {
        '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    })
    cherrypy.tree.mount(AvgGenreRatings(), '/avg-genre-ratings', {
        '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    })
    cherrypy.tree.mount(AvgGenreRatingsForUser(), '/avg-genre-ratings/user', {
        '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    })

    cherrypy.engine.start()
    cherrypy.engine.block()
    cherrypy.config.update({'server.thread_pool': 100})
