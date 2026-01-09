from database.core import Base, engine
import asyncio
import models.users


async def db_init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(db_init())
