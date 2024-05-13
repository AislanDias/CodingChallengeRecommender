import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_user_and_delete_user(users_in_db):
    user = users_in_db[0].username
    user_id = users_in_db[0].id
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/users/add", json={"username": user[0]})
    assert response.status_code == 200
    assert response.json()["username"] == user[0]

    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.delete(f"/users/{user_id}")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user(users_in_db):
    user_id = users_in_db[1].id
    updatedUser = "Jose Ferreira"
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.put(
            f"/users/{user_id}",
            json={"username": updatedUser},
        )

    assert response.status_code == 200

    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/users/{user_id}")

    assert response.json()["username"] == updatedUser


@pytest.mark.asyncio
async def test_get_user_by_id(users_in_db):
    user = users_in_db
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        userEmail = await ac.get(f"/users/{user[1].id}")

    assert userEmail.status_code == 200
    assert userEmail.json()["id"] == user[1].id


@pytest.mark.asyncio
async def test_get_users(users_in_db):
    users = users_in_db
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        users = await ac.get("/users")

    assert users.status_code == 200


@pytest.mark.asyncio
async def test_delete_user(users_in_db):
    user = users_in_db
    user_id = user[2].id
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.delete(f"/users/{user_id}")

    assert response.status_code == 200
