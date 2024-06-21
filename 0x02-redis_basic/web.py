#!/usr/bin/env python3
""" Implement a get_page function """
import requests
import redis
from functools import wraps
from typing import Dict
import time

cache: Dict[str, str] = {}


def cache_with_expiration(expiration: int):
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            url = args[0]
            key = f"count:{url}"
            if key in cache:
                count, timestamp = cache[key]
                if time.time() - timestamp > expiration:
                    result = method(*args, **kwargs)
                    cache[key] = (count+1, time.time())
                    return result
                else:
                    cache[key] = (count+1, timestamp)
                    return


def get_page(url: str) -> str:
    """ Implementing get_page function """
    if url in cache:
        print(f"Retrieving from cache: {url}")
        return cache[url]
    else:
        print(f"Retrieving from the internet: {url}")
        response = requests.get(url)
        cache[url] = response.text
        return response.text


# def track_get_page(method: Callable) -> Callable:
#     """ get_page decorator """

#     @wraps(method)
#     def wrapper(url: str) -> str:
#         """ wrapper function """
#         redis.Redis().incr(f'count:{url}')
#         cached_page = redis.Redis().get(f'cached_page:{url}')
#         if cached_page:
#             return cached_page.decode('utf-8')
#         response = method(url)
#         redis.Redis().set(f'count:{url}', 0)
#         redis.Redis().setex(f'cached_page:{url}', response, 10)
#         return response
#     return wrapper


# @track_get_page
# def get_page(url: str) -> str:
#     """ Implementing get_page function """
#     response = requests.get(url)
#     return response.text
