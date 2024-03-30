#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """

import redis
import requests
import time
from functools import wraps
from typing import Callable, Any

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def count_call(method: Callable):
    """
    Decorator to count how many times a function is called.

    :param: method (callable): The method to be decorated.
    :return: callable: The wrapped method that increment
            the call count and returns the result of the
            original method.
    """

    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        """
        Wrapper function that increments the count for the method
        and calls the original method with the provided arguments.

        :params: *args: Positional arguments passed to the method.
                **kwargs: Keyword arguments passed to the method.

        :returns: Any: The result of the original method.
        """

        # increment the count for the URL access
        url = args[0]
        count_key = f"count:{url}"
        redis_client.incr(count_key)

        output = method(*args, **kwargs)

        return output

    return wrapper


def cache_result(method: Callable) -> Callable:
    """
    Decorator to cache the result of a function
    with an expiration time of 10 seconds.

    :param: method (callable): The method to be decorated.
    :returns: callable: The wrapped method that caches the
              result and returns it if available.
    """

    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        """
        Wrapper function that checks if the result is cached
        and returns it, otherwise, executes the original method,
        caches the result, and returns it.

        :params: *args: Positional arguments passed to the method.
                **kwargs: Keyword arguments passed to the method.

        returns: Any: The cached result or the result of the original method.
        """
        url = args[0]
        cached_content_key = f"cached_content:{url}"
        cached_content = redis_client.get(cached_content_key)

        if cached_content:
            return cached_content.decode()

        # fetch content using request
        with requests.get(url) as response:
            html_content = response.text

        # cache content with expiration time of 10s
        redis_client.setex(cached_content_key, 10, html_content)

        return html_content

    return wrapper


@count_call
@cache_result
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL
    and track the number of accesses.

    :param: url(str) - The URL to retrieve HTML content from.
    :returns: str - The HTML content of the URL.
    """
    return url
