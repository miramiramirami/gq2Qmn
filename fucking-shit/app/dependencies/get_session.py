from app.db.database import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session