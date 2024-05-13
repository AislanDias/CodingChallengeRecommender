from typing import List
import pickle
import pytest
from app.domain.models import Ratings, User, Movie
from app.infrastructure.database import SessionLocal
from faker import Faker


# @pytest.fixture(scope="session", autouse=True)
@pytest.fixture()
def users_in_db(n=5):
    fake = Faker()
    users = []
    for _ in range(n):
        username = fake.user_name()
        # Add user to database
        db = SessionLocal()
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        users.append(user)
    yield users
    db = SessionLocal()
    for user in users:
        db.delete(user)
    db.commit()
    db.close()


# @pytest.fixture
# def create_user():
#     fake = Faker()
#     username = fake.user_name()
#     email = fake.email()
#     return [username, email]


@pytest.fixture
def create_multiple_users(qtd: int = 5) -> List:
    users = []
    for _ in range(qtd):
        fake = Faker()
        username = fake.user_name()
        email = fake.email()
        users.append([username, email])
    return users


@pytest.fixture
def movies_in_db(n=5):
    fake = Faker()
    movies = []
    for _ in range(n):
        title = fake.sentence()
        content = fake.sentence()
        db = SessionLocal()
        movie = Movie(title=title, content=content)
        db.add(movie)
        db.commit()
        db.refresh(movie)
        db.close()
        movies.append(movie)
    yield movies
    db = SessionLocal()
    for movie in movies:
        db.delete(movie)
    db.commit()
    db.close()


@pytest.fixture
def create_movie():
    fake = Faker()
    username = fake.user_name()
    email = fake.email()
    return [username, email]


@pytest.fixture
def ratings_in_db():
    fake = Faker()
    movieIds = []
    userIds = []
    ratings = []
    id = 0
    fakeGenres = ["comedia", "romantico", "acao", "aventura"]
    fakeArtists = ["stephen king", "stallone", "van damme", "depp"]

    db = SessionLocal()

    ratings = db.query(Ratings).all()
    movies = db.query(Movie).all()
    users = db.query(User).all()

    for rating in ratings:
        db.delete(rating)
    db.commit()

    for movie in movies:
        db.delete(movie)
    db.commit()

    for user in users:
        db.delete(user)
    db.commit()

    with open("app/cache/usermovie2rating_test.json", "rb") as f:
        usermovie2rating_test = pickle.load(f)

        for (i, m), target in usermovie2rating_test.items():
            title = fake.sentence()
            content = fake.sentence()
            username = fake.user_name()

            if i not in userIds:
                user = User(
                    id=i,
                    username=username,
                    preferredGenre=fakeGenres[id % 3],
                    preferredArtist=fakeArtists[id % 3],
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            if m not in movieIds:
                movie = Movie(
                    id=m,
                    title=title,
                    content=content,
                    genres=fakeGenres[id % 3],
                    artist=fakeArtists[id % 3],
                )
                db.add(movie)
                db.commit()
                db.refresh(movie)

            rating = Ratings(userId=i, movieId=m, rating=target)
            ratings.append(rating)
            db.add(rating)
            db.commit()
            db.refresh(rating)
            db.close()

            userIds.append(i)
            movieIds.append(m)
            id = id + 1

        yield ratings

        # Clean database
        db = SessionLocal()
        ratings = db.query(Ratings).all()
        movies = db.query(Movie).all()
        users = db.query(User).all()
        for rating in ratings:
            db.delete(rating)
        db.commit()

        for movie in movies:
            db.delete(movie)
        db.commit()

        for user in users:
            db.delete(user)
        db.commit()
        db.close()


def clean_database():
    db = SessionLocal()

    ratings = db.query(Ratings).all()
    movies = db.query(Movie).all()
    users = db.query(User).all()

    for rating in ratings:
        db.delete(rating)
    db.commit()

    for movie in movies:
        db.delete(movie)
    db.commit()

    for user in users:
        db.delete(user)
    db.commit()

    db.close()
