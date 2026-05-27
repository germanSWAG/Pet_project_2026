from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from app.settings.config import settings
from sqlalchemy import Integer, func
from datetime import datetime 
import re



engine = create_async_engine(settings.async_get_db_url())


async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at : Mapped[datetime] = mapped_column(server_default=func.now())
    update_at : Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        
        return F"{re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()}s"
    
