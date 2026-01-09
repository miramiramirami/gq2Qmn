from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = create_async_engine(
    url='postgresql+asyncpg://postgres:postgres@localhost:6432/postgres',
    pool_size=20,
    max_overflow=30
)

Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)