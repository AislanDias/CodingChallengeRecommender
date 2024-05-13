from __future__ import print_function, division

import pickle
import pandas as pd
from sklearn.utils import shuffle


class Preprocess:
    def __init__(self):
        df = pd.read_csv("rating.csv")

        df = shuffle(df)
        cutoff = int(0.8 * len(df))
        df_train = df.iloc[:cutoff]
        df_test = df.iloc[cutoff:]

        self.user2movie = {}
        self.movie2user = {}
        self.usermovie2rating = {}

        df_train.apply(self.update_user2movie_and_movie2user, axis=1)

        self.usermovie2rating_test = {}

        df_test.apply(self.update_usermovie2rating_test, axis=1)

        with open("user2movie.json", "wb") as f:
            pickle.dump(self.user2movie, f)

        with open("movie2user.json", "wb") as f:
            pickle.dump(self.movie2user, f)

        with open("usermovie2rating.json", "wb") as f:
            pickle.dump(self.usermovie2rating, f)

        with open("usermovie2rating_test.json", "wb") as f:
            pickle.dump(self.usermovie2rating_test, f)

    def update_user2movie_and_movie2user(self, row):
        i = int(row.userId)
        j = int(row.movie_idx)
        if i not in self.user2movie:
            self.user2movie[i] = [j]
        else:
            self.user2movie[i].append(j)

        if j not in self.movie2user:
            self.movie2user[j] = [i]
        else:
            self.movie2user[j].append(i)

        self.usermovie2rating[(i, j)] = row.rating

    def update_usermovie2rating_test(self, row):
        i = int(row.userId)
        j = int(row.movie_idx)
        self.usermovie2rating_test[(i, j)] = row.rating
