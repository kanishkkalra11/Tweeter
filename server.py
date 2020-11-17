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
    #TODO add CLI for homepage here
    return

#client thread

def client_thread(client_socket, address):
    user = authenticate(client_socket) #TODO write code for authenticate in utils
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

    