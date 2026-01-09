import uvicorn
from fastapi import FastAPI
from app.routers.extend_api import router as extend_api_router
from app.routers.users import router as users_router
from db.database import Base, engine
from app.models.users import User
import aiohttp

app = FastAPI()

app.include_router(extend_api_router)
app.include_router(users_router)

@app.on_event('startup')
async def open_session():
    app.state.session = aiohttp.ClientSession(
    timeout=aiohttp.ClientTimeout(total=5),
)

@app.on_event('shutdown')
async def close_session():
    await app.state.session.close()

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=True
    )