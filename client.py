from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter import ttk, filedialog

# Global Variables
SERVER = socket(AF_INET, SOCK_STREAM)
IP_ADDR = "127.0.0.1"
PORT = 8050
BUFFER_SIZE = 4096

window = None

def openWindow():
  global window

  window = Tk()
  window.title("Music App")
  window.geometry("350x300")
  window.config(bg="#96c8ff")
  window.resizable(width=False, height=False)

  selectLabel = Label(window, text="Select song:", bg="#96c8ff", font=("Segoe UI", 15, "bold"))
  selectLabel.place(x=20, y=2)

  listbox = Listbox(window, height=8, width=45, activestyle="dotbox", bg="#96c8ff", font=("Segoe UI", 10))
  listbox.place(x=175, y=115, anchor=CENTER)

  scrollbar = Scrollbar(listbox, command=listbox.yview())
  scrollbar.place(relheight=1, relx=1)

  playBtn = Button(window, text="Play", bg="royalblue", fg="white", font="Consolas 11 bold")
  playBtn.place(x=40, y=215, anchor=CENTER)

  stopBtn = Button(window, text="Stop", bg="royalblue", fg="white", font="Consolas 11 bold")
  stopBtn.place(x=90, y=215, anchor=CENTER)

  uploadBtn = Button(window, text="Upload", bg="royalblue", fg="white", font="Consolas 11 bold")
  uploadBtn.place(x=220, y=215, anchor=CENTER)

  dwnldBtn = Button(window, text="Download", bg="royalblue", fg="white", font="Consolas 11 bold")
  dwnldBtn.place(x=295, y=215, anchor=CENTER)

  infoLabel = Label(window, text="", bg="#96c8ff", font=("Segoe UI", 12))
  infoLabel.place(x=20, y=240)

  window.mainloop()

SERVER.connect((IP_ADDR, PORT))
openWindow()