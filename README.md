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

### 3- Test Results
* For the first case, I have filled the remote server data buffer with put command. You can see the cache content at the “Proxy_process.py File Terminal”.  

* Client_process.py File Terminal  

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/00f9c17e-aa50-4880-b313-71197920e432)

* Proxy_process.py File Terminal

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/c6f4e55c-2e6c-48dd-b2f1-018b40602d17)

* Server_process.m File Terminal   
I have filled buffer indexes from 0 to 4 with values 0 to 4.

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/2bc5c0a6-f9ea-4aa8-8604-695e41de6881)

* Then, I have filled remaining buffer indexes from 5 to 9 with values 5 to 9. As you can see, cache
content will bu updated. According to most used data is put to the top of the cache.  

* Client_process.py

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/255c09e9-b2e2-4a67-a8f8-3b280a71c90f)

* Proxy_process.py File Terminal

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/1671d08d-6d92-4e44-83c6-dcc7cca9c308)

* Here is the remote server. It also updated. Such that new added datas will be added to here.,

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/f1dad75f-3c68-43e5-8db1-d155ce774af6)

* Now, I will only change index 0 data with a value 12. I will check that will it work or not.

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/90b29f53-083b-498d-bc39-16bd86d15163)

* Since I added 12 to the index0, cache will put it to the upper most index because it was the most
recently accessed element. Also, I changed index 1 content with a number 45. Top element of the
cache is a 12 as first. After addition of 45, 45 becomes a top element of the cache.

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/bc51c15b-676c-4b7b-94c3-382ead26e72a)

* Here, remote server content. It is updated as I put new datas to server.  

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/7429a04a-1c48-476e-8d88-80b64ec4fb02)

* I added datas at the index 0,1,2. Since they exist at the cache, they will not connect to server. Values
will be directly taken from cache memory since data exist in the cache

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/a91ffd2f-338a-4f1b-824f-8d10aac58514)

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/9580f0d8-a82e-4429-b2cb-56799ba253dd)

* By using get method, obtain values from corresponding indexes. Index 1 value exist in the cache.
Hence, only index 3 and 5 will taken from server. Index 1 taken from cache.

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/a419b001-ded9-490e-b4af-3197a7d92157)



![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/e70a399a-42f5-457d-8d21-1ccecdeac52b)



![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/b15a01c2-9cdf-4cc9-b0fd-3f992a599a30)



* Clear Operation

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/f7f05929-698d-4a8f-baca-2a3537347034)

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/0a7e54ab-ba61-449d-bfbb-70c4c8996b50)

![image](https://github.com/htmos6/Socket-Proxy-Server/assets/88316097/56c46d78-e687-47d4-ae11-28e9d611d6ae)

