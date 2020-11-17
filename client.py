import socket
import time

host_ip = "127.0.0.1"
localport   = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host_ip,localport))

print("Connected \n")

s.send(bytes("DONE","utf-8"))

check = s.recv(16)
checkFlag = check.decode("utf-8")
if checkFlag == "Yes":
    data = s.recv(1024)
    while data:
        data = s.recv(1024)
        print(data)
        input_ = input()
        s.send(input_.encode())
        print("Your response has been sent")
else:
    print("Error")

s.shutdown(2)
print("Bbyee")
s.close()



