#!/usr/bin/env python3
""" Implement a get_page function """
import requests
import redis
from functools import wraps
from typing import Callable


def track_get_page(func: Callable) -> Callable:
    """ get_page decorator """

    @wraps(func)
    def wrapper(url: str) -> str:
        """ wrapper function """
        redis.Redis().incr(f'count:{url}')
        cached_page = redis.Redis().get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        response = func(url)
        redis.Redis().set(f'{url}', response, 10)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """ Implementing get_page function """
    response = requests.get(url)
    return response.text
