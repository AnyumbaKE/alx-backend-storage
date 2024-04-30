#!/usr/bin/env python3
"""Module for Task 14."""


def top_students(mongo_collection):
    """Returns all students in a collection sorted by average score."""
    students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': '$topics.score'
                    },
                    'topics': 1
                }
            },
            {
                '$sort': {'averageScore': -1}
            }
        ]
    )
    return students
