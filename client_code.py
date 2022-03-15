#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

# we would like to start a host and a port number
HOST = '127.0.0.1'
PORT = 6666

#colors to use during the note
Dark_beige = '#EED5B7'
Medium_beige = '#FFE4C4'
Crimson = '#DC143C'
Font_color = "#000000"
Font = ("Times New Roman", 12)
Button_font = ("Times New Roman", 15)
small_font = ("Times New Roman", 13)

# Creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#to add the message into the message box
def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
        username_textbox.delete(0, len(username))
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

root = tk.Tk()
root.geometry("600x600") #set the size of the messenger
root.title("YouChat") #rename the messenger
root.resizable(False, False) #disable the window from being resized to avoid problems

#set the size of our sections
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

#divide our messenger into 3 sections
section1 = tk.Frame(root, width=600, height=100, bg=Dark_beige, cursor='dot')
section1.grid(row=0, column=0, sticky=tk.NSEW)

section2 = tk.Frame(root, width=600, height=300, bg=Medium_beige,cursor='dot')
section2.grid(row=1, column=0, sticky=tk.NSEW)

section3 = tk.Frame(root, width=600, height=100, bg=Dark_beige ,cursor='dot')
section3.grid(row=2, column=0, sticky=tk.NSEW) 

username_label = tk.Label(section1, text="Enter username:", font=Font, bg=Dark_beige, fg=Font_color)
username_label.pack(side=tk.LEFT, padx=2)

username_textbox = tk.Entry(section1, font=Font, bg=Medium_beige, fg=Font_color, width=30)
username_textbox.pack(side=tk.LEFT, padx=10)

username_button = tk.Button(section1, text="Join", font=Button_font, bg=Crimson, fg='white', command=connect)
username_button.pack(side=tk.RIGHT, padx=10)

def remove_label():
    username_label.after(1, username_label.destroy())
    username_button.after(1, username_button.destroy())
    username_textbox.after(1, username_textbox.destroy())
    username_button1.after(1, username_button1.destroy())
    message_button = tk.Button(section3, text="Send", font=Button_font, bg=Crimson, fg='white', command=send_message)
    message_button.pack(side=tk.LEFT, padx=10)

username_button1 = tk.Button(section1, text="Start Chatting", font=Button_font, bg=Crimson, fg='white', command=remove_label)
username_button1.pack(side=tk.RIGHT, padx=10)

message_textbox = tk.Entry(section3, font=Font, bg=Medium_beige, fg=Font_color, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(section2, font=small_font, bg=Medium_beige, fg=Font_color, width=66, height=30)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

# main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




