#!/usr/bin/env python3
"""Defines a Cache class for  storing data in Redis"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any, Awaitable

redis_client = redis.Redis(host='localhost', port=6379, db=0)


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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs
    and outputs for a function using Redis.

    :param method: Callable - The method to be decorated.
    :return: Callable - The wrapped method that stores
             input/output history in Redis.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Stores input/output history in Redis
        and calls the original method.

        Create input & output list keys
        using qualified name of the method.

        :param self: Instance of the class.
        :param args: Positional arguments.
        :param kwargs: keyword arguments
        :return: Any - Result of the original method.
        """
        inputs_key = method.__qualname__ + ":inputs"
        outputs_key = method.__qualname__ + ":outputs"

        input_str = str(args)
        redis_client.rpush(inputs_key, input_str)

        output = method(self, *args, **kwargs)

        output_str = str(output)
        redis_client.rpush(outputs_key, output_str)

        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls for a particular function.

    :param method: Callable - The method to replay history for.
    :return: None
    """

    inputs_key = method.__qualname__ + ":inputs"
    outputs_key = method.__qualname__ + ":outputs"

    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    for input_data, output_data in zip(inputs, outputs):
        times_method_is_called = method.__qualname__
        data = f"(*{eval(input_data.decode())}) -> {output_data.decode()}"
        print(f"{times_method_is_called}{data}")


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
    @call_history
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
