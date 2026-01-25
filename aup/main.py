from fastapi import FastAPI
import aiohttp
from app.router import api_router


app = FastAPI()

app.include_router(api_router)

@app.on_event('startup')
async def startup():
    app.state.client_session = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=5)
    )


@app.on_event('shutdown')
async def shutdown():
    await app.state.client_session.close()