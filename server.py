from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Global Variables
SERVER = socket(AF_INET, SOCK_STREAM)
IP_ADDR = "127.0.0.1"
PORT = 8050
BUFFER_SIZE = 4096
clients={}

def setup():
  SERVER.bind((IP_ADDR, PORT))
  SERVER.listen(100)
  print("Waiting for incoming connections...\n")
  acceptConn()

def acceptConn():
  while True:
    conn, addr = SERVER.accept()
    print(f"{addr} has joined")

print("\n\t\t\t\t~~*** Music Sharing App ***~~\n")
setup()