from fastapi import FastAPI
import uvicorn
import aiohttp
from routers.api import router as api_router

app = FastAPI()

app.include_router(api_router)

@app.on_event('startup')
async def startup():
    app.state.session = aiohttp.ClientSession()


@app.on_event('shutdown')
async def shutdown():
    app.state.session.close()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=True
    )