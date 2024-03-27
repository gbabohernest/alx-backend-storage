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

    students = mongo_collection.find({})

    for student in students:
        if "score" in students:
            total_score = sum(student["score"])
            num_scores = len(student["score"])
            average_score = total_score / num_scores if num_scores > 0 else 0
            student["averageScore"] = average_score

    sorted_students = sorted(students,
                             key=lambda x: x.get["averageScore"], reverse=True)

    return sorted_students
