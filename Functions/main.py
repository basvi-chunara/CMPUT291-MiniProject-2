import pymongo
from pymongo import MongoClient
import json
import sys
from list_top_tweets import tweet_fields
from search_user import search_users
from search_tweets import search_tweets
from compose_tweet import compose_tweet
from top_users import list_top_users

def menu_display():
    """Display the operations menu."""
    print("\nSelect an operation:")
    print("1. Search for tweets")
    print("2. Search for user")
    print("3. List tweets")
    print("4. List top users")
    print("5. Compose a tweet")
    print("6. Exit")
    

def connect_to_database(port_number):
    '''Function to connect to a mongoDB database given a port number.
    If the user enters an incorrect commandline input, output instructions.'''
    try:
        client = MongoClient(f'mongodb://localhost:{port_number}/')
        db = client["291db"]
        return db
    except Exception as e:
        print(f"Error connecting: {e}")
        return None
    
def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <mongodb_port_number>")
        sys.exit(1)
        
    port_number = int(sys.argv[1])
    db = connect_to_database(port_number)
    
    while True:
        menu_display()
        choice = input("Enter your choice: ")
        if choice == "1":
            search_tweets(port_number)

        elif choice == "2":
            search_users(db)
        elif choice == "3":
            tweet_fields(port_number)
        elif choice == "4":
            list_top_users(db)
        elif choice == '5':
            compose_tweet(port_number)
        elif choice == '6':
            print("Exiting program")
            break
        else:
            print("Invalid choice. Please try again.")       
        

if __name__ == "__main__":
    main()