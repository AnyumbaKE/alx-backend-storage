#!/usr/bin/env python3
"""Module for Task 10."""


def update_topics(mongo_collection, name, topics):
    """Updates all topics of a document in the collection based on the name."""
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
