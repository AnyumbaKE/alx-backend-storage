#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable
import time
from functools import lru_cache


def track_access_count(func):
    @lru_cache(maxsize=128)
    def wrapper(url):
        # Track the number of times the URL was accessed
        count_key = f"count:{url}"

        # Increment the count for this URL
        count = int(redis_client.get(count_key) or 0) + 1
        redis_client.setex(count_key, 10, count)

        # Call the original function
        return func(url)

    return wrapper


@track_access_count
def get_page(url: str) -> str:
    # Fetch the HTML content of the URL
    response = requests.get(url)

    # Return the HTML content
    return response.text
