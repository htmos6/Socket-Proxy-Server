# Echo server program
import socket
import time
import re


# Loopback IP address 
# Proxy is a Server for Echo_Client
# Proxy Left Socket
HOST_as_Server = '127.0.0.1'
PORT_as_Server = 6001


# Loopback IP address
# Proxy is a Client for Echo_Server
# Proxy Right Socket
HOST_as_Client = '127.0.0.1'
PORT_as_Client = 6002


# Proxy Left Socket
proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Proxy Server (Left) Socket Successfully Created")
proxy_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy_server_socket.bind((HOST_as_Server, PORT_as_Server))
print("Proxy Server (Left) Socket Bound to IP:", HOST_as_Server," PORT:", PORT_as_Server)
proxy_server_socket.listen(1)
print("Proxy Server (Left) Socket is Listening for Connections")
connProxy, clientAddressProxy = proxy_server_socket.accept()
print('Proxy Server (Left) Socket is Connected ', clientAddressProxy)


# Create a socket for Proxy client side
# Proxy Right Socket
proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_client_socket.connect((HOST_as_Client, PORT_as_Client))


seperated_data = []


PROXY_CACHE_DATA = []
PROXY_CACHE_DATA_ID = []

while 1:
    indices_inp = []
    datas_inp = []
    datas_out = []

    try:
        dataReceivedFromClient = connProxy.recv(1024)
    except OSError:
        print (clientAddressProxy, 'disconnected')
        proxy_server_socket.listen(1)
        connProxy, clientAddressProxy = proxy_server_socket.accept()
        print ('Connected by', clientAddressProxy)
        time.sleep(0.5)

    else:    
        # print("Initial Data is:")
        # Initial data should be a byte object with utf-8 encoding
        # print(dataReceivedFromClient)
        # Decode the data into a string
        dataReceivedFromClient = dataReceivedFromClient.decode('utf-8')
        print("Decoded Data is:")
        print(dataReceivedFromClient)

        # Ex: dataReceivedFromClient = "OP=101;IND=5,9,3;" --> When splitted --> ['OP=101', 'IND=5,9,3', '']
        len_sep_data = re.split(';', dataReceivedFromClient)
        len_sep_data = len(len_sep_data)
        seperated_data = re.split(';|=', dataReceivedFromClient)

        # Required for PUT, GET, ADD, CLR
        if (len_sep_data >= 2): # Required for PUT, GET, ADD
            opcode = seperated_data[seperated_data.index("OP") + 1]
        if (len_sep_data >= 3): # Required for PUT, GET, ADD
            indices_inp = seperated_data[seperated_data.index("IND") + 1].split(",")
        if (len_sep_data == 4): # Required for PUT
            datas_inp = seperated_data[seperated_data.index("DATA") + 1].split(",")

        if opcode == "GET": # "OP=GET;IND=5,9,3;"
            for indice in indices_inp:
                if indice in PROXY_CACHE_DATA_ID:
                    location_of_element_in_list = PROXY_CACHE_DATA_ID.index(indice)
                    datas_out.append(PROXY_CACHE_DATA[location_of_element_in_list])

                    PROXY_CACHE_DATA.insert(0, PROXY_CACHE_DATA.pop(location_of_element_in_list))
                    PROXY_CACHE_DATA_ID.insert(0, PROXY_CACHE_DATA_ID.pop(location_of_element_in_list))
                else:
                    message_to_server = "GET:" + indice + ":"
                    proxy_client_socket.sendall(bytes(message_to_server,'utf-8'))
                    time.sleep(0.5)
                    dataReceivedFromServer = proxy_client_socket.recv(1024)
                    dataReceivedFromServer = dataReceivedFromServer.decode('utf-8')
                    datas_out.append(dataReceivedFromServer)

                    PROXY_CACHE_DATA.insert(0, dataReceivedFromServer) # Insert last reached data to beginning of the list
                    PROXY_CACHE_DATA_ID.insert(0, indice)

                    if (len(PROXY_CACHE_DATA) == 6 or len(PROXY_CACHE_DATA_ID) == 6):
                        PROXY_CACHE_DATA.pop()
                        PROXY_CACHE_DATA_ID.pop()
                
                print("Numbers in Cache by Order: ", end= "")
                for i in PROXY_CACHE_DATA:
                    print(i, end= " ")
                print("\n")
            
            dataReceivedFromClient = dataReceivedFromClient + "DATA=" + ",".join(datas_out)

        elif opcode == "PUT": # "OP=PUT;IND=5,9,3;DATA=3,5,7;"
            for indice, data in zip(indices_inp, datas_inp) :
                if indice in PROXY_CACHE_DATA_ID:
                    location_of_element_in_list = PROXY_CACHE_DATA_ID.index(indice)

                    PROXY_CACHE_DATA.pop(location_of_element_in_list)

                    PROXY_CACHE_DATA.insert(0, data)
                    PROXY_CACHE_DATA_ID.insert(0, PROXY_CACHE_DATA_ID.pop(location_of_element_in_list))

                    message_to_server = "PUT:" + indice + ":" + data + ":"
                    proxy_client_socket.sendall(bytes(message_to_server,'utf-8'))
                    time.sleep(0.5)
                    dataReceivedFromServer = proxy_client_socket.recv(1024)
                    dataReceivedFromServer = dataReceivedFromServer.decode('utf-8')
                    datas_out.append(dataReceivedFromServer)
                else:
                    message_to_server = "PUT:" + indice + ":" + data + ":"
                    proxy_client_socket.sendall(bytes(message_to_server,'utf-8'))
                    time.sleep(0.5)
                    dataReceivedFromServer = proxy_client_socket.recv(1024)
                    dataReceivedFromServer = dataReceivedFromServer.decode('utf-8')
                    datas_out.append(dataReceivedFromServer)

                    PROXY_CACHE_DATA.insert(0, dataReceivedFromServer) # Insert last reached data to beginning of the list
                    PROXY_CACHE_DATA_ID.insert(0, indice)

                    if (len(PROXY_CACHE_DATA) == 6 or len(PROXY_CACHE_DATA_ID) == 6):
                        PROXY_CACHE_DATA.pop()
                        PROXY_CACHE_DATA_ID.pop()

                print("Numbers in Cache by Order: ", end= "")
                for i in PROXY_CACHE_DATA:
                    print(i, end= " ")
                print("\n")

            dataReceivedFromClient = dataReceivedFromClient[0:dataReceivedFromClient.find("DATA")]
            dataReceivedFromClient = dataReceivedFromClient + "DATA=" + ",".join(datas_out)

        elif opcode == "CLR": # "OP=000;"
            PROXY_CACHE_DATA = []
            PROXY_CACHE_DATA_ID = []

            message_to_server = "CLR:"
            proxy_client_socket.sendall(bytes(message_to_server,'utf-8'))
            time.sleep(0.5)
            dataReceivedFromServer = proxy_client_socket.recv(1024)
            dataReceivedFromServer = dataReceivedFromServer.decode('utf-8')
            dataReceivedFromClient = dataReceivedFromClient 

        elif opcode == "ADD": # "OP=ADD;IND=5,9,3;"
            for indice in indices_inp:
                if indice in PROXY_CACHE_DATA_ID:
                    location_of_element_in_list = PROXY_CACHE_DATA_ID.index(indice)
                    datas_out.append(PROXY_CACHE_DATA[location_of_element_in_list])

                    PROXY_CACHE_DATA.insert(0, PROXY_CACHE_DATA.pop(location_of_element_in_list))
                    PROXY_CACHE_DATA_ID.insert(0, PROXY_CACHE_DATA_ID.pop(location_of_element_in_list))
                else:
                    message_to_server = "ADD:" + indice + ":"
                    proxy_client_socket.sendall(bytes(message_to_server,'utf-8'))
                    time.sleep(0.5)
                    dataReceivedFromServer = proxy_client_socket.recv(1024)
                    dataReceivedFromServer = dataReceivedFromServer.decode('utf-8')
                    datas_out.append(dataReceivedFromServer)

                    PROXY_CACHE_DATA.insert(0, dataReceivedFromServer) # Insert last reached data to beginning of the list
                    PROXY_CACHE_DATA_ID.insert(0, indice)

                    if (len(PROXY_CACHE_DATA) == 6 or len(PROXY_CACHE_DATA_ID) == 6):
                        PROXY_CACHE_DATA.pop()
                        PROXY_CACHE_DATA_ID.pop()
                
                print("Numbers in Cache by Order: ", end= "")
                for i in PROXY_CACHE_DATA:
                    print(i, end= " ")
                print("\n")
            
            dataReceivedFromClient = dataReceivedFromClient + "DATA=" + str(sum(list(map(int, datas_out))))

        # Encode and send the data back to the client
        print("DATA Sent to Client", dataReceivedFromClient)
        connProxy.sendall(bytes(dataReceivedFromClient,'utf-8'))

