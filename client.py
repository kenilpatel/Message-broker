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
''' this variable stores the information about download message request '''
download = 0
''' this variable stores the information about upload message request '''
upload = 0
''' this variable stores the number to upload '''
upload_num = 0
''' this variable stores the output queue from server '''
queue = ""
data_from_server = "Downloded content will get displayed here"
upload_msg = "Uploading feedback from server will get displayed here"
''' this variable stores the warning '''
warning_msg = ""
data_frame = None
''' this takes input for length in meter '''
number = StringVar()
mylist = None


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
                    global data_from_server, upload_num, queue, warning_msg, upload_msg
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
                    elif(re.search("^200*", str(msg)) != None):
                        ''' server is normally communicating with the client
                     no special instruction given by server '''
                        global download, upload
                        ''' download from server '''
                        if(download == 1):
                            download = 0
                            data = pickle.dumps("download:" + queue)
                        elif(upload == 1):
                            upload = 0
                            data = pickle.dumps(
                                "upload:" + str(upload_num) + ":" + str(queue))
                        # if nothing special then just send 200 to server
                        else:
                            data = pickle.dumps("200")
                        self.s.send(data)
                        self.conn = 1
                        self.status = "Connected"
                        self.code = 200
                    # if server send the message starting from download then display the download message to GUI
                    elif((re.search("^download-*", str(msg)) != None)):
                        x, data_from_server = msg.split("-")
                        ''' create a list of data items received'''
                        list_item = data_from_server.split("\n")
                        global mylist
                        mylist.delete(0, END)
                        ''' add items in list '''
                        for line in list_item:
                            mylist.insert(END, line)
                        data = pickle.dumps("200")
                        self.s.send(data)
                        self.conn = 1
                        self.status = "Connected"
                        self.code = 200
                     # if server send the message starting from upload then display the upload feedback to GUI
                    elif(re.search("^upload*", str(msg)) != None):
                        upload_msg = msg
                        data = pickle.dumps("200")
                        self.s.send(data)
                        self.conn = 1
                        self.status = "Connected"
                        self.code = 200

                except Exception as e:
                    ''' if anything goes wrong from server side then reset
                    the connection by setting conn to 0 and tries
                    to attempt the connection again '''
                    print(e)
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


''' function to take length as input for queue A '''


def call_a():
    global queue, upload_msg, upload, upload_num
    try:
    	# check weather the number is in proper format or not
        upload_num = float(number.get())
        ''' set queue '''
        queue = "A"
        upload = 1
        ''' display uploading message to GUI '''
        upload_msg = "Uploading " + str(upload_num) + " to A"
    except Exception as e:
    	# set warning to enter proper length
        upload_msg = "Please enter proper length"
    data_frame.destroy()


''' function to take length as input for queue B '''


def call_b():
    global queue, upload_msg, upload, upload_num
    try:
    	# check weather the number is in proper format or not
        upload_num = float(number.get())
        ''' set queue '''
        queue = "B"
        upload = 1
        ''' display uploading message to GUI '''
        upload_msg = "Uploading " + str(upload_num) + " to B"
    except Exception as e:
    	# set warning to enter proper length
        upload_msg = "Please enter proper length"
    data_frame.destroy()


''' function to take length as input for queue C '''


def call_c():
    global queue, upload_msg, upload, upload_num
    try:
    	# check weather the number is in proper format or not
        upload_num = float(number.get())
        ''' set queue '''
        queue = "C"
        upload = 1
        ''' display uploading message to GUI '''
        upload_msg = "Uploading " + str(upload_num) + " to C"
    except Exception as e:
    	# set warning to enter proper length
        upload_msg = "Please enter proper length"
    data_frame.destroy()


''' function to download from queue A '''


def call_a1():
    global queue, download
    download = 1
    queue = "A"
    data_frame.destroy()


''' function to download from queue B '''


def call_b1():
    global queue, download
    download = 1
    queue = "B"
    data_frame.destroy()


''' function to download from queue C '''


def call_c1():
    global queue, download
    download = 1
    queue = "C"
    data_frame.destroy()


''' take length as input from user to upload to server '''


def enter_data():
	# create a data frame
    global data_frame
    number.set("")
    data_frame = Toplevel()
    fnt = font.Font(size=15)
    Label(data_frame).pack()
    ''' label to display enter length '''
    label = Label(data_frame, text=t.name_client + " please enter length in meter")
    label['font'] = fnt
    label.pack()
    Label(data_frame).pack()
    ''' create entry box to take length from user '''
    en = Entry(data_frame, textvariable=number)
    en['font'] = fnt
    en.pack()
    ''' set size of data frame '''
    data_frame.geometry("400x400")
    Label(data_frame).pack()
    ''' prompt user to select queue '''
    label = Label(data_frame, text="Select Queue")
    label['font'] = fnt
    label.pack()
    Label(data_frame).pack()
    ''' create a button to select queue A '''
    A = Button(data_frame, text="A", width=20, command=call_a)
    A['font'] = fnt
    ''' create a button to select queue B '''
    B = Button(data_frame, text="B", width=20, command=call_b)
    B['font'] = fnt
    ''' create a button to select queue C '''
    C = Button(data_frame, text="C", width=20, command=call_c)
    C['font'] = fnt
    A.pack()
    Label(data_frame).pack()
    B.pack()
    Label(data_frame).pack()
    C.pack()
    data_frame.mainloop()


''' display the screen to download the content from queue '''

def download_request():
    global download
    ''' create a data frame '''
    global data_frame
    fnt = font.Font(size=15)
    number.set("")
    data_frame = Toplevel()
    ''' set a size of window '''
    data_frame.geometry("400x300")
    Label(data_frame).pack()
    ''' display the message to select queue '''
    label = Label(data_frame, text=t.name_client + " please select Queue")
    label['font'] = fnt
    label.pack()
    Label(data_frame).pack()
    Label(data_frame).pack()
    ''' create a button to select queue A '''
    A = Button(data_frame, text="A", width=20, command=call_a1)
    A['font'] = fnt
    ''' create a button to select queue B '''
    B = Button(data_frame, text="B", width=20, command=call_b1)
    B['font'] = fnt
    ''' create a button to select queue C '''
    C = Button(data_frame, text="C", width=20, command=call_c1)
    C['font'] = fnt
    A.pack()
    Label(data_frame).pack()
    B.pack()
    Label(data_frame).pack()
    C.pack()
    data_frame.mainloop()


''' set font size that is going to be used on GUI '''
myFont = font.Font(size=12)
myFont1 = font.Font(size=20)
''' dislay the name of client on GUI '''
Label(root).pack()
cname = Label(root, text="client name :- not connected")
cname['font'] = myFont
cname.pack()
Label(root).pack()
''' button to close the client connection to server '''
btn = Button(root, text="Close connection", command=close_window)
btn['font'] = myFont
btn.pack()
''' set the window size to 600x600 '''
root.geometry("600x800")
Label(root).pack()
''' button to upload message to server '''
uploadb = Button(root, text="Upload message", command=enter_data)
uploadb['font'] = myFont
''' button to download message from server '''
downloadb = Button(root, text="Check for message", command=download_request)
downloadb['font'] = myFont
''' empty label to have some space between the components on GUI '''
Label(root).pack()
''' label to display warning message '''
warning = Label(root, text="")
warning['font'] = myFont
warning.pack()
''' empty label to have some space between the components on GUI '''
Label(root).pack()
lab = Label(root)
lab['font'] = myFont1
''' label to display the server status '''
status = Label(root)
status['font'] = myFont
status.pack()

Label(root).pack()
Label(root, text="-----------------------------------------------------------------------").pack()
Label(root).pack()
Label(root).pack()
''' label to display the upload message status '''
message1 = Label(root, text="")
message1['font'] = myFont
message1.pack()
Label(root).pack()
Label(root).pack()
Label(root, text="-----------------------------------------------------------------------").pack()
Label(root).pack()
Label(root).pack()
''' label to display the download message status '''
message = Label(root, text="Messages")
message['font'] = myFont
message.pack()
Label(root).pack()
''' scrollable display to show queue messages '''
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
mylist = Listbox(root, yscrollcommand=scrollbar.set)
mylist.pack(fill=BOTH)
scrollbar.config(command=mylist.yview)
''' empty label to have some space between the components on GUI '''
Label(root).pack()

''' call this update function every 50 ms so it will update
the information on GUI '''
def update():
    message1.config(text=upload_msg)
    if(t.code == 404):
        ''' if we got code 404 from server then just display
    the message as Server is full try again after some time '''
        warning.config(text=warning_msg)
        cname.config(text="client name :- not connected")
        status.config(text="Server is full")
        uploadb.pack_forget()
        downloadb.pack_forget()
    elif(t.code == 201):
        ''' if we got code 201 from server then just display
    the message as Server is online '''
        warning.config(text=warning_msg)
        cname.config(text="client name :- " + t.name_client)
        status.config(text="Server is online")
        uploadb.pack()
        downloadb.pack()
    elif(t.code == 200):
        ''' if we got code 200 from server then everything
    is normal with server no special instruction '''
        warning.config(text=warning_msg)
        cname.config(text="client name :- " + t.name_client)
        status.config(text="Server is online")
        uploadb.pack()
        downloadb.pack()
    elif(t.code == 403):
        ''' if we got code 403 from server then client j
    ust lost a connection a with server '''
        warning.config(text=warning_msg)
        cname.config(text="client name :- not connected")
        status.config(text="Server is not available at the moment")
        uploadb.pack_forget()
        downloadb.pack_forget()
    root.after(50, update)


update()
''' close the server when user simply press close button '''


def doSomething():
    os._exit(0)


root.protocol('WM_DELETE_WINDOW', doSomething)
''' start the main GUI window '''
root.mainloop()
