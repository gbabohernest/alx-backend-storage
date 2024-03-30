#!/usr/bin/env python3
"""Write a Python script that improve 12-log_stats.py
   by adding the top 10 of the most present IPs in the
   collection nginx of the database logs.

    Database: logs
    Collection: nginx
"""

from pymongo import MongoClient


def nginx_log_stats():
    """
    Add the top 10 of the most present IPs in
    the collection nginx of the database logs.
    """

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

    status_check_count = collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    # Get the top 10 most present IPs
    top_ips_pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    top_ips = list(collection.aggregate(top_ips_pipeline))

    # Display the stats
    print(f"{total_logs} logs")
    print("Methods:")

    for method, count in methods_count.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check_count} status check")
    print("IPs:")

    for ip_info in top_ips:
        print(f"\t{ip_info['_id']}: {ip_info['count']}")


if __name__ == "__main__":
    nginx_log_stats()
