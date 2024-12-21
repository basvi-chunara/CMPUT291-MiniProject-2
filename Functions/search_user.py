from pymongo import MongoClient
import re
import pprint
    
def keyword_preprocess(keyword):
    return r"\b" +re.escape(keyword) + r"\b"
    
def search_users(db):
    try:
        
        collection = db['tweets']
        
        keyword = input('Please enter a keyword to search (press Enter to cancel): ').strip()
        
        if keyword == '':
            print("Search cancelled\n")
            return
        
        regex_keyword = keyword_preprocess(keyword)
        # check if the keyword is in the displayname or location
        query = {
            "$or": [
                {"user.displayname": {"$regex": regex_keyword, "$options": "i"}},
                {"user.location": {"$regex": regex_keyword, "$options": "i"}}
            ]
        }
        
        query_count = collection.count_documents(query)
        if query_count == 0:
            print("No users found matching the keyword.")
            return
            
        
        user_cursor = collection.find(query)
            
        unique_users = set()
        user_map = {}
        
        for user in user_cursor:
            username = user['user']['username']
            displayname = user['user']['displayname']
            location = user['user'].get('location', 'Unknown')
            
            user_tuple = (username, displayname, location)
            
            if user_tuple not in unique_users:
                unique_users.add(user_tuple)
                user_map[username] = user
                
                # print(f'Username: {username}, Display Name: {displayname}, Location: {location}')
        for i, user in enumerate(unique_users, start = 1):
            username, displayname, location = user
            print(f"{i}. Username: {username}, Display Name: {displayname}, Location: {location}")
        
        selected_username = input("\nEnter a username to see the full details about that user(or press Enter to go back to the main menu): ")
        
        if selected_username == '':
            print("Going back to the main menu")
            return
        elif selected_username in user_map:
            selected_user = user_map[selected_username]
            print("\nFull User Information")
            pprint.pp(selected_user['user'])
        else:
            print("Invalid username detected")
        
        
    except Exception as e:
        print(f"Failed to search users: {e}")
        return[]

    
    
        