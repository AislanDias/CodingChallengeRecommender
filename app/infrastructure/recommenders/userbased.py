import pickle
import os
import asyncio
import numpy as np
import pandas as pd
from sortedcontainers import SortedList


class Colaborative:
    def __init__(self):
        self.fakeGenres = ["comedia", "romantico", "acao", "aventura"]
        self.fakeArtists = ["stephen king", "stallone", "van damme", "depp"]
        self.K = 25  # numero de vizinhos
        self.limit = 5  # numero de filmes em comum para ser considerado
        self.neighbors = []  # armazenar os vizinhos nesta lista
        self.averages = []  # media de avaliacao de cada usuario
        self.deviations = []  # desvios de cada usuario
        self.N = 0
        self.M = 0

        with open("app/cache/user2movie.json", "rb") as f:
            self.user2movie = pickle.load(f)

        with open("app/cache/movie2user.json", "rb") as f:
            self.movie2user = pickle.load(f)

        with open("app/cache/usermovie2rating.json", "rb") as f:
            self.usermovie2rating = pickle.load(f)

        with open("app/cache/usermovie2rating_test.json", "rb") as f:
            self.usermovie2rating_test = pickle.load(f)

        self.N = np.max(list(self.user2movie.keys())) + 1
        m1 = np.max(list(self.movie2user.keys()))
        m2 = np.max([m for (u, m), r in self.usermovie2rating_test.items()])
        self.M = max(m1, m2) + 1

    def predict(self, i, m):
        numerator = 0
        denominator = 0
        for neg_w, j in self.neighbors[i]:
            try:
                numerator += -neg_w * self.deviations[j][m]
                denominator += abs(neg_w)
            except KeyError:
                pass

        if denominator == 0:
            prediction = self.averages[i]
        else:
            prediction = numerator / denominator + self.averages[i]
        prediction = min(5, prediction)
        prediction = max(0.5, prediction)
        return prediction

    def calculate_avg_deviation(self, i: int, movies_i: set):
        ratings_i = {movie: self.usermovie2rating[(i, movie)] for movie in movies_i}
        avg_i = np.mean(list(ratings_i.values()))
        dev_i = {movie: (rating - avg_i) for movie, rating in ratings_i.items()}
        dev_i_values = np.array(list(dev_i.values()))
        sigma_i = np.sqrt(dev_i_values.dot(dev_i_values))

        self.averages.append(avg_i)
        self.deviations.append(dev_i)

        return sigma_i, dev_i

    async def find_closest_neighbors(self, i):
        movies_i = self.user2movie[i]
        movies_i_set = set(movies_i)

        sigma_i, dev_i = self.calculate_avg_deviation(i, movies_i)

        sl = SortedList()
        for j in range(self.N):
            if j != i:
                movies_j = self.user2movie[j]
                movies_j_set = set(movies_j)
                common_movies = movies_i_set & movies_j_set
                if len(common_movies) > self.limit:
                    ratings_j = {
                        movie: self.usermovie2rating[(j, movie)] for movie in movies_j
                    }
                    avg_j = np.mean(list(ratings_j.values()))
                    dev_j = {
                        movie: (rating - avg_j) for movie, rating in ratings_j.items()
                    }
                    dev_j_values = np.array(list(dev_j.values()))
                    sigma_j = np.sqrt(dev_j_values.dot(dev_j_values))

                    numerator = sum(dev_i[m] * dev_j[m] for m in common_movies)
                    w_ij = numerator / (sigma_i * sigma_j)

                    sl.add((-w_ij, j))
                    if len(sl) > self.K:
                        del sl[-1]

        self.neighbors.append(sl)

        if i % 1 == 0:
            print(i)

    def mse(self, p, t):
        p = np.array(p)
        t = np.array(t)
        return np.mean((p - t) ** 2)

    async def get_neighbors(self):
        promises = []

        for i in range(self.N):
            promises.append(self.find_closest_neighbors(i))
        await asyncio.gather(*promises)

        with open("app/cache/neighbors.json", "wb") as f:
            pickle.dump(self.neighbors, f)
        with open("app/cache/deviations.json", "wb") as f:
            pickle.dump(self.deviations, f)
        with open("app/cache/averages.json", "wb") as f:
            pickle.dump(self.averages, f)

    async def get_movie_recommendations_by_id(self, user_id, movies, user):
        with open("app/cache/neighbors.json", "rb") as f:
            self.neighbors = pickle.load(f)
        with open("app/cache/deviations.json", "rb") as f:
            self.deviations = pickle.load(f)
        with open("app/cache/averages.json", "rb") as f:
            self.averages = pickle.load(f)

        predictions = []
        moviesTitle = []
        moviesId = []
        genre = []
        artist = []

        for m in movies:
            moviesId.append(m.id)
            moviesTitle.append(m.title)
            genre.append(m.genres)
            artist.append(m.artist)

            prediction = self.predict(user_id, m.id)
            predictions.append(prediction)

        df = pd.DataFrame(
            {
                "movieId": moviesId,
                "movieTitle": moviesTitle,
                "predictions": predictions,
                "genre": genre,
                "artist": artist,
            }
        )

        self.fakeGenres.remove(user.preferredGenre)
        self.fakeArtists.remove(user.preferredArtist)

        df = df.sort_values(by="predictions")

        df = df.sort_values(by="genre")
        t = pd.CategoricalDtype(categories=self.fakeGenres, ordered=True)
        df["genre"] = pd.Series(df.genre, dtype=t)
        df.sort_values(by=["genre"], inplace=True)

        df = df.sort_values(by="artist")
        t = pd.CategoricalDtype(categories=self.fakeArtists, ordered=True)
        df["artist"] = pd.Series(df.artist, dtype=t)
        df.sort_values(by=["artist"], inplace=True)

        predict = [df["movieId"].to_list(), df["movieTitle"].to_list()]

        return predict

    async def get_movie_recommendations(self):
        with open("app/cache/neighbors.json", "rb") as f:
            self.neighbors = pickle.load(f)
        with open("app/cache/deviations.json", "rb") as f:
            self.deviations = pickle.load(f)
        with open("app/cache/averages.json", "rb") as f:
            self.averages = pickle.load(f)

        predictions = []
        usersId = []
        moviesId = []

        for (i, m), target in self.usermovie2rating.items():
            prediction = self.predict(i, m)

            moviesId.append(m)
            usersId.append(i)
            predictions.append(prediction)

        df = pd.DataFrame(
            {
                "movieId": moviesId,
                "userId": usersId,
                "predictions": predictions,
            }
        )
        df = df.sort_values(by="predictions")
        predict = [
            df["movieId"].to_list(),
            df["userId"].to_list(),
            df["predictions"].to_list(),
        ]

        return predict
