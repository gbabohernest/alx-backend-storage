#!usr/bin/env python3
"""Write a Python script that provides some stats about
   Nginx logs stored in MongoDB:

    Database: logs
    Collection: nginx
"""

from pymongo import MongoClient


def nginx_log_stats():
    """Provides some stats about Nginx logs stored in MongoDB"""

    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})

    methods_count = {
        "GET": collection.count_documents({"method": "GET"}),
        "POST": collection.count_documents({"method": "POST"}),
        "PUT": collection.count_documents({"method": "PUT"}),
        "PATCH": collection.count_documents({"method": "PATCH"}),
        "DELETE": collection.count_documents({"method": "DELETE"})
    }

    status_check_count = collection.count_documents({"method": "GET",
                                                     "path": "/status"})

    print(f"{total_logs} logs")
    print("Methods")

    for method, count in methods_count.items():
        print(f"\tmethod {method}: {count}")

    print(f"{status_check_count} status check")


if __name__ == "__main__":
    nginx_log_stats()
