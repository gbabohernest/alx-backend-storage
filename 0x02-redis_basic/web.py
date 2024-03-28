#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """

import redis
import requests
import time
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL
    and track the number of accesses.

    :param: url(str) - The URL to retrieve HTML content from.
    :returns: str - The HTML content of the URL.
    """

    count_key = f"count:{url}"
    current_count = redis_client.incr(count_key)

    cached_content_key = f"cached_content:{url}"
    cached_content = redis_client.get(cached_content_key)

    if cached_content:
        return cached_content.decode()

    with requests.get(url) as response:
        html_content = response.text

    redis_client.setex(cached_content_key, 10, html_content)

    return html_content
