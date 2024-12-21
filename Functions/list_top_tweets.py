from pymongo import MongoClient
import json
from bson import json_util

def connect_to_db(port):
    client= MongoClient(f"mongodb://localhost:{port}")
    db = client['291db']
    return db['tweets']

def tweet_fields(port):
    collection = connect_to_db(port)
    field_dict = {1: 'retweetCount', 2: 'likeCount', 3: 'quoteCount'}
    while True: # check for valid input
        print("\nSearch for a tweet by top:")
        print("1. Retweets")
        print("2. Likes")
        print("3. Quotes")
        print("4. Go back")
        try: 
            field = int(input("Choice: "))
            if (field in field_dict.keys()):
                break
            elif field == 4:
                return
            else:
                raise Exception
        except:
            print("Invalid command.")
    
    while True:
        try:
            n = int(input("Enter the number of tweets you want to see: "))
            if n <= 0:
                raise Exception
            break
        except:
            print("Please enter a valid integer greater than 0.")

    tweets = collection.find({}).sort({field_dict[field]:-1}).limit(n) # get the top tweets based on field

    print(f"\nTop {n} tweets based on {field_dict[field][:-5]}s:")
    i = 1
    tweets_list = []
    for t in tweets: # print relevant information
        tweets_list.append(t)
        print(f"\n{i}. Tweet ID: {t['id']}")
        print(f"{t['user']['username']} tweeted")
        print(f"{t['content']}")
        print(f"On {t['date']}")
        print(f"{field_dict[field][:-5].title()}s: {t[field_dict[field]]}")
        i += 1
    
    while True:
        command = input("Choose a tweet to see all fields or enter \"back\" to go back to the main menu:\n")
        if command.strip() == "back":
            return
        try: # if user wants to see all fields of the tweet
            idx = int(command.strip())
            if (1 <= idx <= len(tweets_list)):
                t = tweets_list[idx - 1]
                print("\nFull details of selected tweet:")
                full_tweet = collection.find_one({"id": t['id']})
                print(json.dumps(full_tweet, indent=4, default=json_util.default))
            else:
                raise Exception
            
        except:
            print("Invalid command")