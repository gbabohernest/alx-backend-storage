#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """

import redis
import requests
from functools import wraps
from typing import Callable, Any

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def normalize_url(url: str) -> str:
    """
    Normalize the URL by removing trailing slashes.

    :param: url(str) The URL to normalize.
    :return: str - The normalized URL.
    """
    return url.rstrip('/')


def count_call(method: Callable):
    """
    Decorator to count how many times a
    function is called for a specific URL.

    :param: method (callable): The method to be decorated.
    :return: callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        """
        Wrapper function that increments the count
        for the method and calls the original method.

        :param: *args: Positional arguments
                **kwargs: keyword arguments
        :return: Any - The result of original method.
        """
        url = normalize_url(args[0])
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return method(*args, **kwargs)

    return wrapper


def cache_result(method: Callable) -> Callable:
    """
     Decorator to cache the result of a function
     with an expiration time of 10 seconds.

     :param: method(Callable): The method to be decorated.
     :return: callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        """
        Wrapper function that checks if the result
        is cached and returns it, otherwise, executes the
        original method, caches the result, and returns it.

        :param: *args: Positional arguments
                **kwargs: keyword arguments
        :return: Any: The cached result or the result
                of the original method.
        """
        url = normalize_url(args[0])
        cached_content_key = f"cached_content:{url}"
        cached_content = redis_client.get(cached_content_key)

        if cached_content:
            return cached_content.decode('utf-8')

        try:
            with requests.get(url) as response:
                response.raise_for_status()
                html_content = response.text
                redis_client.setex(cached_content_key, 10, html_content)
                return html_content
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return f"Error: {e}"

    return wrapper


@count_call
@cache_result
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL and track the number of accesses.
    :param: url (str): The URL to retrieve HTML content from.
    :returns: str: The HTML content of the URL.
    """
    return url
