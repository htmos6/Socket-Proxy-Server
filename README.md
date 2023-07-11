# Socket-Proxy-Server

### How to Use Sockets ?
You can see the state diagram of TCP sockets in Figure 1.
![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/49b6f2b0-0bad-4533-b33d-6dfddec8fdcc)

The socket library functions can be summarized as follows:
1. ```socket.socket(family=AF INET, type=SOCK STREAM, proto=0, fileno=None)```  
Creates a socket object, default parameters are correct for this homework.
2. ```socket.bind(address)```  
Binds the socket to an address that is (IP, PORT) pair.
3. ```socket.close()```  
Closes the socket and all its connections
4. ```socket.listen([backlog])```   
Enable a server to accept connections. Listens to the number of connections specified by backlog.
5. ```socket.connect(address)```   
Connect to a remote socket at the address, the address is (IP, PORT) pair.
6. ```socket.accept()```  
Accepts an incoming connection. The return value is a pair (conn, address) where
conn is a new socket object usable to send and receive data on the connection, and
address is the address bound to the socket on the other end of the connection.
7. ```socket.recv(bufsize[, flags])```  
Receives a specified number of bytes from the TCP buffer. Returns a byte object
representing the received data.
8. ```socket.send(bytes[, flags])```   
Sends a specified number of bytes through the socket. Returns the number of bytes
sent.
9. ```socket.sendall(bytes[, flags])```  
Similar to send but this method continues to send data from bytes until either all
data has been sent or an error occurs.











![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/9c4f3e4d-b617-466c-857d-ee9240f2cbe2)
