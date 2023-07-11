# Socket-Proxy-Server

### 1- How to Use Sockets ?
* You can see the state diagram of TCP sockets in Figure 1.
![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/49b6f2b0-0bad-4533-b33d-6dfddec8fdcc)

+ The socket library functions can be summarized as follows:
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

### 2- Simple Proxy Server
* We will implement a simple system consisting of 3 nodes. Namely,
Client, Proxy, and Server. Topology is very simple and can be seen in Figure 2.

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/f673559a-c974-4370-950d-84752f5735c3)

### 2.1- Operation Specifications
* The Server will hold a list of 10 elements as described in Table 1. Each entry will consist
of an index value ranging from 0 to 9 and data of a single integer. The Proxy should be
consistent with the server, that is any update made to the Proxy’s table should also be
made to Server’s table. 

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/ca2b5b94-7758-494f-8e51-907664f46cc1)

* The Proxy server will hold half of the table in its process as described in Table 2,
think of it as a cached version of the Server’s table. The Client will only communicate
with the proxy server, if an element that is not present in the Proxy’s table is required
proxy server will communicate with the Server to get that element and add it to its table
by overwriting the oldest table entry.

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/fc0b0a61-ab55-4ee4-afea-f1755cc3eb04)

* Nodes will exchange proxy messages between them using the format below.  
```OP=XXX;IND=Ind1,Ind2,..;DATA=Dat1,Dat2,...;```

* Notice that fields are separated with semicolons(;). OP field describes which operation
to do on the table, for more detail check Table 3. IND field tells which of the indexes are
required for the operation. The DATA field is for integer data either from the server for
operations like ”ADD” or as an update value from the client. Not all messages require
every field. You can choose to omit the unused fields for certain operations.

* Response messages have the same form as request messages. For example response
to the ”ADD” message will have ”ADD” as the operation code and contain the result in
the ”DATA” field.

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/8c44bb44-bb74-4570-a958-bd31bdb1ed4f)










![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/9c4f3e4d-b617-466c-857d-ee9240f2cbe2)
