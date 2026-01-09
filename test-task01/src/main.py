from fastapi import FastAPI, Body, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
import uvicorn
from src.db import engine, Base, Session
from src.model import ShortURL
from src.service import ShortenerService
from src.exceptions import NoLongUrlFoundError
from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession

async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session


@app.post('/short')
async def generate_slug(
    long_url: Annotated[str, Body(embed=True)],
    session: AsyncSession = Depends(get_session)
):
    slug = await ShortenerService.generate_short_url(long_url, session)
    return {"new_slug": slug}


@app.get('/{slug}')
async def redirect(
    slug: str,
    session: AsyncSession = Depends(get_session)
):
    try:
        long_url = await ShortenerService.get_url_by_slug(slug, session)

    except NoLongUrlFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Url не существует"
        )
    
    if not long_url.startswith(("http://", "https://")):
        long_url = "http://" + long_url
    
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)


if __name__ == '__main__':
    uvicorn.run(
        'src.main:app',
        port=9999,
        reload=True,
    )