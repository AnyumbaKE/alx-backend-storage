#!/usr/bin/env python3
"""Module for Task 8.
"""


def list_all(mongo_collection):
    """List all documents in a collection.
    """
    return list(mongo_collection.find())
