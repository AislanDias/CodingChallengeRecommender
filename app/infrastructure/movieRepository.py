from app.infrastructure.recommenders.userbased import Colaborative
from ..domain.models import Movie, User
from sqlalchemy.orm import Session
from typing import Union


class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, movie_data: dict) -> Movie:
        db_movie = Movie(**movie_data)
        self.db.add(db_movie)
        self.db.commit()
        self.db.refresh(db_movie)
        return db_movie

    def update(self, movie_data: dict, movie_id: int) -> Union[Movie, None]:
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if movie:
            for var, value in movie_data.items():
                setattr(movie, var, value)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        return None

    def delete(self, movie_id: int) -> None:
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if movie:
            self.db.delete(movie)
            self.db.commit()

    def get_movie_by_id(self, movie_id: int) -> Union[Movie, None]:
        movie = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if movie:
            return movie

        return None

    async def get_movie_recommendations_by_id(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()

        collaborative = Colaborative()
        movies = self.db.query(Movie).all()
        return await collaborative.get_movie_recommendations_by_id(
            user_id, movies, user
        )

    async def get_movie_recommendations(self):
        collaborative = Colaborative()
        return await collaborative.get_movie_recommendations()

    def get(self) -> Movie:
        movies = self.db.query(Movie).all()

        return movies
