from dataqueries import *

BUFF = 1024 #buffer size

def authenticate(client_socket):
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
            
            if (check_user_pass(username, password)): 
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
                if (check_user_exists(username)):
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
            register_new_user(username, password)
            break

        else:
            client_socket.send("Please select a valid option.")

    return username

#TODO database input for func
def recent_tweets(client_socket):
#TODO
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

def follow_user(client_socket, username):
    return

def unfollow_user(client_socket, username):
    return

def remove_follower(client_socket, username):
    return

def display_tweets_of_user(client_socket, username):
    return

def chat_with_user(client_socket, username):
    return

def search_registered_users(client_socket):
    client_socket.send(
    """
    Enter username: 
    """.encode())
    username = client_socket.recv(BUFF).decode()
    while (True):
        client_socket.send(
        """
        Please select one:
        1: Follow this user 
        2: Unfollow this user
        3: Remove user from my followers
        4: Display users' tweets
        5: Chat with user
        6: Home Page
        """.encode())
        response = client_socket.recv(BUFF).decode()
        if (response==1):
            follow_user(client_socket, username)
        elif (response==2):
            unfollow_user(client_socket, username)
        elif (response==3):
            remove_follower(client_socket, username)
        elif (response==4):
            display_tweets_of_user(client_socket, username)
        elif (response==5):
            chat_with_user(client_socket, username)
        elif (response==6):
            break
        else:
            client_socket.send("Enter a valid response.".encode())
    return
  
def hashtags_and_tweets(client_socket):
    #TODO Display 5 trending tweets skip one line and then display the tweets with that mentioned hashtags
    trending = get_trending_hashtags()
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
    tweets = get_tweets_by_hashtag(response)
    # we will only display max 10 recent tweets of that hashtag
    output = f"""
        Recent tweets with {response}:
    
        """
    for tweet in tweets:
        output += ">> " + tweet + "\n"
    client_socket.send(output.encode())    
    return
   
def post_tweet(client_socket):
    #TODO
    # post
    return
