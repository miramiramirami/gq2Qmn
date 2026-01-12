from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import pool

Base = declarative_base()

DB_URL = 'postgresql+asyncpg://postgres:postgres@localhost:6432/postgres'

engine = create_async_engine(
    DB_URL,
    poolclass=pool.NullPool
)

Session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)