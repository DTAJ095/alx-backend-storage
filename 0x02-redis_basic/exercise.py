#!/usr/bin/env python3
""" Redis client module """
import redis
from uuid import uuid4
from functools import wraps
from typing import Any, Callable, Optional, Union


def count_calls(method: Callable) -> Callable:
    """ count calls """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """ Wraps called method and adds its call count redis before execution
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator for Cache class method to track args
    """

    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """ Wraps called method and tracks its passed argument by storing
            them to redis
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


def replay(func: Callable) -> None:
    """ Check redis for how many times a function was called and display:
            - How many times it was called
            - Function args and output for each call
    """
    client = redis.Redis()
    calls = client.get(func.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              client.lrange(f'{func.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               client.lrange(f'{func.__qualname__}:outputs', 0, -1)]
    print(f'{func.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{func.__qualname__}(*{input}) -> {output}')


class Cache:
    """ Caching class """
    def __init__(self) -> None:
        """ Initialize new cache object """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        """ Stores data in redis with randomly generated key """
        key = str(uuid4())
        client = self._redis
        client.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """ Gets key's value from redis and converts
            result byte  into correct data type
        """
        client = self._redis
        data = client.get(key)
        if not data:
            return
        if fn is int:
            return self.get_int(data)
        if fn is str:
            return self.get_str(data)
        if callable(fn):
            return fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        """ Converts bytes to string """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """ Converts bytes to integers """
        return int(data)
