import asyncio
from typing import Callable, Awaitable, Any


def dec(func: Callable[..., Awaitable[Any]]):
    async def wrapper(*args, **kwargs):
        res = await func(*args, **kwargs)
        return res
    return wrapper


@dec
async def my_async(sleep: int):
    await asyncio.sleep(sleep)
    return 1

print(asyncio.run(my_async(4)))
