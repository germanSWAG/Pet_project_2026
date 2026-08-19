from sqlalchemy import select, exists, update, func, insert
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from app.models.user import User 
from app.models.products import Product
from app.models.basket import Basket
from app.schemas.user import UserOut
import logging

logger = logging.getLogger(__name__)

class Repository:
    def __init__(self, session : AsyncSession):
        self.session = session


    async def get_user(self, email : str) -> User | None:
        query = select(User).where(email == User.email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def commit(self,) -> None:
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            logger.exception("Проблема при фиксирование изменений")
            raise


    async def rollback(self,) -> None:
        await self.session.rollback()
        return None

    
    async def user_exists_email(self, email : str) -> bool:
            query = select(exists().where(User.email == email))
            return await self.session.scalar(query)
    
    async def user_exists_id(self, id : int) -> bool:
            query = select(exists().where(User.id == id))
            return await self.session.scalar(query)

    async def add_user_for_db(self, user_data : dict) -> User:
        new_user = User(**user_data)
            
        self.session.add(new_user)
        await self.session.flush()
        return new_user
       
        
        
    async def update_token(self, token : str, id : int) -> None:
        query = update(User).where(User.id == id).values(refresh_token=token)
        await self.session.execute(query)

    
    async def user_refresh(self, refresh_token : str) -> int | None:
        query = select(User.id).where(User.refresh_token == refresh_token).with_for_update()
        return await self.session.scalar(query)


    async def delete_refresh_db(self, id : int) -> None:
        query = update(User).where(User.id == id).values(refresh_token=None)
        
        await self.session.execute(query)
        await self.session.commit()
    
    
    async def add_product_db(self, data : dict) -> dict | None:
        new_product = Product(**data)
        
        try:
            self.session.add(new_product)
            await self.session.commit()
            await self.session.refresh(new_product)
            return data
        

        except Exception as e:
            logger.error(f"Ошибка при добавление нового товара в БД: {e}")
            return None

    
    async def get_product_db(self, id : int):
        query = select(Product).where(Product.id == id)
        result = await self.session.execute(query)
        return result.scalar()



    async def get_all_products_db(self, offset : int, page_size : int) -> dict:
        stmt = select(Product).order_by(Product.id).offset(
            offset).limit(page_size)
        
        try:
            result = await self.session.scalars(stmt)
            total = await self.session.scalar(select(func.count()).select_from(Product))

        except Exception as e:
            logger.error(f"Ошибка при получение всех данных о товаре. Traceback - {e}")
            return None
        return {"total" : total, "items" : result.all()}



    async def add_basket(self, user_id: int,
                        product_id: int,
                        count : int) -> Basket | None:
        if count <=0:
            raise ValueError("count должен быть положительным")
        
        stmt = insert(Basket).values(user_id=user_id,
                                    product_id=product_id, 
                                    quantity=count
                                    )
        stmt = stmt.on_conflict_do_update(
                                    constraint="idx_user_id_product_id",
                                    set_= {"quantity": Basket.quantity + stmt.excluded.quantity},
                                    ).returning(Basket)
        

        try:

            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except Exception:
            await self.session.rollback()
            logger.exception(f'Ошибка при работе с базой. \n'
                             f'Функция - {self.add_basket.__name__} \n'
                            )
            return None
        
            
            

    async def get_basket_db(self, user_id : int) -> list[Basket] | None:
        stmt = select(Basket).where(
            Basket.user_id == user_id
            ).options(
            joinedload(
            Basket.product
        ))

        try:
            result = await self.session.execute(stmt)
            items = result.scalars().all()
            return items

        except Exception:
            logger.exception(f'Ошибка при работе с базой. \n'
                         f'Функция - {self.get_basket_db.__name__}')
            return None



        


