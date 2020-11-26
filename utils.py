from dataqueries import *

BUFF = 1024 #buffer size

def authenticate(db_conn, client_socket):
    #TODO login/register here
    while True:
        client_socket.send(
            """
            Please authenticate:
            1: Login
            2: Register
            """.encode()
        )
        response = client_socket.recv(BUFF).decode()

        if (response=='1'):
            #login
            client_socket.send("Username: ".encode())
            username = client_socket.recv(BUFF).decode()
            client_socket.send("Password: ".encode())
            password = client_socket.recv(BUFF).decode()
            
            if (check_user_pass(db_conn, username, password)): 
                client_socket.send("Login successful. Welcome back.")
                break
            else:
                client_socket.send("Invalid username or password.".encode())
                continue

        elif (response=='2'):
            #register
            while True:
                client_socket.send("Enter new username: ".encode())
                username = client_socket.recv(BUFF).decode()
                if (check_user_exists(db_conn, username)):
                    client_socket.send("Username not available".encode())
                    continue
                client_socket.send("Enter new password: ".encode())
                password = client_socket.recv(BUFF).decode()
                client_socket.send("Confirm new password: ".encode())
                password_confirm = client_socket.recv(BUFF).decode()
                if (password != password_confirm):
                    client_socket.send("Password does not match".encode())
                else:
                    break
            if not register_new_user(db_conn, username, password):
                client_socket.send("Registration was unsuccessful.".encode())
            break

        else:
            client_socket.send("Please select a valid option.")

    return username

def recent_tweets(client_socket):
    while(True):
        client_socket.send(
        """
        Please reply with an integer:
        1: Enter the Tweet ID of Tweet you want to retweet
        2: Home Page
        """.encode())
        response = client_socket.recv(BUFF).decode()
    return

#TODO database input for func
def pinned_tweets(client_socket):
#TODO
    return

#TODO database input for func
def followers_list(client_socket):
    # show active/online followers
    # give user a chance to delete a follower
    #TODO
    while(True):
        client_socket.send(
        """
        Please reply with an integer:
        1: Do you want to delete a follower? Which one?
        2: Home Page
        """.encode())
        response = client_socket.recv(BUFF).decode()
    return

#TODO database input for func
def following_list(client_socket):
    # give him option to unfollow
    # list active/offline also
    #TODO
    while (True):
        client_socket.send(
        """
        Please reply with an integer:
        1: Do you want to unfollow a user? Which one?
        2: Home Page
        """.encode())
        response = client_socket.recv(BUFF).decode()
    return

def follow_user(db_conn, user, client_socket, userInput):
    if add_user_to_following(db_conn, user, userInput):
        client_socket.send("You are now following {}".format(userInput).encode())
    return

def unfollow_user(db_conn, user, client_socket, userInput):
    if rem_user_from_following(db_conn, user, userInput):
        client_socket.send("You have unfollowed {}".format(userInput).encode())
    return

def remove_follower(db_conn, user, client_socket, userInput):
    if rem_user_from_followers(db_conn, user, userInput):
        client_socket.send("You have removed {} from your followers".format(userInput).encode())
    return

def display_tweets_of_user(db_conn, user, client_socket, userInput):
    tweets = get_tweets_of_user(db_conn, userInput)
    pinned_tweets = get_pinned_tweets_of_user(db_conn, userInput)
    output = f"""
        Pinned tweets of {userInput}:


        """
    for tweet in pinned_tweets:
        output += format_tweet(tweet)

    output += "Recent tweets of {}:\n\n".format(userInput)
    for tweet in tweets:
        output += format_tweet(tweet)

    client_socket.send(output.encode())
    return

def chat_with_user(db_conn, user, client_socket, userInput):
    #TODO setup 1v1 chat sessions
    return

def search_registered_users(db_conn, client_socket, user):
    client_socket.send(
    """
    Enter username: 
    """.encode())
    userInput = client_socket.recv(BUFF).decode()
    following, follower = get_follow_update(db_conn, user, userInput)
    while (True):
        if following and follower:
            client_socket.send(
            """
            Please select one:
            1: Unfollow this user
            2: Remove user from my followers
            3: Display users' tweets
            4: Chat with user
            5: Home Page
            """.encode())
            response = client_socket.recv(BUFF).decode()
            if (response==1):
                unfollow_user(db_conn, user, client_socket, userInput)
                following = False
            elif (response==2):
                remove_follower(db_conn, user, client_socket, userInput)
                follower = False
            elif (response==3):
                display_tweets_of_user(db_conn, user, client_socket, userInput)
            elif (response==4):
                chat_with_user(db_conn, user, client_socket, userInput)
            elif (response==5):
                break
            else:
                client_socket.send("Enter a valid response.".encode())
        elif follower:
            client_socket.send(
            """
            Please select one:
            1: Follow this user
            2: Remove user from my followers
            3: Display users' tweets
            4: Home Page
            """.encode())
            response = client_socket.recv(BUFF).decode()
            if (response==1):
                follow_user(db_conn, user, client_socket, userInput)
                following = True
            elif (response==2):
                remove_follower(db_conn, user, client_socket, userInput)
                follower = False
            elif (response==3):
                display_tweets_of_user(db_conn, user, client_socket, userInput)
            elif (response==4):
                break
            else:
                client_socket.send("Enter a valid response.".encode())
        elif following:
            client_socket.send(
            """
            Please select one:
            1: Unfollow this user
            2: Display users' tweets
            3: Home Page
            """.encode())
            response = client_socket.recv(BUFF).decode()
            if (response==1):
                unfollow_user(db_conn, user, client_socket, userInput)
                following = False
            elif (response==2):
                display_tweets_of_user(db_conn, user, client_socket, userInput)
            elif (response==3):
                break
            else:
                client_socket.send("Enter a valid response.".encode())
        else:
            client_socket.send(
            """
            Please select one:
            1: Follow this user
            2: Display users' tweets
            3: Home Page
            """.encode())
            response = client_socket.recv(BUFF).decode()
            if (response==1):
                follow_user(db_conn, user, client_socket, userInput)
                following = True
            elif (response==2):
                display_tweets_of_user(db_conn, user, client_socket, userInput)
            elif (response==3):
                break
            else:
                client_socket.send("Enter a valid response.".encode())

    return

def format_tweet(tweet):
    """
    tweet: [tweet_id, tweet, username, hashtags, timestamp, is_retweet, retweet_id, retweet_obj(optional)]
    returns: stringified tweet for display in CLI
    """

    display = ">> {} tweeted by {} on {}\n\t{}\n".format(tweet[0], tweet[2], tweet[4], tweet[1])
    if tweet[5]:
        #is a retweet
        display += "Retweet of {} tweeted by {}\n\t{}\n\n".format(tweet[6], tweet[7][2], tweet[7][1])
    return display



def hashtags_and_tweets(db_conn, client_socket):
    #TODO Display 5 trending tweets skip one line and then display the tweets with that mentioned hashtags
    trending = get_trending_hashtags(db_conn)
    client_socket.send(
        f"""
        TOP 5 Trending Hashtags:
        {trending[0]}
        {trending[1]}
        {trending[2]}
        {trending[3]}
        {trending[4]}

        Please enter the hashtag you want to search tweets by: (e.g. #modi)
        """.encode()
    )
    response = client_socket.recv(BUFF).decode()
    tweets = get_tweets_by_hashtag(db_conn, response[1:])
    # we will only display max 10 recent tweets of that hashtag
    output = f"""
        Recent tweets with {response}:


        """
    for tweet in tweets:
        output += format_tweet(tweet)
        
    client_socket.send(output.encode())    
    return
   
def post_tweet(client_socket):
    #TODO
    # post
    return
