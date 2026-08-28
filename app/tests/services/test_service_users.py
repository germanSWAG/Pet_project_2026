# import pytest 
# from app.services.service_user import *
# from app.schemas.dto import RegisterDTO


# async def test_registration_user():
#     user = RegisterDTO(username="Ivan", email="ivan_2004@bk.ru", password="12DF3gf35675")
#     assert test_registration_user(user) == {}

#     pass

import pytest
from app.schemas.user import UserOut
from app.services.service_user import AuthService
from app.repository import Repository
from httpx import AsyncClient

pytestmark = pytest.mark.anyio

@pytest.fixture(scope="function")
async def auth_user(db_session):
    repository = Repository(db_session)
    return AuthService(repository=repository)



async def test_endpoint_registration_success(ac : AsyncClient):
    payload = {
        "username" : "Алексей",
        "email" : "alexey256@bk.ru",
        "password" : "Password12345"
    }

    response = await ac.post("/users/register", json=payload)

    assert response.status_code == 200

    data = UserOut.model_validate(response.json())
    assert data.username == "Алексей"
    assert data.email == "alexey256@bk.ru"
    assert data.id is not None

    assert "refresh_token" in response.cookies