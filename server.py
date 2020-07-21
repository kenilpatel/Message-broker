# Name : Kenilkumar Maheshkumar Patel
# Student Id: 1001765579

# importing important modules for code
import socket
import pickle
import threading
import re
from random import randint
import time
from tkinter import *
from tkinter import font
import os
''' maintain the list of clients id that are connected currently '''
clients = []
''' maintain the list of clients name that are connected currently '''
name = []
''' initialize the GUI '''
root = Tk()
''' both variables are used to represent the message received
from the client '''
signal = ""
signal_disconnected = ""
count = 1
''' this thread handle the incoming connection to the client '''


class handle_client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        ''' create a socket '''
        s = socket.socket()
        ''' port number to accept the connection from client '''
        port = 7398
        s.bind(('', port))
        s.listen(5)
        ''' initialize the count to 0 as intially no clients
        are connected to the server '''
        count = 0
        while(True):
            ''' accept the connection '''
            c, addr = s.accept()
            ''' if there are no clients connected then set
            count to 1 otherwise juts increment the counter '''
            if(len(clients) == 0):
                count = 1
            else:
                x = sorted(clients)
                count = int(x[len(clients) - 1]) + 1
            ''' create the thread to send and recieve the
            message from client '''
            t = myThread(c, count)
            t.start()


''' This thread to send and recieve the message from client '''


class myThread(threading.Thread):
    def __init__(self, c, id):
        threading.Thread.__init__(self)
        self.c = c
        self.id = id
        self.n = ""
        self.msg = 100

    def run(self):
        err = 0
        ''' add the name of client to list of clients connected '''
        clients.append(self.id)
        global signal_disconnected
        ''' if number of connected clients exceeds 3 then just remove
        the name of client and close the connection '''
        if(len(clients) == 4):
            ''' remove the client id from connected clients '''
            clients.remove(self.id)
            ''' send the 404 signal to client which means server is full '''
            self.msg = 404
            data = pickle.dumps(self.msg)
            self.c.send(data)
        else:
            global count
            while (True):
                try:
                    ''' if server is communicating to client for the
                    first time then send msg 201 which will ask the
                    client to send its name to server '''
                    if(self.msg == 100):
                        signal_disconnected = ""
                        self.msg = "201" + ":" + str(count)
                        count = count + 1
                    ''' send the signal to client '''
                    data = pickle.dumps(self.msg)
                    self.c.send(data)
                    ''' recive data from client '''
                    rdata = pickle.loads(self.c.recv(1024))
                    if(re.search("^201:*", str(self.msg)) != None):
                        self.n = rdata
                        name.append(self.n)
                        ''' send msg 200 which means normal message
                        no special instruction '''
                        self.msg = 200
                    elif(re.search("^download:*", str(rdata)) != None):
                        self.msg = "content:here is the download content" + \
                            str(randint(0, 100))
                    elif(re.search("^upload:*", str(rdata)) != None):
                        x, number = rdata.split(":")
                        self.msg = "content:here is the upload content" + \
                            str(number)
                    else:
                        self.msg = 200
                except Exception as e:
                    ''' if exception occurs then disconnects the
                    clients '''
                    err = 1
                    if(self.n != ""):
                        ''' remove the client from the list of clients
                        that are connected
                        construct the signal about which clients
                        got disconnected and print it on GUI '''
                        signal_disconnected = self.n + " disconnected"
                    clients.remove(self.id)
                    if(self.n != ""):
                        name.remove(self.n)
                    break


''' function that stops the connection with the server and exit '''


def close_window():
    ''' destroying the windows and exiting the code execution '''
    root.destroy()
    os._exit(0)


''' setting up the font size '''
myFont = font.Font(size=20)
myFont1 = font.Font(size=40)
''' create empty label to have some space between component '''
Label(root).pack()
''' create button to close the server '''
btn = Button(root, text="Close server", command=close_window)
btn['font'] = myFont
btn.pack()
''' set up the screen size to 600x600 '''
root.geometry("600x800")
''' create empty label to have some space between component '''
Label(root).pack()
''' normal label to display message on GUI '''
head = Label(root, text="Currently connected client")
head['font'] = myFont
head.pack()
''' create empty label to have some space between component '''
Label(root).pack()
''' create empty label to have some space between component '''
Label(root).pack()
''' label to display name of currently connected clients '''
cstatus = Label(root)
cstatus['font'] = myFont
cstatus.pack()
''' create empty label to have some space between component '''
Label(root).pack()
''' create empty label to have some space between component '''
Label(root).pack()
''' label to display name of client who just got disconnected '''
dstatus = Label(root)
dstatus['font'] = myFont
dstatus.pack()
''' call this update function every 50 ms so it will update the
information on GUI '''


def update():
    c = ""
    ''' if there is no client conected then print no one is
    connected '''
    if(len(name) == 0):
        c = "No one is connected"
    else:
        ''' if there are some clients that are connected then print it
        on GUI '''
        for i in name:
            c = c + i + "\n"
    cstatus.config(text=c)
    ''' signal_disconnected prints the which clients got disconnnected '''
    dstatus.config(text=signal_disconnected)
    ''' call update function after every 50 ms '''
    root.after(50, update)


update()
''' call the thread to handle clients '''
main_t = handle_client()
main_t.start()
''' close the server when user simply press close button '''


def doSomething():
    os._exit(0)


root.protocol('WM_DELETE_WINDOW', doSomething)
''' start the main GUI window '''
root.mainloop()
