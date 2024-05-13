import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_movie(movies_in_db):
    movie = movies_in_db[0].title
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/filmes/add", json={"title": movie[0]})
    assert response.status_code == 200
    assert response.json()["title"] == movie[0]


@pytest.mark.asyncio
async def test_update_movie(movies_in_db):
    movie_id = movies_in_db[0].id
    updatedmovie = "Jose Ferreira"
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.put(
            f"/filmes/{movie_id}",
            json={"title": updatedmovie},
        )

    assert response.status_code == 200

    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/filmes/{movie_id}")

    assert response.json()["title"] == updatedmovie


@pytest.mark.asyncio
async def test_get_movie_by_id(movies_in_db):
    movie = movies_in_db
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        movieEmail = await ac.get(f"/filmes/{movie[1].id}")

    assert movieEmail.status_code == 200
    assert movieEmail.json()["id"] == movie[1].id


@pytest.mark.asyncio
async def test_get_movies(movies_in_db):
    movies = movies_in_db
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        movies = await ac.get("/filmes")

    assert movies.status_code == 200


@pytest.mark.asyncio
async def test_delete_movie(movies_in_db):
    movie = movies_in_db
    movie_id = movie[2].id
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.delete(f"/filmes/{movie_id}")

    assert response.status_code == 200
