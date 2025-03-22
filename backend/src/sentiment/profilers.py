from time import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


def async_profiler(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        start = time()
        result = await f(*args, **kwargs)
        logger.info(f"{f.__name__} took {time()- start} seconds.")
        return result

    return wrapper


def sync_profiler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        logger.info(f"{f.__name__} took {time()- start} seconds.")
        return result

    return wrapper
