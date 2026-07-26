import pytest 
from app.services.service_user import *
from app.schemas.dto import RegisterDTO


async def test_registration_user():
    user = RegisterDTO(username="Ivan", email="ivan_2004@bk.ru", password="12DF3gf35675")

    pass