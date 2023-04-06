# Client code
# Import socket module
import socket			
import sys

if len(sys.argv) == 3:
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    sys.exit("Format: python client.py <ip address> <port>")

# Create a TCP socket object
clientSock = socket.socket()		
			
# connect to the server on local computer
clientSock.connect((ip, port))

# receive data from the server and decoding to get the string.
print (clientSock.recv(1024).decode())
# close the connection

# def create_data_socket():
#     # ephemeral_port = int(client.recv(1024).decode())
#     data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # Bind the socket to port 0 (ephemeral port)
#     data_socket.bind(('', 0))

#     return data_socket

def recvAll(sock, numBytes):
    recvBuff = b''
    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes - len(recvBuff))
        if not tmpBuff:
            break
        recvBuff += tmpBuff
    return recvBuff
        
        
while True:
    # send a thank you message to the client. encoding to send byte type.
    userInput = input("ftp> ")
    inputList = userInput.split()

    if inputList[0] == "get":
        clientSock.send(userInput.encode())

        fileSizeBuff = recvAll(clientSock, 10)
        fileSize = int(fileSizeBuff.decode())

        print("The file size is", fileSize)

        fileData = recvAll(clientSock, fileSize)

        print("The file data is:")
        print(fileData.decode())
		
    elif userInput == "exit":
        break
    
    else:
        clientSock.send(userInput.encode())
        # print (s.recv(1024).decode())

clientSock.close()	

