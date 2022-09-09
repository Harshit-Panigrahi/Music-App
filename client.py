import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from tkinter import *
from tkinter import filedialog, messagebox
from socket import socket, AF_INET, SOCK_STREAM
from ftplib import FTP

# Global Variables
SERVER = socket(AF_INET, SOCK_STREAM)
IP_ADDR = "127.0.0.1"
PORT = 8050

window = None
listBox = None
infoLabel = None
nameEntry = None

nameBtn = None
playBtn = None
pauseBtn = None
stopBtn = None
uploadBtn = None
dwnldBtn = None

name = None
now_playing = None
songLst = []
songCount = 0

def getSongs():
  global songCount
  
  for f in os.listdir("."):
    if f.endswith(".wav") or f.endswith(".mp3") or f.endswith("ogg"):
      songCount += 1
      listBox.insert(songCount, os.fsdecode(f))

  print(songCount, "songs found")

def connect():
  global name
  name = nameEntry.get().strip()

  if name:
    SERVER.connect((IP_ADDR, PORT))
    SERVER.send(name.encode("utf-8"))
    nameEntry.config(state=DISABLED)
    nameBtn.config(bg="white", disabledforeground="royalblue", state=DISABLED)
    playBtn.config(bg="royalblue", fg="white", state=NORMAL)
    pauseBtn.config(bg="royalblue", fg="white", state=NORMAL)
    stopBtn.config(bg="royalblue", fg="white", state=NORMAL)
    uploadBtn.config(bg="royalblue", fg="white", state=NORMAL)
    dwnldBtn.config(bg="royalblue", fg="white", state=NORMAL)
    window.protocol("WM_DELETE_WINDOW", exitApp)
    pygame.mixer.init()

  else:
    name = None

def exitApp():
  if messagebox.askokcancel("Quiz Game", "Do you want to exit the app?"):
    try:
      window.destroy()
      SERVER.send("~disconnected".encode("utf-8"))
      SERVER.close()
    except:
      pass

def playSong():
  global now_playing

  if now_playing:
    pygame.mixer.music.unpause()
    infoLabel.config(text=f"Now playing: {now_playing}")
  else:
    now_playing = listBox.get(ANCHOR)
    pygame.mixer.music.load(now_playing)
    pygame.mixer.music.play()
    infoLabel.config(text=f"Now playing: {now_playing}")

def pauseSong():
  if now_playing:
    pygame.mixer.music.pause()
    infoLabel.config(text=f"Paused: {now_playing}")

def stopSong():
  global now_playing
  if now_playing:
    now_playing = None
    pygame.mixer.music.stop()
    infoLabel.config(text="")

def browseFiles():
  try:
    file = filedialog.askopenfilename()
    filename = os.path.basename(file)
    ftp_server = FTP("127.0.0.1", "ftp_username", "ftp_pass")
    ftp_server.encoding = "utf-8"
    ftp_server.cwd("shared_files")
    with open(file, 'rb') as f:
      ftp_server.storbinary(f"STOR {filename}", f)
    ftp_server.quit()

  except FileNotFoundError:
    print("No file selected")

def openWindow():
  global window, listBox, infoLabel, nameEntry
  global nameBtn, playBtn, pauseBtn, stopBtn, uploadBtn, dwnldBtn

  window = Tk()
  window.title("Music App")
  window.geometry("350x350")
  window.config(bg="#96c8ff")
  window.resizable(width=False, height=False)

  Label(window, text="Enter your name:", bg="#96c8ff", font="Consolas 11").place(x=15, y=10)
  nameEntry = Entry(window, width=35, font="Consolas 10")
  nameEntry.place(x=15, y=35)
  nameBtn = Button(window, text="Submit", bg="royalblue", fg="white", font="Consolas 10 bold", command=connect)
  nameBtn.place(x=300, y=45, anchor=CENTER)

  Label(window, text="Songs in this directory:", bg="#96c8ff", font=("Consolas 14 bold")).place(x=25, y=65)
  listBox = Listbox(window, height=8, width=45, activestyle="dotbox", bg="#96c8ff", font=("Consolas", 10))
  listBox.place(x=175, y=165, anchor=CENTER)

  playBtn = Button(window, text="Play", bg="white", disabledforeground="royalblue", font="Consolas 11 bold", command=playSong, state=DISABLED)
  playBtn.place(x=20, y=285, anchor=W)
  pauseBtn = Button(window, text="Pause", bg="white", disabledforeground="royalblue", font="Consolas 11 bold", command=pauseSong, state=DISABLED)
  pauseBtn.place(x=70, y=285, anchor=W)  
  stopBtn = Button(window, text="Stop", bg="white", disabledforeground="royalblue", font="Consolas 11 bold", command=stopSong, state=DISABLED)
  stopBtn.place(x=20, y=325, anchor=W)

  uploadBtn = Button(window, text="Upload", bg="white", disabledforeground="royalblue", font="Consolas 11 bold", command=browseFiles, state=DISABLED)
  uploadBtn.place(x=320, y=285, anchor=E)
  dwnldBtn = Button(window, text="Download", bg="white", disabledforeground="royalblue", font="Consolas 11 bold", state=DISABLED)
  dwnldBtn.place(x=320, y=325, anchor=E)

  infoLabel = Label(window, text="", bg="#96c8ff", font="Consolas 11")
  infoLabel.place(x=25, y=236)

  getSongs()
  window.mainloop()

openWindow()
