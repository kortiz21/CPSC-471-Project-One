# Server code 

# Import necessary modules
import socket
import sys
import os

# Get the arguments from the command line
if len(sys.argv) == 2:
    port = int(sys.argv[1])
else:
    sys.exit("Format: python server.py <port>")

# Create a TCP socket object
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
print ("Socket successfully created")

# Bind to port
serverSock.bind(('', port))
print ("Socket binded to %s" %(port))

# Socket in listening mode
serverSock.listen(5)	

controlSock, addr = serverSock.accept()	
print (f'SUCCESS: Got connection from {addr[0]}')

# Function to save the file
def saveFile(fileName, fileData):
    # Open the file for writing
    fileObj = open(fileName, "wb")
    
    # Write the data to the file
    fileObj.write(fileData)
    
    # Close the file
    fileObj.close()

# Getting the data from the client
def recvAll(sock, numBytes):
    recvBuff = b''
    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes - len(recvBuff))
        if not tmpBuff:
            break
        recvBuff += tmpBuff
    return recvBuff

# Creating the data socket using the ephemeral port
def ephemeralPort(controlSock):
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to port, picks an available port
    serverSock.bind(('', 0))

    dataPort = serverSock.getsockname()[1]
    print(f"Data Socket Port: {dataPort}")
    controlSock.send(str(dataPort).encode())

    serverSock.listen(1)

    dataSock, addr = serverSock.accept()	

    # Send the socket back
    return dataSock

# Sending the data to the client
def sendData(dataSock, fileObj):
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
            
            # # The number of bytes sent
            numSent = 0
            
            # Send the data!
            while len(fileData) > numSent:
                numSent += dataSock.send(fileData[numSent:])
        
        # The file has been read. We are done
        else:
            break

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client. 
    try:
        message = controlSock.recv(1024).decode()
        print(f"\nCommand from client: {message}")
        message = message.split()
    except:
        controlSock, addr = serverSock.accept()	
        print (f'SUCCESS: Got connection from {addr[0]}')
        message = ""

    # If we get a message
    if len(message) > 0:
        # When client wants to get a file
        if message[0] == "get" and len(message) == 2:
            fileName = message[1]
            
            # Open the file
            try:
                fileObj = open(fileName, "rb")
            except IOError:
                print("FAILURE: File not found")
                

            # Create the data socket using ephemeral port
            dataSock = ephemeralPort(controlSock)

            # Send the file data
            sendData(dataSock, fileObj)
            
            # Close data socket once done
            dataSock.close()

            print("SUCCESS: File sent")

        # When client wants to put a file
        elif message[0] == "put":
            # Create the data socket using ephemeral port
            dataSock = ephemeralPort(controlSock)

            fileSizeBuff = recvAll(dataSock, 10)
            fileSize = int(fileSizeBuff.decode())

            print("The file size is", fileSize)

            fileData = recvAll(dataSock, fileSize)

            # Save the file from the client
            fileName = message[1]
            newFile = "fmclient_" + fileName
            saveFile(newFile, fileData)
            print(f"File Data stored in: {newFile}")

            # Close data socket once done
            dataSock.close()

            print("SUCCESS: File received")

        # When client wants to list the files
        elif message[0] == "ls" and len(message) == 1:
            # Create the data socket using ephemeral port
            dataSock = ephemeralPort(controlSock)

            # Get the list of files
            files = "\n".join(os.listdir("."))

            # Send the list of files
            dataSock.send(files.encode())

            # Close data socket once done
            dataSock.close()

            print("SUCCESS: File list sent")
        
        elif message[0] == "quit" and len(message) == 1:
            controlSock.close()
            print("SUCCESS: Closing connection")
            
# Close once we break out of the loop
controlSock.close()