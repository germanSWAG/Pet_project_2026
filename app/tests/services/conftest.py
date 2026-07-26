from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import pytest 
import pytest_asyncio
from app.database import Base
import models
from app.services.service_user import AuthService


@pytest_asyncio.fixture(scope="session")
async def db_engine():

    test_engine = create_async_engine("sqlite+aiosqlite:///:memory")

    async with test_engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

    yield test_engine

    await test_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):

    async_session = async_sessionmaker(bind=db_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture(scope="function")
async def add_user(db_session, auth : AuthService):
    pass
