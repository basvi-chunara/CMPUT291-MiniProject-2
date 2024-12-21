import pymongo
from pymongo import MongoClient
import re
import pprint

def connect_to_db(port):
    client = MongoClient(f"mongodb://localhost:{port}")
    db = client['291db']
    return db['tweets']

def search_tweets(port):
    collection = connect_to_db(port)
    input_keywords = input("\nEnter keywords: ")
    
    # Split input into words and check for hashtags
    keywords = re.findall(r'\b\w+(?:\'\w+)?\b|#\w+', input_keywords)
    if not keywords:
        print("No valid keywords entered. Try again.")
        return

    # Build query
    query_parts = []
    for kw in keywords:
        if kw.startswith('#'):
            # Match exact hashtags only
            query_parts.append({"content": {"$regex": f"\\b{re.escape(kw)}\\b", "$options": "i"}})
        else:
            # Match as separate words
            query_parts.append({"content": {"$regex": f"\\b{re.escape(kw)}\\b", "$options": "i"}})
    
    query = {"$and": query_parts}
    results = collection.find(query, {"id": 1, "date": 1, "content": 1, "user.username": 1})
    tweets = list(results)

    if not tweets:
        print("No matching tweets found.")
        return

    print("\nMatching tweets:")
    for idx, tweet in enumerate(tweets, start=1):
        username = tweet.get('user', {}).get('username', 'Unknown')
        print(f"{idx}. ID: {tweet['id']}, Date: {tweet['date']}, User: {username}")
        print(f" Content: {tweet['content']}\n")
    
    while True:
        try:
            selection = int(input("Enter the number of the tweet to view full details (0 to return): "))
            if selection == 0:
                print("Going back to the main menu")
                break
            elif 1 <= selection <= len(tweets):
                print("\nFull details of the selected tweet:")
                full_tweet = collection.find_one({"id": tweets[selection - 1]['id']})
                if full_tweet:
                    pprint.pprint(full_tweet)  
                else:
                    print("No details found for the selected tweet.")
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")
