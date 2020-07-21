# Name : Kenilkumar Maheshkumar Patel
# Student Id : 1001765579

# importing important modules for code

import socket
import pickle
import re
import threading
import time
from tkinter import *
import sys
import os
from tkinter import font
from tkinter import simpledialog
''' Started the GUI '''
root = Tk()
''' This vaiable stores the name of client and sends it to server'''
name = StringVar()
''' This is the main thread that is gonna handle the communication with the
 server '''
download = 0
upload = 0
upload_num = 0
data_from_server = ""


class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        ''' Socket variable '''
        self.s = None
        ''' Port number where client is gonna connect to the server on both of
         the system port number is same '''
        self.port = 7398
        ''' This variable stores the state of the connection it is
        initialize to 0 that means at the time of creating thread
        client is not connected to the server '''
        self.conn = 0
        ''' This variable stores the information about connection status to
         the server '''
        self.status = ""
        ''' This stores the code which represent different kind of
         informations '''
        self.code = 0
        ''' This variable stores the client name '''
        self.name_client = ""

    def run(self):
        while(True):
            ''' if anytime conn got lost with server then we will try to
             connect to server again '''
            if(self.conn == 0):
                try:
                    ''' attempting to connect server '''
                    self.s = socket.socket()
                    self.s.connect(('127.0.0.1', self.port))
                    ''' if everythin happens properly then change
                    conn varible to 1 which represents the
                    client is successfully connected to client '''
                    self.conn = 1
                except Exception as e:
                    ''' If any exception occurs during attempting the
                     connection that set the message to
                     server is not available and conn variable to 0 '''
                    self.status = "Server is not available"
                    self.conn = 0
                    ''' 403 represent server is not available '''
                    self.code = 403
            else:
                try:
                    ''' receving message from server '''
                    msg = pickle.loads(self.s.recv(1024))
                    ''' if message is 404 then server is currently connected
                     to 3 clients '''
                    if(msg == 404):
                        self.status = "server is full please"
                        self.conn = 0
                        self.code = 404
                    elif(re.search("^201:*", str(msg)) != None):
                        ''' if message is 201 then server is requesting
                        the name from client '''
                        x, y = msg.split(":")

                        self.code = 201
                        self.status = "Server is online"
                        self.name_client = "client-" + str(y)
                        ''' sending the name to the server '''
                        data = pickle.dumps(self.name_client)
                        self.s.send(data)
                        self.conn = 1
                    elif(msg == 200):
                        ''' server is normally communicating with the client
                     no special instruction given by server '''
                        global download, upload
                        if(download == 1):
                            download = 0
                            data = pickle.dumps("download:a")
                        elif(upload == 1):
                            upload = 0
                            data = pickle.dumps("upload:" + str(upload_num))
                        else:
                            data = pickle.dumps("200")
                        self.s.send(data)
                        self.conn = 1
                        self.status = "Connected"
                        self.code = 200
                    elif((re.search("^content:*", str(msg)) != None)):
                        global data_from_server
                        x, data_from_server = msg.split(":")
                        data = pickle.dumps("200")
                        self.s.send(data)
                        self.conn = 1
                        self.status = "Connected"
                        self.code = 200

                except Exception as e:
                    ''' if anything goes wrong from server side then reset
                    the connection by setting conn to 0 and tries
                    to attempt the connection again '''
                    self.name_client = ""
                    self.status = "Server is not available"
                    self.conn = 0
                    self.code = 403


''' start the thread to maintain the connection with the server '''
t = myThread()
t.start()
''' function that stops the connection with the server and exit '''


def close_window():
    root.destroy()
    os._exit(0)


''' function to take name of client as input '''


def enter_data():
    ''' take the name ofclient using the textbox '''
    number = simpledialog.askstring(
        "Input", "Enter any decimal number ?", parent=root)

    if(number):
        number = float(number)
    global upload, upload_num
    upload_num = number
    upload = 1


def download_request():
    ''' take the name ofclient using the textbox '''
    global download
    download = 1


''' set font size that is going to be used on GUI '''
myFont = font.Font(size=20)
myFont1 = font.Font(size=40)
''' dislay the name of client on GUI '''
Label(root).pack()
cname = Label(root, text="")
cname['font'] = myFont
cname.pack()
Label(root).pack()
''' button to close the client connection to server '''
btn = Button(root, text="Close connection", command=close_window)
btn['font'] = myFont
btn.pack()
''' entry box to get client name '''
en = Entry(root, textvariable=name)
en['font'] = myFont
''' set the window size to 600x600 '''
root.geometry("600x800")
Label(root).pack()
Label(root).pack()
upload = Button(root, text="Upload message", command=enter_data)
upload['font'] = myFont
upload.pack()
Label(root).pack()
Label(root).pack()
Download = Button(root, text="Download message", command=download_request)
Download['font'] = myFont
Download.pack()
''' empty label to have some space between the components on GUI '''
Label(root).pack()
message = Label(root)
message['font'] = myFont
message.pack()

''' empty label to have some space between the components on GUI '''
Label(root).pack()
Label(root).pack()
''' label to display the reverse counter on GUI '''
lab = Label(root)
lab['font'] = myFont1
''' empty label to have some space between the components on GUI '''
Label(root).pack()
lab.pack()
Label(root).pack()
''' label to display the server status and display some special '''
status = Label(root)
status['font'] = myFont
status.pack()
''' call this update function every 50 ms so it will update
the information on GUI '''


def update():
    message.config(text=data_from_server)
    if(t.code == 404):
        ''' if we got code 404 from server then just display
    the message as Server is full try again after some time '''
        cname.config(text=t.name_client)
        status.config(text="Server is full")
    elif(t.code == 201):
        ''' if we got code 201 from server then just display
    the message as Server is online '''
        cname.config(text=t.name_client)
        status.config(text="Server is online")
    elif(t.code == 200):
        ''' if we got code 200 from server then everything
    is normal with server no special instruction '''
        cname.config(text=t.name_client)
        status.config(text="Server is online")
    elif(t.code == 403):
        ''' if we got code 403 from server then client j
    ust lost a connection a with server '''
        cname.config(text=t.name_client)
        status.config(text="Server is not available at the moment")
    ''' call update function after every 50 ms '''
    root.after(50, update)


update()
''' close the server when user simply press close button '''


def doSomething():
    os._exit(0)


root.protocol('WM_DELETE_WINDOW', doSomething)
''' start the main GUI window '''
root.mainloop()
