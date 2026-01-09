from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
