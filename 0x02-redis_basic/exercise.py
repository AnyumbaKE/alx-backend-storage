#!/usr/bin/env python3
'''A module for utilizing Redis NoSQL data storage.
'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union


def count_calls(method: Callable) -> Callable:
    '''Records the number of times a method in a Cache class is called.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Increments the call counter before invoking the method.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''Stores the call history of a method in a Cache class.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Stores method's inputs and outputs before returning its result.
        '''
        input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, result)
        return result
    return wrapper


def replay(fn: Callable) -> None:
    '''Replays the call history of a method from a Cache class.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_instance = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_instance, redis.Redis):
        return
    method_name = fn.__qualname__
    input_key = '{}:inputs'.format(method_name)
    output_key = '{}:outputs'.format(method_name)
    method_calls = 0
    if redis_instance.exists(method_name) != 0:
        method_calls = int(redis_instance.get(method_name))
    print('{} was called {} times:'.format(method_name, method_calls))
    method_inputs = redis_instance.lrange(input_key, 0, -1)
    method_outputs
