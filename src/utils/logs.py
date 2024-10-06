import functools
import logging
import time
from typing import Callable

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def func_log(message: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                formatted_message = message.format(*args, **kwargs)
            except (IndexError, KeyError) as e:
                formatted_message = (
                    f"{message} - (unable to format due to "
                    f"missing arguments: {e})"
                )

            start_time = time.time()
            logger.info(
                f"{formatted_message}... Executing '{func.__name__}'..."
            )

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in '{func.__name__}': {e}")
                raise
            else:
                end_time = time.time()
                elapsed_time = end_time - start_time
                logger.info(
                    f"{formatted_message} - DONE. '{func.__name__}' "
                    f"took {elapsed_time:.4f} seconds."
                )
                return result

        return wrapper
    return decorator
