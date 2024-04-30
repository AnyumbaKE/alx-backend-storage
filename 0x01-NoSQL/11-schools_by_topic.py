#!/usr/bin/env python3
"""Module for Task 11."""


def schools_by_topic(mongo_collection, topic):
    """Return the list of schools that include a specific topic."""
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic
            }
        }
    }
    return [school for school in mongo_collection.find(topic_filter)]
