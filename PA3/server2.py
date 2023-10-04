#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "[team name here]"
__credits__ = [
  "Your",
  "Names",
  "Here"
]

import socket as s
import time
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

serverMsg = "X: \"\", Y: \"\""
counter = 0
MAX = 2
clientList = []

def debugPrt(msg):
    print(str(msg))

def connection_handler(connection_socket):
    # Old code
    query = connection_socket.recv(1024)
    query_decoded = query.decode()
    log.info("Recieved query test \"" + str(query_decoded) + "\"")
    time.sleep(5)
    # response = query_decoded.upper()
    # connection_socket.send(response.encode())
    # connection_socket.close()

    
    client = threading.Thread(target=msgThread, args=(query_decoded, id))

    client.start()

    time.sleep(5)

    client.join()

    connection_socket.send(serverMsg.encode())
    connection_socket.close()

    # while True:
    #     if t.active_count() >= MAX:
    #         t.Thread.join()

def msgThread(msg, id):
    

def main():
    global clientList

    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    server_socket.bind(('', server_port))

    server_socket.listen(MAX)

    log.info("The server is ready to reveive on port " + str(server_port))

    try:
        while True:
            connection_socket, address = server_socket.accept()
            log.info("connected to client at " + str(address))

            
            clientList.append(connection_socket)
            # for i in clientList:
            #     print("\n" + str(i) + "\n")

            if len(clientList) >= MAX:
                print("Two clients added?") #remove
                break

        for i in clientList:
            connection_handler(i)

    finally:
        server_socket.close()

if __name__ == "__main__":
  main()