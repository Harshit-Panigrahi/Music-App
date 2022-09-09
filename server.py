from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Global Variables
SERVER = socket(AF_INET, SOCK_STREAM)
IP_ADDR = "127.0.0.1"
PORT = 8050
clients={}

def ftpServer():
  auth = DummyAuthorizer()
  auth.add_user("ftp_username", "ftp_pass", ".", "elradfmw")
  handler = FTPHandler
  handler.authorizer = auth
  ftp_server = FTPServer((IP_ADDR, 21), handler)
  ftp_server.serve_forever()

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
thread1 = Thread(target=setup).start()
thread2 = Thread(target=ftpServer).start()
