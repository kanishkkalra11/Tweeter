import socket
import time
import getpass

BUFF = 1024
PORT = 12345
HOST = socket.gethostname()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Connected \n")
i=0

while True:
    data = client_socket.recv(BUFF)
    data = data.decode('utf-8')
    print(data)
    if (data=="Thanks for using Tweeter. See you soon!"): break

    if i==0: input_ = "2"
    elif i==1: input_ = "kavivvv"
    elif i==2: input_ = "kavivvvpass"
    elif i==3: input_ = "kavivvvpass"
    elif i==4: input_ = "7"
    elif i==5: input_ = "1"
    elif i==6: input_ = "Hi i am new here!! #new #lovetweets"
    elif i==7: input_ = "0"

    
    client_socket.send(input_.encode())
    i += 1


client_socket.shutdown(2)
client_socket.close()



