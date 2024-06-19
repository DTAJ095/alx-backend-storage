#!/usr/bin/env python3
""" Writing strings to redis """
import redis
from uuid import uuid4
from typing import Callable, Union, Optional
from functools import wraps


@cache_decorator
def count_calls(method: Callable) -> Callable:
    """ Count calls decorator """
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

@history_decorator
def call_history(method: Callable) -> Callable:
    """ Store the history of input and output for
    a particular function
    """ 
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


class Cache():
    """ Cache class """
    def __init__(self):
        """ Constructor method """
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @call_history    
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store method """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Optional[Callable]) -> bytes:
        """ Get method """
        data = self._redis.get(key)
        return data
    
    def get_str(self, key: str) -> str:
        """ Get str method """
        data = self._redis.get(key)
        return data.decode('utf-8')
    
    def get_int(self, key: str) -> int:
        """ Get int method """
        data = self._redis.get(key)
        return int(data)
