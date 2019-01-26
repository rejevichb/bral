This is a client program that follows the protocol given in the HW. 

There are 4 message types in this protocol:

HELLO 
FIND 
BYE
COUNT 

The definitions and format of these requests on the course website. The client connects via TCP to the specified 
host and port, then sends a HELLO request. The server responds with a FIND message. Our program counts the 
symbol in the given corpus and returns the result in a COUNT message. This loop continues with FIND, COUNT 
until the server decides to send a BYE message. 

We save the secret flags accordingly. Please see the file. 

If the connection is dropped, the client program will shutdown. 

If the protocol is broken by the server, the client will shut down and any behavior from when the 
protocol is broken to when client shutdown is undefined. 