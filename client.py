import socket
import time

buffer_size = [1024,2048,4096,8192] 
i=1
localport   = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((s.gethostname() ,localport))

print("Connected \n")

s.send(bytes("DONE","utf-8"))

check = s.recv(16)
checkFlag = check.decode("utf-8")
if checkFlag == "Yes":
    data = s.recv(buffer_size[i])
    while data:
        data = s.recv(buffer_size[i])
        print(data)
        input_ = input()
        s.send(input_.encode())
        print("Your response has been sent")
else:
    print("Error")

s.shutdown(2)
print("Bbyee")
s.close()



