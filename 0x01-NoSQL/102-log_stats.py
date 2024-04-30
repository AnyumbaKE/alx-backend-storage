#!/usr/bin/env python3
"""Module for Task 15."""
from pymongo import MongoClient

def print_nginx_request_logs(nginx_collection):
    """Print statistics about Nginx request logs."""
    print(f'{nginx_collection.count_documents({})} logs')
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {req_count}')
    status_checks_count = nginx_collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f'{status_checks_count} status check')

def print_top_ips(server_collection):
    """Print statistics about the top 10 HTTP IPs in a collection."""
    print('IPs:')
    request_logs = server_collection.aggregate([
        {'$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}},
        {'$sort': {'totalRequests': -1}},
        {'$limit': 10}
    ])
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        print(f'\t{ip}: {ip_requests_count}')

def run():
    """Provide some statistics about Nginx logs stored in MongoDB."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)
    print_top_ips(client.logs.nginx)

if __name__ == '__main__':
    run()
