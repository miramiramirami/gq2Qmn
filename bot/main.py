import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from faststream.rabbit import RabbitBroker

TOKEN = "8410187785:AAH1qDmq3XBsu8j5Fy84qYGAnQvHB92ek_s"

dp = Dispatcher()

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")

bot = Bot(TOKEN)

@broker.subscriber("orders")
async def handle_orders(data: str):
    await bot.send_message(
        chat_id = 1197282533,
        text = data
    )

@dp.message()
async def handle_message(msg: Message):
    await msg.answer(f"Ваш chat id: {msg.chat.id}")


async def main() -> None:
    async with broker:
        await broker.start()
        logging.info("Старт брокера")
        await dp.start_polling(bot)
    logging.info("Брокер остановился")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())