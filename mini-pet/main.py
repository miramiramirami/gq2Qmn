from fastapi import FastAPI, Body, Request
from gemeni_client import get_answer
from contextlib import asynccontextmanager
from db import Base, ChatReqs, engine, get_user_reqs, add_req_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title="AI", lifespan=lifespan)


@app.get('/reqs')
def get_my_reqs(request: Request):
    user_reqs = get_user_reqs(request.client.host)
    return user_reqs


@app.post('/reqs')
def send_prompt(request: Request, prompt: str = Body(embed=True)):
    answer = get_answer(prompt)
    add_req_data(request.client.host, prompt, answer)
    return {"answer": answer}