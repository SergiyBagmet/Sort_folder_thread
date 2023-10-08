from functools import wraps
import time

from my_logger import MyLogger
logger = MyLogger("time").get_logger()

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"Execution time for {func.__name__}: {elapsed_time:.2f} seconds")
        return res
    return wrapper