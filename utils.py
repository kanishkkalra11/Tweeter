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

def news_feed(db_conn, client_socket, user):
    feed = get_news_feed(db_conn, user) #TODO match with func in dataqueries
    output = "Your News Feed:\n"
    for tweet in feed:
        output += format_tweet(tweet)
    return

def pinned_tweets_list(db_conn, client_socket, user):
    pinned_tweets = get_pinned_tweets_of_user(db_conn, user) #TODO match func in dataqueries
    output = f"""
        Your pinned tweets:


        """
    for tweet in pinned_tweets:
        output += format_tweet(tweet)
    client_socket.send(output.encode())
    return

def followers_list(db_conn, client_socket, user):
    # show active/online followers
    # give user a chance to delete a follower
    online_followers, other_followers = get_followers_list(db_conn, user) #TODO match with func in dataqueries
    online_output=""
    for f in online_followers:
        online_output += ">> " + f + "\n"
    for f in other_followers:
        others_output += ">> " + f + "\n"
    output = "Online Followers:\n{}Other Followers{}".format(online_output, others_output)
    client_socket.send(output.encode())
    return

def following_list(db_conn, client_socket, user):
    # give him option to unfollow
    # list active/offline also
    online_following, other_following = get_following_list(db_conn, user) #TODO match with func in dataqueries
    online_output=""
    for f in online_following:
        online_output += ">> " + f + "\n"
    for f in other_following:
        others_output += ">> " + f + "\n"
    output = "Online Following:\n{}Other Following{}".format(online_output, others_output)
    client_socket.send(output.encode())
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
   
def make_new_tweet(db_conn, client_socket, user):
    client_socket.send("Enter the tweet: ".encode())
    tweet_text = client_socket.recv(BUFF).decode()
    if post_new_tweet(db_conn, user, tweet_text, None): #TODO match with func in dataqueries
        client_socket.send("Your tweet has been posted.".encode())
    return

def retweet(db_conn, client_socket, user):
    client_socket.send("Enter the tweet ID that you want to retweet: ".encode())
    retweet_id = int(client_socket.recv(BUFF).decode())

    retweet_text = format_tweet(get_tweet_by_id(db_conn, retweet_id)) #TODO match with func in dataqueries
    retweet_output = "You are retweeting:\n{}".format(retweet_text)
    client_socket.send(retweet_output.encode())

    client_socket.send("Enter the tweet: ".encode())
    tweet_text = client_socket.recv(BUFF).decode()
    if post_new_tweet(db_conn, user, tweet_text, retweet_id): #TODO match with func in dataqueries
        client_socket.send("Your retweet has been posted.".encode())
    return

def post_tweet(db_conn, client_socket, user):
    client_socket.send(
        f"""
        Please select an option:
        1: Write a new tweet
        2: Retweet an existing tweet
        3: Homepage
        """
    )
    response = client_socket.recv(BUFF).decode()
    if response==1:
        make_new_tweet(db_conn, client_socket, user)
    elif response==2:
        retweet(db_conn, client_socket, user)
    elif response==3:
        return
    else:
        client_socket.send("Enter a valid response.".encode())
    return
