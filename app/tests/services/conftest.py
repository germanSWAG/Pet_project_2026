from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import pytest_asyncio
from app.database import Base
from httpx import AsyncClient, ASGITransport
from app.services.dependencies import get_db
from app.main import app


@pytest_asyncio.fixture(scope="session")
async def db_engine():

    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")

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
async def ac(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

    trasport = ASGITransport(app=app)
    async with AsyncClient(transport=trasport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


