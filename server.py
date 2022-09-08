from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Global Variables
SERVER = socket(AF_INET, SOCK_STREAM)
IP_ADDR = "127.0.0.1"
PORT = 8050
clients={}

def acceptConn():
  while True:
    conn, addr = SERVER.accept()
    name = conn.recv(2048).decode().strip()
    print(f"> {name} has connected {addr}")

    clients[name] = {
      "cli": conn,
      "addr": addr,
      "conn_with": "",
      "file_name": "",
      "file_size": 4096
    }

    cliThread = Thread(target=handleClient, args=(conn, name))
    cliThread.start()

def handleClient(cli, name):
  while True:
    try:
      msg=cli.recv(2048).decode().strip()
      if msg=="~disconnected":
        print(f"> {name} has disconnected")
        clients.pop(name)
      elif msg:
        print(f"{name}: {msg}")
    except:
      pass

def setup():
  SERVER.bind((IP_ADDR, PORT))
  SERVER.listen(100)
  print("Waiting for incoming connections...\n")
  acceptConn()

print("\n\t\t\t\t~~*** Music Sharing App ***~~\n")
setup()
