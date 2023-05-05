# CPSC-471-Project-One

# Authors:

Kevin Ortiz: keortiz@csu.fullerton.edu

Ben Martinez: benmrtnz27@gmail.com

Anthony Maida: amaida@csu.fullerton.edu

Ethan Bockler: ethanbockler@gmail.com

Anna Chiu: anna.chiu@csu.fullerton.edu

# Programming language:

Python 3: We used python 3.10 for testing.

# Executing program:

There are two python programs, `server.py` and `client.py`
We used python3 when executing, but it depends on how you execute your python programs.
Dont include <> when writing the port number or IP address. Just put the number.

Start the `server.py` by typing `python3 server.py <port number>`.
Ex. `python3 server.py 8000`

Start the `client.py` by typing `python3 client.py <ip address> <port number>`.
Ex. `python3 client.py 127.0.0.1 8000` or `python3 client.py localhost 8000`

Once the client connects, the client will display `ftp>` and this is where you insert commands to send to the server.
The server will display `SUCCESS: Got connection from <ip address>` once the client connects.

# Using the Program:

There are four commands which are get, put, ls and quit.

Get and put both require a file name to be followed after it.
Ex. `put test1.txt` or `get test1.txt`
There are two test files included which are `test1.txt` and `test2.txt`.

The `ls` will display all files in the directory where our `server.py` is located.

`quit` will ensure that we close the port and allow for the server to listen for another connection.
This is the recommended method for exiting the client as it will close the port.

# Anything Special:

When using get or put, the data gets saved to a file in the directory.

We also ensured that we implemented an ephemeral port.