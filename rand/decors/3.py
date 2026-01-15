from typing import Callable
import time

def limit_calls(limit: int):
    def wrapper(func: Callable):
        def inner(*args, **kwargs):
            nonlocal limit
            if limit == 0:
                print('Нельзя вызвать функция')
                return

            res = func(*args, **kwargs)
            limit -= 1
            return res
        return inner
    return wrapper


@limit_calls(2)
def my_func(sleep: int):
    time.sleep(sleep)
    return  100


print(my_func(1))