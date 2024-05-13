import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_movie_recommendations_by_user_id(ratings_in_db):
    rating = ratings_in_db
    user_id = rating[0].userId

    print("Usuário: ", user_id)
    print("Chamando a rota para predizer os filmes: /filmes/{user_id}/recomendacoes")
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/filmes/{user_id}/recomendacoes")

    # print("Resposta: ")
    # print(response.body())

    assert response.status_code == 200
