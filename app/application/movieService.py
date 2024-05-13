from ..domain.movie import Movie
from ..infrastructure.movieRepository import MovieRepository


class MovieService:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def create_movie(self, movie_data: dict) -> Movie:
        return self.movie_repository.save(movie_data)

    def get_movies(self) -> Movie:
        return self.movie_repository.get()

    def get_movie_by_id(self, movie_id: int) -> Movie:
        return self.movie_repository.get_movie_by_id(movie_id)

    def update_movie(self, movie_data: dict, movie_id: int) -> Movie:
        return self.movie_repository.update(movie_data, movie_id)

    def delete_movie(self, movie_id: int) -> None:
        return self.movie_repository.delete(movie_id)

    async def get_movie_recommendations(self):
        return await self.movie_repository.get_movie_recommendations()

    async def get_movie_recommendations_by_id(self, user_id: int):
        return await self.movie_repository.get_movie_recommendations_by_id(user_id)
