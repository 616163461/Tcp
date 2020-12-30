#python version 3.7.3
from socket import *
import sys
import threading
import os

login_data = []


def login_prompt():
    global login_data
    login_data.clear()
    username = input("Enter username: ")
    login_data.append(username)
    return login_data

def login(client_socket):
    login_data = login_prompt()
    while True:
        if len(login_data) != 1:
            print("Incorrect username format")
            login_data = login_prompt()
            continue
        sendmess_server = "Login" + " " + str(login_data)
        client_socket.send(sendmess_server.encode())
        messagerecv = client_socket.recv(1024)
        mess = messagerecv.decode()
        if mess == "already logged in":
            print("already logged in")
            login_data = login_prompt()
            continue
        if mess == "Enter password":
            userpass = input("Enter password: ")
            login_data.append(userpass)
            sendmess_server = "Login" + " " + str(login_data)
            client_socket.send(sendmess_server.encode())
            messagerecv = client_socket.recv(1024)
            mess = messagerecv.decode()
            if mess == "Welcome to the forum":
                print(mess)
                break
            if mess == "Incorrect password":
                print("Invalid password")
                login_data = login_prompt()
                continue
        
        if mess == "Start register":
            userpass = input("Enter password for " + login_data[0] + ": ")
            login_data.append(userpass)
            sendmess_server = "Login" + " " + str(login_data)
            client_socket.send(sendmess_server.encode())
            messagerecv = client_socket.recv(1024)
            mess = messagerecv.decode()
            if mess == "registration success, welcome to the forum":
                break

def logout(client_socket):
    global login_data
    sendmess_server = "Logout" + " " + str(login_data)
    client_socket.send(sendmess_server.encode())
    print("Goodbey")



def create_thread(thread_name,client_socket):
    sendmess_server = "CRT" + " " + str(login_data[0]) + " " + str(thread_name)
    client_socket.send(sendmess_server.encode())
    messagerecv = client_socket.recv(1024)
    mess = messagerecv.decode()
    if mess == "success create thread":
        print("Thread" + " " + str(thread_name) + " " + "created")
    elif mess == "fail create thread":
        print("Thread" + " " + str(thread_name) + " " + "exists")
    else:
        print("error")
        
def append_message(mess_info,client_socket):
    thread_name = mess_info.split(" ",1)[0]
    send_message = mess_info.split(" ",1)[1]
    sendmess_server = "MSG" + " " + str(thread_name) + " " + str(login_data[0]) + " " + str(send_message) 
    client_socket.send(sendmess_server.encode())
    messagerecv = client_socket.recv(1024)
    mess = messagerecv.decode()
    if mess == "success post":
        print("Message posted to " + str(thread_name) + " thread")
    elif mess == "fail post":
        print("Message posted to " + str(thread_name) + " thread failed, thread not exist")
    else:
        print("error")

def delete_message(mess_info,client_socket):
    thread_name = mess_info.split(" ",1)[0]
    message_num = mess_info.split(" ",1)[1]
    sendmess_server = "DLT" + " " + str(thread_name) + " " + str(login_data[0]) + " " + str(message_num)
    client_socket.send(sendmess_server.encode())
    messagerecv = client_socket.recv(1024)
    mess = messagerecv.decode()
    if mess == "success delete":
        print("The message has been deleted")
    elif mess == "fail delete cause of thread":
        print("The message is not deleted, check thread name")
    elif mess == "fail delete cause of user":
        print("The message belongs to another user and cannot be deleted")
    elif mess == "fail delete cause of mess num":
        print("The message is not deleted, check message number")
    else:
        print("error")

def edit_message(mess_info,client_socket):
    thread_name = mess_info.split(" ",1)[0]
    message_num = mess_info.split(" ",2)[1]
    new_mess = mess_info.split(" ",2)[2]
    sendmess_server = "EDT" + " " + str(thread_name) + " " + str(login_data[0]) + " " + str(message_num) + " " + str(new_mess)
    client_socket.send(sendmess_server.encode())
    messagerecv = client_socket.recv(1024)
    mess = messagerecv.decode()
    if mess == "success edit":
        print("The message has been edited")
    elif mess == "fail edit cause of thread":
        print("The message can not edit, check thread name")
    elif mess == "fail edit cause of user":
        print("The message belongs to another user and cannot be edited")
    elif mess == "fail edit cause of mess num":
        print("The message can not edit, check message number")
    else:
        print("error")

def list_thread(client_socket):
    sendmess_server = "LST" + " " + str(login_data[0])
    client_socket.send(sendmess_server.encode())
    messagerecv = client_socket.recv(1024)
    mess = messagerecv.decode()
    if mess == "fail list threads":
        print("No threads to list")
    else:
        #messagerecv = client_socket.recv(1024)
        #mess = messagerecv.decode('utf-8')
        print("The list of active threads:")
        mess = eval(mess)
        for item in mess:
            print(item)


def read_thread(thread_name,client_socket):
    sendmess_server = "RDT" + " " + str(login_data[0]) + " " + str(thread_name)
    client_socket.send(sendmess_server.encode())
    messagerecv = client_socket.recv(1024)
    mess = messagerecv.decode()
    if mess == "fail read thread empty":
        print(str(thread_name) + " is empty")
    elif mess == "fail read thread not exist":
        print(str(thread_name) + " not exist")    
    else:
        #messagerecv = client_socket.recv(1024)
        #mess = messagerecv.decode('utf-8')
        mess = eval(mess)
        for item in mess:
            print(item.strip("\n"))


def close_server(admin_pass,client_socket):
    sendmess_server = "SHT" + " " + str(login_data[0]) + " " + str(admin_pass)
    client_socket.send(sendmess_server.encode())
    messagerecv = client_socket.recv(1024)
    mess = messagerecv.decode()
    if mess == "fail shut down":
        print("Incorrect admin password")
    elif mess == "success shut down":
        print("Goodbye. Server shutting down")
        client_socket.close()
        exit(1)
    else:
        print("error")

def remove_thread(thread_name,client_socket):
    sendmess_server = "RMV" + " " + str(login_data[0]) + " " + str(thread_name)
    client_socket.send(sendmess_server.encode())
    messagerecv = client_socket.recv(1024)
    mess = messagerecv.decode()
    if mess == "thread not exist":
        print(str(thread_name) + " not exist")
    elif mess == "thread creator":
        print("The thread was created by another user and cannot be removed")
    elif mess == "remove success":
        print("The thread has been removed")
    else:
        print("error")

def upload_file(file_info,client_socket):
    thread_name = file_info.split(" ",1)[0]
    file_name = file_info.split(" ",1)[1]
    sendmess_server = "UPD" + " " + str(thread_name) + " " + str(login_data[0]) + " " + str(file_name)
    client_socket.send(sendmess_server.encode())
    with open(file_name,'rb') as file_to_send:
        for data in file_to_send:
            client_socket.sendall(data)
    client_socket.send("\n\nComplete".encode())
    messagerecv = client_socket.recv(1024)
    mess = messagerecv.decode()
    if mess == "thread not exist":
        print("Thread not exist, upload file fail")
    elif mess == "same name file":
        print("File already uploaded")
    elif mess == "upload success":
        print(str(file_name) + " uploaded to " + str(thread_name))
    else:
        print("Upload file fail")

def download_file(file_info,client_socket):
    thread_name = file_info.split(" ",1)[0]
    file_name = file_info.split(" ",1)[1]
    sendmess_server = "DWN" + " " + str(thread_name) + " " + str(login_data[0]) + " " + str(file_name)
    client_socket.send(sendmess_server.encode())
    mess = client_socket.recv(1024)
    if mess == b'thread not exist':
        print("Thread not exist, download file fail")
    elif mess == b'file not found':
        print("File not found, download file fail")
    else:
        while True:
            if mess.endswith(b'\n\nComplete'):
                break
            morerecv = client_socket.recv(1024)
            mess = mess + morerecv
        with open(str(file_name),'wb') as file_to_write:
            file_to_write.write(mess.split(b'\n\nComplete')[0])
        file_to_write.close()
        print("file has download from server")







def check_space(command):
    if command.startswith(" "):
        print("(extra space added before user's response)")
        command = command.lstrip()
    return command

ip_server = sys.argv[1]
port_server = sys.argv[2]
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((ip_server, int(port_server)))
#firstly login
login(client_socket)
#after login
while True:
    try: 
        command = input("Enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT, SHT: ")
        command = check_space(command)
        command_list = command.split(" ",1)
        if command_list[0] == "XIT":
            if len(command.split()) != 1:
                print("Invalid command, wrong number of command")
                continue
            logout(client_socket)
            break
        elif command_list[0] == "CRT":
            if len(command.split()) == 1:
                print("Invalid command, wrong number of command")
                continue
            if len(command_list[1].split()) != 1:
                print("Invalid command, wrong length of thread name")
                continue
            if command_list[1].startswith(" ") or command_list[1].endswith(" "):
                print("Extra space for thread name")
                continue
            create_thread(command_list[1],client_socket)
        elif command_list[0] == "MSG":
            if len(command.split()) < 3:
                print("Invalid command, wrong number of command")
                continue
            append_message(command_list[1],client_socket)
        elif command_list[0] == "DLT":
            if len(command.split()) != 3:
                print("Invalid command, wrong number of command")
                continue
            if command_list == command.split(" ",2)[2] == 0:
                print("Invalid command, wrong number of message")
                continue
            delete_message(command_list[1],client_socket)
        elif command_list[0] == "EDT":
            if len(command.split()) < 4:
                print("Invalid command, wrong number of command")
                continue
            if command_list == command.split(" ",3)[2] == 0:
                print("Invalid command, wrong number of message")
                continue
            edit_message(command_list[1],client_socket)
        elif command_list[0] == "LST":
            if len(command.split()) != 1:
                print("Invalid command, wrong number of command")
                continue
            list_thread(client_socket)
        elif command_list[0] == "RDT":
            if len(command.split()) != 2:
                print("Invalid command, wrong number of command")
                continue
            read_thread(command_list[1],client_socket)
        elif command_list[0] == "SHT":
            if len(command.split()) != 2:
                print("Invalid command, wrong number of command")
                continue
            close_server(command_list[1],client_socket)
        elif command_list[0] == "RMV":
            if len(command.split()) != 2:
                print("Invalid command, wrong number of command")
                continue
            remove_thread(command_list[1],client_socket)
        elif command_list[0] == "UPD":
            if len(command.split()) != 3:
                print("Invalid command, wrong number of command")
                continue
            if len(command.split(" ",2)[2].split()) != 1:
                print("Invalid command, wrong length of the file name")
                continue
            if os.path.isfile('./' + str(command.split(" ",2)[2])) != True:
                print("upload file not found")
                continue
            upload_file(command_list[1],client_socket)
        elif command_list[0] == "DWN":
            if len(command.split()) != 3:
                print("Invalid command, wrong number of command")
                continue
            if len(command.split(" ",2)[2].split()) != 1:
                print("Invalid command, wrong length of the file name")
                continue
            download_file(command_list[1],client_socket)
        else:
            print("Invalid command")
    except timeout:
        pass
client_socket.close()



