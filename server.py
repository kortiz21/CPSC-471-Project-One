# Server code 
# first of all import the socket library
import socket
import sys

if len(sys.argv) == 2:
    port = int(sys.argv[1])
else:
    sys.exit("Format: python server.py <port>")

# next create a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
print ("Socket successfully created")

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)	
print ("socket is listening")		

clientSock, addr = s.accept()	
print ('Got connection from', addr )

# send a thank you message to the client. encoding to send byte type.
clientSock.send('Thank you for connecting'.encode())

def recvAll(sock, numBytes):
    recvBuff = b''
    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes - len(recvBuff))
        if not tmpBuff:
            break
        recvBuff += tmpBuff
    return recvBuff

# a forever loop until we interrupt it or
# an error occurs
while True:

    # Get the data from the client
    message = clientSock.recv(1024).decode()
    message = message.split()

    if message[0] == "get":
        fileName = message[1]
        
        # Open the file
        try:
            fileObj = open(fileName, "rb")
        except IOError:
            print("File not found")
            break

        # The number of bytes sent
        numSent = 0

        # The file data
        fileData = None

        # Keep sending until all is sent
        while True:
            
            # Read 65536 bytes of data
            fileData = fileObj.read(65536)
            
            # Make sure we did not hit EOF
            if fileData:
                # Get the size of the data read
                # and convert it to string
                dataSizeStr = str(len(fileData))
                
                # Prepend 0's to the size string
                # until the size is 10 bytes
                while len(dataSizeStr) < 10:
                    dataSizeStr = "0" + dataSizeStr
            

                # Convert the dataSizeStr to bytes
                dataSizeBytes = dataSizeStr.encode()
                
                # Prepend the size of the data to the
                # file data.
                fileData = dataSizeBytes + fileData
                
                # The number of bytes sent
                numSent = 0
                
                # Send the data!
                while len(fileData) > numSent:
                    numSent += clientSock.send(fileData[numSent:])
            
            # The file has been read. We are done
            else:
                break

    print(message)
    # Close the connection with the client
    # c.close()
    if message == "exit":
        break
    # Breaking once connection closed

clientSock.close()
