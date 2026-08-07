# import pytest 
# from app.services.service_user import *
# from app.schemas.dto import RegisterDTO


# async def test_registration_user():
#     user = RegisterDTO(username="Ivan", email="ivan_2004@bk.ru", password="12DF3gf35675")
#     assert test_registration_user(user) == {}

#     pass

import pytest
import pytest_asyncio
from app.schemas.dto import RegisterDTO
from app.schemas.user import UserOut
from app.services.service_user import AuthService
from app.repository import Repository

@pytest_asyncio.fixture(scope="function")
async def auth_user(db_session):
    repository = Repository(db_session)
    return AuthService(repository=repository)

@pytest.mark.asyncio
async def test_add_user(auth_user : AuthService):
    register_data = RegisterDTO(username="Алексей", email="alexey256@bk.ru", password="password1234A")
    data = await auth_user.registration(register_data)
    assert data == UserOut(id=1, username="Алексей", email = "alexey256@bk.ru")

@pytest.mark.asyncio
async def test_add_exists_user(auth_user : AuthService):
    register_data = RegisterDTO(username="Алексей", email="alexey256@bk.ru", password="password1234A")
    data = await auth_user.registration(register_data)
    assert data == UserOut(id="1", username=234, email = "alexey256@bk.ru")

