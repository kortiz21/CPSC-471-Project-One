# Authors: 
# Anthony Maida: amaida@csu.fullerton.edu
# Kevin Ortiz: keortiz@csu.fullerton.edu
# Ben Martinez: benmrtnz27@gmail.com
# Ethan Bockler: ethanbockler@gmail.com
# Anna Chiu: anna.chiu@csu.fullerton.edu

# Client code

# Import necessary modules
import socket			
import sys

# Get the arguments from the command line
if len(sys.argv) == 3:
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    sys.exit("Format: python client.py <ip address> <port>")

# Create a TCP socket object
controlSock = socket.socket()		
			
# connect to the server on local computer
controlSock.connect((ip, port))

# Function to save the file
def saveFile(fileName, fileData):
    # Open the file for writing
    fileObj = open(fileName, "wb")
    
    # Write the data to the file
    fileObj.write(fileData)
    
    # Close the file
    fileObj.close()

# Getting the data from the server
def recvAll(sock, numBytes):
    recvBuff = b''
    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes - len(recvBuff))
        if not tmpBuff:
            break
        recvBuff += tmpBuff
    return recvBuff

# Sending the data to the server
def sendData(dataSock, fileObj):
    # The number of bytes sent
    numSent = 0

    # Total number of bytes
    totalNumSent = 0

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
                numSent += dataSock.send(fileData[numSent:])

            totalNumSent += numSent

        # The file has been read. We are done
        else:
            break
        
    # Display the filename and the number of bytes sent
    print(f"Filename: {fileName}")
    print(f"File Size: {totalNumSent} bytes")

# Connecting to the data socket
def connectDataSock(controlSock):
    dataPort = controlSock.recv(1024).decode()
    print(f"Data Socket Port: {dataPort}")
    dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataSock.connect((ip, int(dataPort)))

    return dataSock

# Main loop
while True:
    # Get user input
    userInput = input("\nftp> ")
    inputList = userInput.split()

    # If user enters get 
    if inputList[0] == "get" and len(inputList) == 2:
        controlSock.send(userInput.encode())
        
        # Break if file not found
        try:
            dataSock = connectDataSock(controlSock)
        except:
            print("File not found")
            break
        
        fileSizeBuff = recvAll(dataSock, 10)
        
        fileSize = int(fileSizeBuff.decode())

        fileName = inputList[1]

        # Display file information
        print(f"Filename: {fileName}")
        print(f"File Size: {fileSize} bytes")

        fileData = recvAll(dataSock, fileSize)
        newFile = "fmserv_"+fileName
        saveFile(newFile, fileData)
        print(f"File Data stored in: {newFile}")

        # Close data socket once complete
        dataSock.close()

    # If user enters put 
    elif inputList[0] == "put" and len(inputList) == 2:
        controlSock.send(userInput.encode())

        dataSock = connectDataSock(controlSock)

        fileName = inputList[1]
        
        # Open the file
        try:
            fileObj = open(fileName, "rb")
        except IOError:
            print("File not found")
            break

        sendData(dataSock, fileObj)

        # Close data socket once complete
        dataSock.close()

    # If user enters ls 
    elif inputList[0] == "ls" and len(inputList) == 1:
        controlSock.send(userInput.encode())

        dataSock = connectDataSock(controlSock)
        
        files = dataSock.recv(1024).decode()
        print("Files on the server:")
        print(files)

        # Close data socket once complete
        dataSock.close()

    # If user enters quit 
    elif inputList[0] == "quit" and len(inputList) == 1:
        controlSock.send(userInput.encode())
        # Close the control socket
        controlSock.close()	
        break
    
    else:
        print("FAILED: Invalid command.")

controlSock.close()	