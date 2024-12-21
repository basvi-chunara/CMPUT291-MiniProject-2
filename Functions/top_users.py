import pprint

def get_max_user_info(users):
    user_info = {}
    for user in users:
        username = user['user']['username']
        if username not in user_info:
            user_info[username] = user['user']
        else:
            user_info[username]['followersCount'] = max(user_info[username]['followersCount'], user['user']['followersCount'])
            user_info[username]['friendsCount'] = max(user_info[username]['friendsCount'], user['user']['friendsCount'])
            user_info[username]['statusesCount'] = max(user_info[username]['statusesCount'], user['user']['statusesCount'])
            user_info[username]['favouritesCount'] = max(user_info[username]['favouritesCount'], user['user']['favouritesCount'])
            user_info[username]['listedCount'] = max(user_info[username]['listedCount'], user['user']['listedCount'])
            user_info[username]['mediaCount'] = max(user_info[username]['mediaCount'], user['user']['mediaCount'])
    return user_info
            
def list_top_users(db):
    try:
        while True: # check invalid input
            collection = db['tweets']
            try:
                n = int(input("Enter the number of top users to display(enter 0 to return to main menu): "))
                if n == 0:
                    print("Cancelling action. Returning to main menu.\n")
                    return
                if n < 0:
                    raise ValueError
            except ValueError:
                print("Invalid input. Please enter a number. \n")
                continue    
            
            # Aggregating user data
            users = list(collection.find({}, {"user": 1}))
            users_aggregated = get_max_user_info(users)
            
            sorted_users = sorted(users_aggregated.values(), key = lambda x: x['followersCount'], reverse=True)
            
            print(f"\nTop {n} users by followers count:")
            for i, user in enumerate(sorted_users[:n], start = 1):
                print(f"{i}. Username: {user['username']}, Display name: {user['displayname']}, Followers: {user['followersCount']}")
                
            selected_username = input("\nEnter a username to see the full details about that user(or press Enter to go back to the main menu): ")
            
            if selected_username == '':
                print("Going back to the main menu")
                return
            elif selected_username in users_aggregated:
                selected_user = users_aggregated[selected_username]
                print("\nFull User Information")
                pprint.pp(selected_user)
            else:
                print("Invalid username detected")
                              
    except Exception as e:
        print(f"An error occured: {e}")                