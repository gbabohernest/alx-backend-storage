#!/usr/bin/env python3
"""Write a Python function that inserts a new document in a
   collection based on kwargs:

    Prototype: def insert_school(mongo_collection, **kwargs):
    mongo_collection will be the pymongo collection object
    Returns the new _id
"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection
    based on kwargs
    :param mongo_collection: collection name
    :param kwargs: dictionary to insert
    :return: The id of the document
    """

    document_id = mongo_collection.insert_one(kwargs).inserted_id
    return document_id
