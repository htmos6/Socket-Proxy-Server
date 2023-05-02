# Echo server program
import socket
import time

#Loopback IP address
HOST = '127.0.0.1'
PORT = 6001
#Create a sockets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

while 1:
    print("\nEnter Proxy Message in the form of")
    print("OP=XXX;IND=Ind1,Ind2,..;DATA=Dat1,Dat2...;")
    # IND field shows which of the indexes are required for the operation.
    message = input("Enter Message: ")

    #You can only send byte-like objects through the socket
    client_socket.sendall(bytes(message,'utf-8'))
    time.sleep(0.5)

    #Initial data should be a byte object with utf-8 encoding
    dataReceived=client_socket.recv(1024)
    #print("Initial Data is:")
    #print(dataReceived)
    #Decode the data into a string
    dataReceived = dataReceived.decode('utf-8')
    print("\nReceived Message is:")
    print(dataReceived, "\n\n")
