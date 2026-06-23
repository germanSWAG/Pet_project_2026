from sqlalchemy import select, exists, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User 
from app.models.add_cars import AdsCar
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

    async def user_exists_email(self, email : str) -> bool:
            query = select(exists().where(User.email == email))
            return await self.session.scalar(query)
    
    async def user_exists_id(self, id : int) -> bool:
            query = select(exists().where(User.id == id))
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
        
        
    async def add_token(self, token : str, id : int) -> bool:
        query = update(User).where(User.id == id).values(refresh_token=token)
        try:
            await self.session.execute(query)
            await self.session.commit()
            return True
        except Exception as e:
            logger.error(f"Ошибка при обновление токена для {id}: {e}")
            return False

    async def add_cars(self, data : list) -> bool:
        if not data:
            return False
        
        add_car = [
            AdsCar(
            platform='drom',
            brand=car['brand'],
            model=car['model'],
            price=car['price'],
            url=car['link']
            )
            for car in data
        ]
        

        if not add_car:
            return False
        
        
        try:
            async with self.session.begin():
                self.session.add_all(add_car)
            return True
    

        except Exception as e:

            logger.error(f"Ошибка при пакетном добавлении авто в БД: {e}")

            return False
       

            
        

        


