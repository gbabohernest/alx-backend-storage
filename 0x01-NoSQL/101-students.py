#!/usr/bin/env python3
"""Write a Python function that returns all students sorted by average score:

    Prototype: def top_students(mongo_collection):
    mongo_collection will be the pymongo collection object
    The top must be ordered
    The average score must be part of each item returns with key = averageScore
"""


def top_students(mongo_collection):
    """
    Return all students sorted by average score
    :param mongo_collection: pymongo collection object
    :return: Sorted students by average score with averageScore key
    """

    pipeline = [
        {
            "$unwind": "$topics"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]

    sorted_students = mongo_collection.aggregate(pipeline)

    return sorted_students
