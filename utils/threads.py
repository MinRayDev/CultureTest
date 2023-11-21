import functools
import threading
from typing import Callable


def thread(daemon: bool = True) -> Callable:
    def handle(func):
        def start_thread(_thread: threading.Thread) -> threading.Thread:
            _thread.start()
            return _thread

        @functools.wraps(func)
        def wrapper(*args_, **kwargs_):
            return start_thread(threading.Thread(target=func, args=args_, kwargs=kwargs_, daemon=daemon))

        return wrapper

    return handle
