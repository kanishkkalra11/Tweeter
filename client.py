import socket
import time

buffer_size = [1024,2048,4096,8192] 
i=1
localport   = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((client_socket.gethostname() ,localport))

print("Connected \n")

client_socket.send(bytes("DONE","utf-8"))

check = client_socket.recv(16)
checkFlag = check.decode("utf-8")
if checkFlag == "Yes":
    data = client_socket.recv(buffer_size[i])
    while data:
        data = client_socket.recv(buffer_size[i])
        print(data)
        input_ = input()
        client_socket.send(input_.encode())
        print("Your response has been sent")
else:
    print("Error")

client_socket.shutdown(2)
print("Bbyee")
client_socket.close()



