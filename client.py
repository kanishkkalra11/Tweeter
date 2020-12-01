import socket
import time
import getpass

BUFF = 1024
PORT = 12345
HOST = socket.gethostname()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Connected \n")

while True:
    data = client_socket.recv(BUFF)
    data = data.decode('utf-8')
    print(data)
    #TODO add exit condition
    # time.sleep(0.5)
    if (data=="Password: " or data=="Enter new password: " or data == "Confirm new password: "):
        input_ = getpass.getpass(prompt="")
        client_socket.send(input_.encode())
    if (data=="Thanks for using Tweeter. See you soon!"): break
    else:    
        input_ = input()
        client_socket.send(input_.encode())


client_socket.shutdown(2)
client_socket.close()



