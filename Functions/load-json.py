import pymongo
from pymongo import MongoClient
import json
import sys

def json_to_chunk(db_name, size=10000):
    with open(db_name, 'r') as f:
        batch = []
        for line in f:
            try:
                tweet = json.loads(line.strip())
                batch.append(tweet)
            except json.JSONDecodeError:
                continue
            
            if len(batch) >= size:
                yield batch
                batch = []
        if batch:
            yield batch

def initialize_db():
    if len(sys.argv) != 3:
        print("Usage: python load-json.py <json_file> <port>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    port = int(sys.argv[2])
    client = pymongo.MongoClient(f"mongodb://localhost:{port}/")
    db = client['291db']
    collection = db['tweets']
    collection.drop()
    db.create_collection('tweets')
    for batch in json_to_chunk(json_file):
        try:
            collection.insert_many(batch)
        except:
            continue

    client.close()
    
if __name__ == "__main__":
    initialize_db()