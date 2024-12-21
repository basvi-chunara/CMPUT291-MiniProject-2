import pymongo
from pymongo import MongoClient
from datetime import datetime

def connect_to_db(port):
    client= MongoClient(f"mongodb://localhost:{port}")
    db = client['291db']
    return db['tweets']

def compose_tweet(port):
    collection = connect_to_db(port)

    content = input("\nEnter your tweet content: ").strip()
    if not content:
        print("Tweet content cannot be empty. Try again.")
        return 

    tweet = {
        "url": None,
        "date": datetime.now().isoformat(),
        "content": content,
        "renderedContent": None,
        "id": None,
        "user": {
            "username": '291user',
            "displayname": None,
            "id": None,
            "description": None,
            "rawDescription": None,
            "descriptionUrls": None,
            "verified": None,
            "created": None,
            "followersCount": None,
            "friendsCount": None,
            "statusesCount": None,
            "favouritesCount": None,
            "listedCount": None,
            "mediaCount": None,
            "location": None,
            "protected": None,
            "linkUrl": None,
            "linkTcourl": None,
            "profileImageUrl": None,
            "profileBannerUrl": None,
            "url": None
        
        # "content" : content,
        # "date": datetime.now().isoformat(),
        # "username": "291user",
        # "retweetCount": None,
        # "likeCount":None,
        # "quoteCount":None               #other fields required or not??
        }
    }

    result = collection.insert_one(tweet)
    print(f"---------\nTweet successfully added with ID: {result.inserted_id}")