# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 15:54:56 2021

@author: marti
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk


def receive():
    """receiving messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """sending messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "QUITTER":
        client_socket.close()
        top.destroy()


def on_closing(event=None):
    """when the window is closed."""
    my_msg.set("QUITTER")
    send()

top = tkinter.Tk()
top.title("SuperChatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.


scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=40, width=100, yscrollcommand=scrollbar.set, bg = "black", fg = "Lime", font = "fixedsys")

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg, width = 50)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Envoyer", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#interface connection
connection = tkinter.Tk()
connection.attributes("-topmost", True)
connection.title("Connection")

lbl1 = tkinter.Label(connection, text="IP du serveur: ", font = ("verdana", 10))
lbl1.pack()
entree1 = tkinter.Entry(connection, width = 50)
entree1.pack()


lbl2 = tkinter.Label(connection, text="Porte: ", font = ("verdana", 10))
lbl2.pack()
entree2 = tkinter.Entry(connection, width = 50)
entree2.pack()

def click():
    global HOST
    HOST = entree1.get()
    global PORT
    PORT = entree2.get()
    if not PORT:
        PORT = 80
    else:
        PORT = int(PORT)
    global BUFSIZ
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    global client_socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()
    connection.destroy()

btn1 = tkinter.Button(connection, text="entrer", command=click)
btn1.pack()


tkinter.mainloop()
