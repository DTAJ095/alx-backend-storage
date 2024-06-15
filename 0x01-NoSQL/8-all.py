#!/usr/bin/env python3
""" Function that list all documents in a collection """
import pymongo


def list_all(mongo_collection) -> list:
    """ Return a list of all documents in a collection """
    documents = []
    for doc in mongo_collection.find():
        documents.append(doc)
    return documents
