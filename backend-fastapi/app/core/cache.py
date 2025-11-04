import time
import inspect
from typing import Any, Callable, Dict, Tuple
from functools import wraps

class SimpleCache:
    def __init__(self):
        self._store: Dict[str, Tuple[Any, float]] = {}

    def set(self, key: str, value: Any, ttl: int = 60):
        """
        Set a value in the cache with a time-to-live (ttl) in seconds.
        """
        expire_time = time.time() + ttl
        self._store[key] = (value, expire_time)

    def get(self, key: str):
        """
        Get a value from the cache. Returns None if not found or expired.
        """
        item = self._store.get(key)
        if not item:
            return None
        value, expire = item
        if time.time() > expire:
            del self._store[key]
            return None
        return value

    def clear(self):
        self._store.clear()


cache = SimpleCache()


def cached(ttl: int = 60):
    """
    Async-aware caching decorator — supports both async and sync functions.
    """
    def decorator(func: Callable):
        is_async = inspect.iscoroutinefunction(func)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            result = cache.get(key)
            if result is not None:
                print(f"[CACHE HIT] {key}")
                return result

            print(f"[CACHE MISS] {key}")
            result = await func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            result = cache.get(key)
            if result is not None:
                print(f"[CACHE HIT] {key}")
                return result

            print(f"[CACHE MISS] {key}")
            result = func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result

        return async_wrapper if is_async else sync_wrapper

    return decorator
