#!/usr/bin/env python3
"""Module for Task 9."""


def insert_school(mongo_collection, **kwargs):
    """Insert a new document into a collection."""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
