#!/usr/bin/env python3
"""Defines a Cache class for  storing data in Redis"""


import redis
import uuid
from typing import Union


class Cache:
    """
    A simple cache class that uses Redis for storing data.
    """

    def __init__(self):
        """
        Initialize the Cache class with a Redis
        client and flush the Redis database.
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
