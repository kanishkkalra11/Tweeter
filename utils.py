#libs
BUFF = 1024 #buffer size

def register_new_user(username, password):
    #TODO add new user to database
    return

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
            
            if (1): #TODO check username exists and password matches
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
                if (1): #TODO check if username taken already
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
            register_new_user(username, password) #TODO write register_new_user function in utils
            break

        else:
            client_socket.send("Please select a valid option.")

    return username


def recent_tweets(DATABASE,username, socket_client):
#TODO
    socket_client.send(
    """
    Welcome to Mini-Face: (Reply with)
    1: Enter the Tweet ID of Tweet you want to retweet
    2: Home Page
    """.encode())
        response = socket_client.recv(1024).decode()


def pinned_tweets(DATABASE,username, socket_client):
#TODO


def followers_list(DATABASE,username,socket_client):
    # show active/online followers
    # give user a chance to delete a follower
    #TODO
    socket_client.send(
    """
    Welcome to Mini-Face: (Reply with)
    1: Do you want to delete a follower? Which one?
    2: Home Page
    """.encode())
        response = socket_client.recv(1024).decode()


def following_list(DATABASE,username,socket_client):
    # give him option to unfollow
    # list active/offline also
    #TODO
    socket_client.send(
    """
    Welcome to Mini-Face: (Reply with)
    1: Do you want to unfollow a user? Which one?
    2: Home Page
    """.encode())
        response = socket_client.recv(1024).decode()

def registered_users(DATABASE,username,socket_client):
    # allow him to follow/unfollow that user
    """
    Welcome to Mini-Face: (Reply with)
    1: Do you want to follow this user? 
    2: Do you want to unfollow this user?
    4: Do you want to view his tweets both pinned and unpinned will get displayed?
    5: Home Page
    """.encode())
        response = socket_client.recv(1024).decode()

def hashtags_and_tweets(DATABASE,username,socket_client):
    #TODO
    # Display 5 trending tweets skip one line and then display the tweets with that mentioned hashtags

def post_tweet(DATABASE,username,socket_client):
    #TODO
    # post
