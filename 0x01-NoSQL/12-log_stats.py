#!/usr/bin/env python3
""" Script that provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient



if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    
    logs_count = nginx_collection.count_documents({})
    print(f"{logs_count} logs")
    print("Methods:")
    
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")
    
    get_check = nginx_collection.count_documents({
        "method": "GET", "path": "/status"
    })
    print(f"{get_check} status check")