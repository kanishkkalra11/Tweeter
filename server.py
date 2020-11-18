import socket
import time
import _thread
from utils import *
import mysql.connector
from mysql.connector import Error

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#server configurations
server_ip = socket.gethostname()
server_port = 12345
MAX_USERS = 32

# import databases
pw = "password"
connection = create_db_connection("localhost", "root", pw, "Tweeter")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

#CLI
def home_page(username, client_socket):
    while(True):
        client_socket.send(
"""
Hi!!!!!
Options: (Reply with)
1: News feed (Recent Tweets/Updates)
2: Your Pinned Tweets
3: Followers List
4: Following List
5: Search a registered user 
6: View Tweets by hashtags (Top 5 trending will be shown)
7: Post a Tweet
0: Logout
""".encode())
        option = client_socket.recv(1024).decode()
        if(option == "1"):
            recent_tweets( ,username, client_socket) 
        # Display another menu (Enter the tweet ID of the tweet to Retweet) to user when he chooses option 1
        
        elif(option == "2"):
            pinned_tweets( ,username, client_socket) 
        
        elif(option == "3"):
            followers_list( ,username,client_socket)
            # show active/online followers
            # give user a chance to delete a follower

        elif(option == "4"):
            following_list( ,username,client_socket)
            # give him option to unfollow

        elif(option == "5"):
            registered_users( ,username,client_socket)
            # allow him to follow/unfollow that user

        elif(option == "6"):
            hashtags_and_tweets( ,username,client_socket)
        
        elif(option == "7"):
            post_tweet( ,username,client_socket)
            
        elif(option == "0"):
            return
        
        else:
            client_socket.send("Invalid Option!".encode())
    return
    

#client thread

def client_thread(client_socket, address):
    user = authenticate(client_socket) #TODO write code for authenticate in utils
    #TODO mark user as online
    QUERY = ""
    execute_query(connection, QUERY)
    home_page(user, client_socket) #TODO write code for home_page 
    #TODO mark user as offline
    print(f"Closing client thread: {address}")
    client_socket.send("Thanks for using Tweeter. See you soon!")
    client_socket.shutdown(2)
    client_socket.close()
    return

#create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(MAX_USERS)

print("Server started and listening...")

while True:
    client_socket, address = server_socket.accept()
    print(f"New client connected: {address}")

    _thread.start_new_thread(client_thread, (client_socket, address))

    
