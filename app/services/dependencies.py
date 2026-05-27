from app.database import get_db
from app.repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.service_user import AuthService
from fastapi import Depends



async def get_repository(session : AsyncSession = Depends(get_db)):
    return Repository(session=session)


async def get_auth_service(repository : Repository = Depends(get_repository)):
    return AuthService(repository=repository)







