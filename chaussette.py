# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 15:22:05 2021

@author: marti
"""

# Python program to implement server side of chat room.  

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}
HOST = '' #public ip
PORT = 80
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s s'est connecté." % client_address)
        client.send(bytes("Bienvenue dans le Super Chatter 2000 !\nEntrez votre pseudonyme dans le chat...", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Bienvenue %s! Pour quitter le chat, taper QUITTER ' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s est arrivé !" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("QUITTER", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("QUITTER", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s s'est déconnecté." % name, "utf8"))
            break

def broadcast(msg, prefix=""): 

    # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()

