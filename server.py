#!/usr/bin/env python
from socket import *
from threading import Thread
import threading, time
ver = '1.12.13'

def remove_spaces(username):
    for x in username:
        if x == ' ':
            username = username[1:]
        else:
            pass
    return username

def get_list_len(llist):
    cnt = 0
    for x in llist:
        cnt+=1
        print cnt
    return cnt

def send_user_list(s,conn,oldusername,username):
    if oldusername is not '':
        oldusername = remove_spaces(oldusername)
    if username is not '':
        username = remove_spaces(username)
    sendlist = ''
    for x in threadip:
        sendlist+= str(x[2]+'\n')
    if username is not '':
        if oldusername is not '':
            broadcastData(s, conn,'SSERVER::'+oldusername+' is now '+username)
        else:
            broadcastData(s, conn,'SSERVER::'+username+' joined')
    time.sleep(0.5)
    broadcastData(s, conn,'USRLIST::'+sendlist[:-1])

def recieveData(s, conn):# function to recieve data
    try:
        data = conn.recv(1024) # conn.recv(1024) waits for data of 1024 or less bytes and stores it in data
##        print conn, data, "\n" # print the connection and data sent
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
##    print "Data sent to all clients \n"  # print to inform data was went


def clientHandler(i):
    global s, threadip, threads
    username,username_set = '',False
    conn, addr = s.accept() # awaits for a client to connect and then accepts 
    print addr," is now connected! \n"
    threadip.append([str(i),conn])
    conn.sendall('SSERVER::Welcome to inSecure Plain Text Chat - ver: '+ver)
    while 1:
        data = recieveData(s, conn)
        ##Normal messages
        if data[0:9] == 'MESSAGE::':
            broadcastData(s, conn, username+': '+data[9:])
        ## Leaving
        if not data:
            cnt = 0
            for x in threadip:
                b = x[0].find(str(i))
                if b is not -1:
                    del threadip[cnt]
                cnt+=1
            send_user_list(s,conn,'','')
            time.sleep(1)
            username2 = remove_spaces(username)
            broadcastData(s, conn, 'SSERVER::'+username2+' left')
            print addr," is now disconnected! \n"
            Thread(target=clientHandler,args=(i,)).start()
            break
        ## Leaving
        elif data == 'close::':
            cnt = 0
            for x in threadip:
                b = x[0].find(str(i))
                if b is not -1:
                   del threadip[cnt]
                cnt+=1
            send_user_list(s,conn,'','')
            time.sleep(1)
            username2 = remove_spaces(username)
            broadcastData(s, conn, 'SSERVER::'+username2+' left')
            print addr," is now disconnected! \n"
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
                    username = username[:15]
                ## Username gets changed
                if username_set is True:
                    for x in threadip:
                        b = x[0].find(str(i))
                        if b is not -1:
                            username2 = remove_spaces(username)
                            x[2] = username2
                            send_user_list(s,conn,oldusername,username)
                ## Login username received
                else:
                    for x in threadip:
                        b = x[0].find(str(i))
                        if b is not -1:
                            username2 = remove_spaces(username)
                            x.append(username2)
                            send_user_list(s,conn,'',username)
                username_set = True
        
threads = 10
action_time = True
threadip = []
def main(): # main function
    global s, action_time
    s = socket(AF_INET, SOCK_STREAM) # creates our socket; TCP socket
    s.bind(('', 8001)) # tells the socket to bind to localhost on port 8000
        # 'localhost'
        # ''
        # "127.0.0.1"
    s.listen(threads) # number of connections listening for
    print "Server is running...... \n"

    for i in range(1,1+threads):
        Thread(target=clientHandler,args=(i,)).start()
    time.sleep(1)
    print str(threading.active_count()-1)+' threads started'
    
    while action_time is True:
        msg = raw_input('::: ')
        msg = str(msg)
        if msg == 'quit':
            broadcastData(s, '', 'CLOSING::')
            action_time = False
            time.sleep(1)
        elif msg == 'thread':
            print threading.active_count()
        else:
            print msg

main() # calls up out main function
