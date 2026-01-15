from typing import Callable
import time

def param_timer_dec(func: Callable):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f'Заняло - {end - start}')
        return res
    return wrapper


@param_timer_dec
def my_func(sleep: int):
    time.sleep(sleep)
    return  100


print(my_func(1))