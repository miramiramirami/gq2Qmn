from fastapi import FastAPI
import uvicorn
import httpx
from routers.extend_api import router as apies_router
from routers.users import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(apies_router)


@app.on_event("startup")
async def startup():
    app.state.http_client = httpx.AsyncClient(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=5.0,
    )


@app.on_event("shutdown")
async def shutdown():
    await app.state.http_client.aclose()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
