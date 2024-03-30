#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """

import requests
import redis
from functools import wraps
from typing import Callable


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """

    @wraps(method)
    def wrapper(url: str) -> str:
        redis_client = redis.Redis()
        key = f"count:{url}"
        redis_client.incr(key)
        return method(url)

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL and cache it.

    Args:
        url (str): The URL to get the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    redis_client = redis.Redis()
    cached_content = redis_client.get(url)
    if cached_content:
        return cached_content.decode()

    response = requests.get(url).text
    redis_client.setex(url, 10, response)  # Cache for 10 seconds
    return response
