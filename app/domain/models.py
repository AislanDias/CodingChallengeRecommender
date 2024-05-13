from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    preferredGenre = Column(String, index=True)
    preferredArtist = Column(String, index=True)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    genres = Column(String, index=True)
    artist = Column(String, index=True)


class Ratings(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"))
    movieId = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Integer, index=True)
    movie_idx = Column(Integer, index=True)
