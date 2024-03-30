#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """

import redis
import requests
from functools import wraps

r = redis.Redis()


def count_calls(method):
    """Decorator to count the number of times a method is called.

    Args:
        method: The method to be decorated.
    """
    @wraps(method)
    def wrapper(url):
        """wrapper function"""
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        # Get new content and update cache
        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        r.expire(key, 10)
        return html_content
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
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
