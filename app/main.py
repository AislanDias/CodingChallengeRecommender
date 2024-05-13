from app.application.ratingService import RatingService
from app.infrastructure.ratingRepository import RatingRepository
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .infrastructure.database import get_db
from .application.userService import UserService
from .application.movieService import MovieService
from .infrastructure.userRepository import UserRepository
from app.infrastructure.movieRepository import MovieRepository
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.get("/filmes/recomendacoes")
async def get_movie_recommendations(db: Session = Depends(get_db)):
    movie_service = MovieService(MovieRepository(db))
    predictions = await movie_service.get_movie_recommendations()

    return {
        "movieId": predictions[0],
        "userId": predictions[1],
        "predictions": predictions[2],
    }


@app.get("/filmes/{user_id}/recomendacoes")
async def get_user_all_recommendations_by_id(
    user_id: int, db: Session = Depends(get_db)
):
    movie_service = MovieService(MovieRepository(db))
    predictions = await movie_service.get_movie_recommendations_by_id(user_id)

    return {"movieId": predictions[0], "movieTitle": predictions[1]}


@app.get("/users")
def get_user_all_users(db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))

    return user_service.get_users()


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))

    return user_service.get_user_by_id(user_id)


@app.post("/users/add")
def create_user(user_data: dict, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    return user_service.create_user(user_data)


@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))
    return user_service.update_user(user_data, user_id)


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(UserRepository(db))

    return user_service.delete_user(user_id)


# Movies
@app.get("/filmes")
def get_movie_all_movies(db: Session = Depends(get_db)):
    movie_service = MovieService(MovieRepository(db))

    return movie_service.get_movies()


@app.get("/filmes/{movie_id}")
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie_service = MovieService(MovieRepository(db))

    return movie_service.get_movie_by_id(movie_id)


@app.post("/filmes/add")
def create_movie(movie_data: dict, db: Session = Depends(get_db)):
    movie_service = MovieService(MovieRepository(db))
    return movie_service.create_movie(movie_data)


@app.put("/filmes/{movie_id}")
def update_movie(movie_id: int, movie_data: dict, db: Session = Depends(get_db)):
    movie_service = MovieService(MovieRepository(db))
    return movie_service.update_movie(movie_data, movie_id)


@app.delete("/filmes/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie_service = MovieService(MovieRepository(db))

    return movie_service.delete_movie(movie_id)


# Ratings


@app.get("/ratings")
def get_rating_all_ratings(db: Session = Depends(get_db)):
    rating_service = RatingService(RatingRepository(db))

    return rating_service.get_ratings()


@app.get("/ratings/{rating_id}")
def get_rating_by_id(rating_id: int, db: Session = Depends(get_db)):
    rating_service = RatingService(RatingRepository(db))

    return rating_service.get_rating_by_id(rating_id)


@app.post("/ratings/add")
def create_rating(rating_data: dict, db: Session = Depends(get_db)):
    rating_service = RatingService(RatingRepository(db))
    return rating_service.create_rating(rating_data)


@app.put("/ratings/{rating_id}")
def update_rating(rating_id: int, rating_data: dict, db: Session = Depends(get_db)):
    rating_service = RatingService(RatingRepository(db))
    return rating_service.update_rating(rating_data, rating_id)


@app.delete("/ratings/{rating_id}")
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating_service = RatingService(RatingRepository(db))

    return rating_service.delete_rating(rating_id)
