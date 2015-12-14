#!/usr/bin/env python
from socket import *
from threading import Thread
import threading, time
ver = '1.12.14'

def send_user_list(s,conn,data):
    sendlist = ''
    for x in threadip:
        sendlist+= str(x[2]+'\n')
    if data is not '':
        broadcastData(s, conn,'SSERVER::'+data[9:]+' joined')
    time.sleep(0.5)
    broadcastData(s, conn,'USRLIST::'+sendlist[:-2])

def recieveData(s, conn):# function to recieve data
    try:
        data = conn.recv(1024) # conn.recv(1024) waits for data of 1024 or less bytes and stores it in data
        print conn, data, "\n" # print the connection and data sent
    except:
        data = 'close::'
    return data; # returns the contents of data

def broadcastData(s, conn, data): # function to send Data
##    conn.sendall(data)  # sends data received to connection
    for x in threadip:
        try:
            x[1].sendall(data)
        except:
            print x[1],' NOT AVAILABLE\n'
    print "Data sent to all clients \n"  # print to inform data was went


def clientHandler(i):
    print 'Thread ',i,' started'
    global s, threadip
    username,username_set = '',False
    conn, addr = s.accept() # awaits for a client to connect and then accepts
    print addr, " is now connected! \n" # telling us a client is connected and address
    threadip.append([str(i),conn])
    conn.sendall('SSERVER::Welcome to inSecure Plain Text Chat - ver: '+ver)
    while 1:
        data = recieveData(s, conn)
        if not data:
            cnt = 0
            for x in threadip:
                b = x[0].find(str(i))
                if b is not -1:
                    del threadip[cnt]
                cnt+=1
            send_user_list(s,conn,'')
            time.sleep(1)
            broadcastData(s, conn, 'SSERVER::'+username+' left')
            Thread(target=clientHandler,args=(i,)).start()
            break
        elif data == 'close::':
            cnt = 0
            for x in threadip:
                b = x[0].find(str(i))
                if b is not -1:
                   del threadip[cnt]
                cnt+=1
            send_user_list(s,conn,'')
            time.sleep(1)
            broadcastData(s, conn, 'SSERVER::'+username+' left')
            Thread(target=clientHandler,args=(i,)).start()
            break
        elif data[0:9] == 'USRINFO::':
            oldusername = str(username)
            for x in oldusername:
                if x == ' ':
                    oldusername = oldusername[1:]
                else:
                    pass
            if len(data) > 11:
                username = data[9:]
                if len(username) < 15:
                    for x in range(0,15-len(username)):
                        username = ' '+username
                else:
                    username = username[15:]
                if username_set is True:
                    for x in threadip:
                        b = x[0].find(str(i))
                        if b is not -1:
                            x[2] = data[9:]
                            send_user_list(s,conn,data)
                else:
                    for x in threadip:
                        b = x[0].find(str(i))
                        if b is not -1:
                            x.append(data[9:])
                            send_user_list(s,conn,data)
                username_set = True
        else:
            broadcastData(s, conn, username+': '+data)

action_time = True
threadip = []
def main(): # main function
    global s, action_time
    s = socket(AF_INET, SOCK_STREAM) # creates our socket; TCP socket
    s.bind(('', 8001)) # tells the socket to bind to localhost on port 8000
        # 'localhost'
        # ''
        # "127.0.0.1"
    s.listen(10) # number of connections listening for
    print "Server is running...... \n"

    for i in range(1,8):
        Thread(target=clientHandler,args=(i,)).start()
    while action_time is True:
        msg = raw_input('::: ')
        msg = str(msg)
        if msg == 'quit':
            s.close()
            action_time = False
            print action_time
        elif msg == 'thread':
            print threading.active_count()
        else:
            print msg

main() # calls up out main function
