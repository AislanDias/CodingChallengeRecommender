class Ratings:
    def __init__(
        self, userId: int, movieId: int, rating: int, movie_idx: int, id: int = None
    ):  # type: ignore
        self.id = id
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
