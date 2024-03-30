#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """

import redis
import requests
from functools import wraps
from typing import Callable, Any

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def count_call(method: Callable):
    """
    Decorator to track URL accesses and cache results
    with an expiration time of 10 seconds.

    :param: method (callable): The method to be decorated.
    :return: callable: The wrapped method.
    """

    @wraps(method)
    def wrapper(url) -> Any:
        """
        Wrapper function to handle caching and counting URL accesses.
        """
        cached_key = f"cached:{url}"
        count_key = f"count:{url}"

        # Check if content is cached
        cached_content = redis_client.get(cached_key)
        if cached_content:
            redis_client.incr(count_key)
            return cached_content.decode("utf-8")

        # Fetch new content and update cache
        html_content = method(url)
        redis_client.setex(cached_key, 10, html_content)
        redis_client.incr(count_key)

        return html_content

    return wrapper


@count_call
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL
    and track the number of accesses.

    :param: url(str) - The URL to retrieve HTML content from.
    :returns: str - The HTML content of the URL.
    """
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
