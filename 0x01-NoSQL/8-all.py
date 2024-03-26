#!/usr/bin/env python3
"""Defines a function that lists all documents in a collection"""

import pymongo


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    :param mongo_collection: name of the collection
    :return: An empty list if no document in the collection,
            otherwise the document of the collection
    """

    return [all_docs for all_docs in mongo_collection.find()]
