from sqlalchemy import select, exists, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User 
from app.schemas.user import UserOut
import logging

logger = logging.getLogger(__name__)

class Repository:
    def __init__(self, session : AsyncSession):
        self.session = session


    async def get_user(self, email : str) -> User | None:
        query = select(User).where(email == User.email)
        result = await self.session.execute(query)
        existing_data = result.scalar_one_or_none()

        return existing_data

    async def check_user(self, email : str) -> bool:
        query = select(exists().where(User.email == email))
        return await self.session.scalar(query)
    

    async def add_user(self, user_data : dict) -> UserOut | None:
        new_user = User(**user_data)
            
        try:
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return UserOut.model_validate(new_user)
        except Exception as e:
        
            await self.session.rollback()
            logger.exception("Ошибка при добавление в базу")
            return None
        
        
    async def add_token(self, token : str, email : str) -> True | None:
        query = update(User.refresh_token).where(User.email == email)
        pass

        
