#python version 3.7.3
from socket import *
import sys
import threading
import time
import datetime as dt
import os



#t_lock=threading.Condition()

def identify_user(login_data):
    f = open("credentials.txt", "a+")
    f.seek(0)
    file_data = f.readlines()
    check = 0
    for item in file_data:
        info = item.split(' ',1)
        #already registered
        if info[0] == login_data[0]:
            check = 1
            break
    f.close()
    return check

def check_password(login_data):
    f = open("credentials.txt", "a+")
    f.seek(0)
    file_data = f.readlines()
    check = 0
    for item in file_data:
        info = item.split(' ',1)
        
        #already registered
        if info[0] == login_data[0]:
            if info[1] == login_data[1] + '\n':
                check = 1
                break
            if info[1] == login_data[1]:
                check = 1
                break
    f.close()
    return check

def register_user(login_data):
    f = open("credentials.txt", "a+")
    f.write("\n")
    f.write(login_data[0]+" ")
    f.write(login_data[1])
    f.close()

def already_login(login_data):
    f = open("login.txt","a+")
    f.seek(0)
    file_data = f.readlines()
    check = 0
    for item in file_data:
        #already logged in
        if item == login_data[0] + "\n":
            check = 1
            break
    #if check == 0:
        #f.write(login_data[0] + "\n")
    f.close()
    return check

def client_login(login_data, connect_socket):
    reg_text = "registration success, welcome to the forum"
    success_text = "Welcome to the forum"
    fail_text = "Incorrect password"
    identify_text = "Enter password"
    register_text = "Start register"
    if already_login(eval(login_data)) == 1:
        connect_socket.send("already logged in".encode())
        print("depulicate login")
    elif identify_user(eval(login_data)) == 1:        
        connect_socket.send(identify_text.encode())
        messagerecv = connect_socket.recv(1024)
        login_data = messagerecv.decode("utf-8") 
        login_data = eval(login_data.split(" ",1)[1])
        if check_password(login_data) == 1:
            f = open("login.txt","a+")
            f.write(login_data[0] + "\n")
            f.close()
            print(login_data[0] + " successfully logged in")
            connect_socket.send(success_text.encode())
        else:
            print(fail_text)
            connect_socket.send(fail_text.encode())
    else:
        print("New user")
        connect_socket.send(register_text.encode())
        messagerecv = connect_socket.recv(1024)
        login_data = messagerecv.decode("utf-8")
        login_data = eval(login_data.split(" ",1)[1])
        register_user(login_data)
        f = open("login.txt","a+")
        f.write(login_data[0] + "\n")
        f.close()
        print(login_data[0] + " successfully logged in")
        connect_socket.send(reg_text.encode())

def client_logout(logout_data, connect_socket):
    logout_data = eval(logout_data)
    print(logout_data[0] + " exited")
    f = open("login.txt", "r")
    file_data = f.readlines()
    f.close()
    counter = 0
    for data in file_data:
        if data == logout_data[0] + "\n":
            del file_data[counter]
            break
        counter = counter + 1
    new_f = open("login.txt","w+")
    for data in file_data:
        new_f.write(data)       
    new_f.close()
    


def client_CRT(CRT_data, connect_socket):   
    success_text = "success create thread"
    fail_text = "fail create thread"
    user_name = CRT_data.split(" ",1)[0]
    thread_title = CRT_data.split(" ",1)[1]
    print(user_name + " issued CRT command")
    if os.path.isfile('./' + str(thread_title)) == True:
        print("Thread" + " " + thread_title + " " + "exists")
        connect_socket.send(fail_text.encode())
    else:
        print("Thread" + " " + thread_title + " " + "created")
        f = open(str(thread_title), "w+")
        f.write(str(user_name) + "\n")
        f.close()
        connect_socket.send(success_text.encode())

def client_MSG(MSG_data, connect_socket):
    success_text = "success post"
    fail_text = "fail post"
    thread_title = MSG_data.split(" ",2)[0]
    user_name = MSG_data.split(" ",2)[1]
    user_mess = MSG_data.split(" ",2)[2]
    print(user_name + " issued MSG command")
    if os.path.isfile('./' + str(thread_title)) == True:
        print("Message posted to " + thread_title + " thread")
        #get num
        f = open(str(thread_title), "r")
        counter = 1
        file_data = f.readlines()
        for item in file_data:
            if item.split(" ",1)[0].isnumeric():
                counter = counter + 1
        f.close()
        #write
        f = open(str(thread_title), "a+")
        f.write(str(counter) + " " + user_name + ": " + user_mess)
        f.write("\n")
        f.close()
        connect_socket.send(success_text.encode())
    else:
        print("Message cannot be posted")
        connect_socket.send(fail_text.encode())


def client_DLT(DLT_data, connect_socket):
    success_text = "success delete"
    failthread_text = "fail delete cause of thread"
    failuser_text = "fail delete cause of user"
    failnum_text = "fail delete cause of mess num"    
    thread_title = DLT_data.split(" ",2)[0]
    user_name = DLT_data.split(" ",2)[1]
    mess_num = DLT_data.split(" ",2)[2]
    print(user_name + " issued DLT command")
    #check thread_title/user/message number
    check_num = 0
    check_user = 0
    counter = 0
    if os.path.isfile('./' + str(thread_title)) == True:
        f = open(str(thread_title), "r")
        file_data = f.readlines()
        f.close()
        for item in file_data:
            item_num = item.split(" ",1)[0]            
            if item_num == mess_num: 
                item_user = item.split(" ",2)[1]
                check_num = 1               
                if item_user == user_name + ":":                  
                    check_user = 1                  
                    del file_data[int(counter)]
                    break
            counter = counter + 1
        #pass all check, rewrite file
        if check_num == 1 and check_user == 1:                   
            new_f = open(str(thread_title),"w+")
            for item in file_data:
                item_num = item.split(" ",1)[0]
                #the thread creator
                if item == file_data[0]:
                    new_f.write(str(item))
                    continue
                #any upload
                elif item.split(" ",2)[1] == "uploaded":
                    new_f.write(str(item))
                    continue
                elif int(item_num) > int(mess_num):
                    item_num = str(int(item_num)-1) 
                    new_f.write(item_num + " " + item.split(" ",2)[1] + " " + item.split(" ",2)[2])
                else:
                    new_f.write(str(item))
            new_f.close()
            print("Message has been deleted")
            connect_socket.send(success_text.encode())
        #fail username check
        elif check_num == 1 and check_user == 0:
            print("Message can not be deleted")
            connect_socket.send(failuser_text.encode())
        #fail message number/username check
        elif check_num == 0 and check_user == 0:
            print("Message can not be deleted")
            connect_socket.send(failnum_text.encode())  
    #fail thread_title check   
    else:
        print("Message can not be deleted")
        connect_socket.send(failthread_text.encode())

def client_EDT(EDT_data, connect_socket):
    success_text = "success edit"
    failthread_text = "fail edit cause of thread"
    failuser_text = "fail edit cause of user"
    failnum_text = "fail edit cause of mess num"  
    thread_title = EDT_data.split(" ",1)[0]
    user_name = EDT_data.split(" ",2)[1]
    mess_num = EDT_data.split(" ",3)[2]
    new_mess = EDT_data.split(" ",3)[3]
    print(user_name + " issued EDT command")
    #check thread_title/user/message number
    check_num = 0
    check_user = 0
    counter = 0
    if os.path.isfile('./' + str(thread_title)) == True:
        f = open(str(thread_title), "r")
        file_data = f.readlines()
        f.close()
        for item in file_data:
            item_num = item.split(" ",1)[0]            
            if item_num == mess_num: 
                item_user = item.split(" ",2)[1]
                check_num = 1               
                if item_user == user_name + ":":                 
                    check_user = 1                  
                    file_data[counter] = str(mess_num) + " " + str(user_name) + ": " + new_mess + "\n"
                    break
            counter = counter + 1
        #pass all check, rewrite file
        if check_num == 1 and check_user == 1:                   
            new_f = open(str(thread_title),"w+")
            for item in file_data:
                new_f.write(str(item))
            new_f.close()
            print("Message has been edited")
            connect_socket.send(success_text.encode())
        #fail username check
        elif check_num == 1 and check_user == 0:
            print("Message cannot be edited")
            connect_socket.send(failuser_text.encode())
        #fail message number/username check
        elif check_num == 0 and check_user == 0:
            print("Message cannot be edited")
            connect_socket.send(failnum_text.encode())  
    #fail thread_title check   
    else:
        print("Message cannot be edited")
        connect_socket.send(failthread_text.encode())
    
    
def client_LST(LST_data, connect_socket):
    faillist_text = "fail list threads"
    #successlist_text = "success list threads"
    print(str(LST_data) + " issued LST command")
    files = os.listdir('.')
    files.remove("credentials.txt")
    files.remove("login.txt")
    #files.remove("client.py")
    files.remove("server.py")
    for data in files:
        if '-' in data:
            files.remove(data)
    if len(files) != 0:
        connect_socket.send(str(files).encode())
    else:
        connect_socket.send(faillist_text.encode())



def client_RDT(RDT_data, connect_socket):
    fail_empty = "fail read thread empty"
    fail_exist = "fail read thread not exist"
    #success_text = "success read thread"
    user_name = RDT_data.split(" ",1)[0]
    thread_title = RDT_data.split(" ",1)[1]
    print(str(user_name) + " issued RDT command")
    if os.path.isfile('./' + str(thread_title)) == True:
        f = open(str(thread_title), "r")
        file_data = f.readlines()
        f.close()
        if len(file_data) <= 1:
            print("Thread " + str(thread_title) + " nothing to read")
            connect_socket.send(fail_empty.encode())    
        else:
            print("Thread " + str(thread_title) + " read")
            del file_data[0]
            connect_socket.send(str(file_data).encode()) 
    else:
        print("Incorrect thread specified")
        connect_socket.send(fail_exist.encode())
 
def client_SHT(SHT_data, connect_socket):
    check = 0
    success_text = "success shut down"
    fail_text = "fail shut down"
    user_name = SHT_data.split(" ",1)[0]
    check_pass = SHT_data.split(" ",1)[1]
    print(str(user_name) + " issued SHT command")
    if str(check_pass) == str(admin_passwd):
        print("Server shutting down")
        files = os.listdir('.')
        files.remove("server.py")
        for item in files:
            os.remove(item)
        check = 1
    return check

def client_RMV(RMV_data, connect_socket):
    fail_exist = "thread not exist"
    fail_creator = "thread creator"
    success_text = "remove success"
    user_name = RMV_data.split(" ",1)[0]
    thread_title = RMV_data.split(" ",1)[1]
    print(str(user_name) + " issued RMV command")
    if os.path.isfile('./' + str(thread_title)) == True:
        f = open(str(thread_title), "r")
        file_data = f.readlines()
        f.close()
        if file_data[0].rstrip("\n") == str(user_name):
            os.remove(str(thread_title))
            print("Thread " + str(thread_title) + " removed")
            connect_socket.send(success_text.encode())    
        else:
            print("Thread " + str(thread_title) + " cannot be removed")
            connect_socket.send(fail_creator.encode()) 
    else:
        print("Incorrect thread specified")
        connect_socket.send(fail_exist.encode())

def client_UPD(UPD_data, connect_socket):
    notexist_text = "thread not exist"
    success_text = "upload success"
    samefile_text = "same name file"
    thread_title = UPD_data.split(" ",1)[0]
    user_name = UPD_data.split(" ",3)[1]
    file_name = UPD_data.split(" ",3)[2]


    messrecv = connect_socket.recv(1024) 
    while not messrecv.endswith(b'\n\nComplete'):
        mess_more = connect_socket.recv(1024)
        messrecv = messrecv + mess_more
    file_data = messrecv.split(b'\n\nComplete')[0]

    print(str(user_name) + " issued UPD command")
    if os.path.isfile('./' + str(thread_title)) == True:
        if os.path.isfile('./' + str(thread_title) + "-" + str(file_name)) == True:
            print("Already have same name file")
            connect_socket.send(samefile_text.encode())
        else:
            with open(str(thread_title) + "-" + str(file_name),'wb') as file_to_write:
                file_to_write.write(file_data)
            file_to_write.close()
            connect_socket.send(success_text.encode())
            print("success upload file")
            #add entry to thread
            f = open(str(thread_title), "a+")
            f.write(str(user_name) + " uploaded " + str(file_name))
            f.write("\n")
            f.close()
    if os.path.isfile('./' + str(thread_title)) != True:
        connect_socket.send(notexist_text.encode())

def client_DWN(DWN_data, connect_socket):
    filenot_exist = "file not found"
    threadnot_exist = "thread not exist"
    thread_title = DWN_data.split(" ",1)[0]
    user_name = DWN_data.split(" ",2)[1]
    file_name = DWN_data.split(" ",2)[2]
    print(str(user_name) + " issued DWN command")    
    if os.path.isfile('./' + str(thread_title)) == True:
        if os.path.isfile('./' + str(thread_title) + "-" + str(file_name)) == True:
            #pass check
            with open(str(thread_title) + "-" + str(file_name),'rb') as file_to_send:
                for data in file_to_send:
                    connect_socket.sendall(data)
            connect_socket.send("\n\nComplete".encode())
            print("file has transfered to " + str(user_name))
        else:
            print("download fail")
            connect_socket.send(b'file not found')
    else:
        print("download fail")
        connect_socket.send(b'thread not exist')
        



   

def recv_handler(connect_socket):
    global servershutdown
    while servershutdown == False:
        messagerecv = connect_socket.recv(1024)
        client_command = messagerecv.decode()
        if client_command.split(" ",1)[0] == "Login":
            client_login(client_command.split(" ",1)[1], connect_socket)
        if client_command.split(" ",1)[0] == "Logout":
            client_logout(client_command.split(" ",1)[1], connect_socket)
            break
        if client_command.split(" ",1)[0] == "CRT":
            client_CRT(client_command.split(" ",1)[1], connect_socket)
        if client_command.split(" ",1)[0] == "MSG":
            client_MSG(client_command.split(" ",1)[1], connect_socket)
        if client_command.split(" ",1)[0] == "DLT":
            client_DLT(client_command.split(" ",1)[1], connect_socket)
        if client_command.split(" ",1)[0] == "EDT":
            client_EDT(client_command.split(" ",1)[1], connect_socket)
        if client_command.split(" ",1)[0] == "LST":
            client_LST(client_command.split(" ",1)[1], connect_socket)
        if client_command.split(" ",1)[0] == "RDT":
            client_RDT(client_command.split(" ",1)[1], connect_socket)
        if client_command.split(" ",1)[0] == "SHT":
            check = client_SHT(client_command.split(" ",1)[1], connect_socket)
            if check == 1:
                connect_socket.send(str("success shut down").encode())
                servershutdown = True
                break 
            else:
                print("Incorrect admin password")
                connect_socket.send(str("fail shut down").encode())
        if client_command.split(" ",1)[0] == "RMV":
            client_RMV(client_command.split(" ",1)[1], connect_socket)
        if client_command.split(" ",1)[0] == "UPD":
            client_UPD(client_command.split(" ",1)[1], connect_socket)
        if client_command.split(" ",1)[0] == "DWN":
            client_DWN(client_command.split(" ",1)[1], connect_socket)
    connect_socket.close()
    

        


server_port = int(sys.argv[1])
admin_passwd = sys.argv[2]
#create a socket object
server_socket = socket(AF_INET, SOCK_STREAM)
#bind the socket
server_socket.bind(('localhost', server_port))
#put sys to listen mode
server_socket.listen(3)
print("Waiting for clients")
servershutdown = False
server_socket.settimeout(0.6)
while servershutdown == False:
    try:
        #establish connection with client
        c, addr = server_socket.accept()
        print("Client connected")
        #set thread
        client_thread = threading.Thread(name = "client_thread", target = recv_handler, args = (c,), daemon = True)
        client_thread.start()
    except timeout:
        pass

server_socket.close()




