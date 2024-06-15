#!/usr/bin/env python3
""" Function that returns the list of school having a specific topic """
import pymongo


def schools_by_topic(mongo_collection, topic):
    """ Returns the list of school having a specific topic """
    schools = []
    
    for school in mongo_collection.find({"topics": topic}):
        schools.append(school)
    
    return schools