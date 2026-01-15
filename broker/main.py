from fastapi import FastAPI
from faststream.rabbit.fastapi import RabbitRouter


app = FastAPI()

router = RabbitRouter("amqp://guest:guest@localhost:5672/")

@router.post('/orders')
async def make_order(name: str):
    await router.broker.publish(
        f"Новый заказ: {name}",
        queue="orders"
    )
    return {"data": "ok"}


app.include_router(router)