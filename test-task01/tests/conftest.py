from src.main import app, get_session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
import pytest
import httpx
from src.db import Base

engine = create_async_engine(
    url='sqlite+aiosqlite:///./test.db'
)

Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        from src.model import ShortURL
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(scope='function')
async def session():
    async with Session() as session:
        yield session


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as ac:
        yield ac
