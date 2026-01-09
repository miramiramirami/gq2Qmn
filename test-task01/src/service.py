from src.model import ShortURL
from src.generate_slug import generate_slug
from sqlalchemy import select
from src.exceptions import NoLongUrlFoundError
from sqlalchemy.ext.asyncio import AsyncSession

class ShortenerService:
    @staticmethod
    async def generate_short_url(
        long_url: str,
        session: AsyncSession,
    ) -> str:
        # async with session() as session:
        #     while True: 
        #         generated_slug = generate_slug()
        #         res = await session.execute(select(ShortURL).where(ShortURL.slug == generated_slug))
        #         if not res.scalar_one_or_none():
        #             break

        generated_slug = generate_slug()

        slug = ShortURL( 
            slug=generated_slug,
            long_url=long_url
        )

        session.add(slug)
        await session.commit()

        return slug.slug
    

    @staticmethod
    async def get_url_by_slug(slug: str, session: AsyncSession) -> str:
        # async with Session() as session:
        result = await session.execute(select(ShortURL).filter_by(slug=slug))
        data: ShortURL | None = result.scalar_one_or_none()

        if not data:
            raise NoLongUrlFoundError()

        return data.long_url 
        




