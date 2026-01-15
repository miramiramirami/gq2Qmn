from typing import Callable
import time

def dec(func: Callable):
    def wrapper():
        res = func()
        return res
    return wrapper

@dec
def my_func():
    return 100


# подсчет времени
def count_time(func: Callable):
    def wrapper():
        start = time.time()
        res = func()
        end = time.time()
        print(f'Заняло {end-start} sec')
        return res
    return wrapper

@count_time
def my_second_func():
    time.sleep(3)
    return 100


print(my_func())
print(my_second_func())