#!/usr/bin/env python3
"""Write a Python function that returns the list of
   school having a specific topic:

    Prototype: def schools_by_topic(mongo_collection, topic):
    mongo_collection will be the pymongo collection object
    topic (string) will be topic searched
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """

    :param mongo_collection: pymongo collection object
    :param topic:  Topic searched.
    :return:  list of school having a specific topic
    """

    school_list = list(mongo_collection.find({"topic": topic}))
    return school_list
