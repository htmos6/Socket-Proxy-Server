# Echo server program
import socket
import time

#Loopback IP address
HOST = '127.0.0.1'
PORT = 6001
#Create a sockets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket successfully created")

# This line avoids bind() exception: OSError: [Errno 48] Address already in use as you configure address reuse
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
print ("Socket is bound to IP:",HOST," PORT:",PORT)
server_socket.listen(1)
print("Listening for connections")
conn, clientAddress = server_socket.accept()
print ('Connected ', clientAddress)

while 1:
    try:
        dataReceived = conn.recv(1024)
    except OSError:
        print (clientAddress, 'disconnected')
        server_socket.listen(1)
        conn, clientAddress = server_socket.accept()
        print ('Connected by', clientAddress)
        time.sleep(0.5)

    else:    
        print("Initial Data is:")
        #Initial data should be a byte object with utf-8 encoding
        print(dataReceived)
        #Decode the data into a string
        dataReceived = dataReceived.decode('utf-8')
        print("Decoded Data is:")
        print(dataReceived)
        #Encode and send the data back to the client
        conn.sendall(bytes(dataReceived,'utf-8'))

