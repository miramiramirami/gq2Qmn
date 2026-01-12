import uvicorn 
from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.products import Product
from contextlib import asynccontextmanager
from app.routers.products import router as products_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(products_router)


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        reload=True
    )