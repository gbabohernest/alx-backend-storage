#!/usr/bin/env python3
"""Defines a Cache class for  storing data in Redis"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any, Awaitable


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.
    :param method: Callable - The method to be wrapped & counted.
    :return: Callable - The wrapped method that increments the call
             count and returns the result of the original method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Increments the count for the method and calls
        the original method with the provided arguments.
        :param self: Instance of the class.
        :param args: Positional arguments.
        :param kwargs: keyword arguments
        :return: Any - Result of the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


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

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis with a random key and return the key.

        :param data: (Union[str, bytes, int,
                        float]) - The data to be stored in Redis.
        :return: (str) - The randomly generated key used to store
                        the data in Redis.
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> (
            Union)[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the given key, optionally
        converting it using the provided function.

        :param key: (str) - The key used to retrieve data from Radis.
        :param fn: (callable, optional) - A function to convert the
                    retrieved data. Defaults to None
        :return: Union[str, bytes, int, float, None] - The retrieved data from
                  Radis, optionally converted using the callable fn.
        """

        data = self._redis.get(key)

        if data is None:
            return data

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve data from Redis as a UTF-8 string using the given key.

        :param key: (str) - The key used to retrieve data from Redis.
        :return: Union[str, None] - The retrieved data as a UTF-8 string
                or None if the key doesn't exist.
        """

        return self.get(key, fn=lambda data: data.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve data from Radis as an integer using the given key.

        :param key: (str) - The key used to retrieve data from Radis.
        :return: Union[int, None]: The retrieved data as an integer,
                or None if the key doesn't exist.
        """

        return self.get(key, fn=int)
