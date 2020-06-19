import json

import pandas as pd


def prepare_data():
    rated_df = pd.read_table("../user_ratedmovies.dat", usecols=["userID", "movieID", "rating"], sep="\t").fillna(0)
    genres_df = pd.read_table("../movie_genres.dat", sep="\t").fillna(0)
    genres_df["isgen"] = 1
    rng = rated_df.set_index("movieID").join(genres_df.set_index("movieID"))
    table = pd.pivot_table(rng, values='isgen', index='movieID', columns=['genre'], fill_value=0)
    return pd.merge(rated_df, table, on='movieID')
# wyszukiwanie w pivot_table
# crosssection  table.xs(('martin','2014','Algebra'))
# query table.to_frame().query('student== "martin" & year == 2014 & subject == "Algebra"')
# multiindex dataframe table.loc[("Martin",2014,"Algebra")]
