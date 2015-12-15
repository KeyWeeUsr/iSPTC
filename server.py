#!/usr/bin/env python
from socket import *
from threading import Thread
import threading, time
ver = '1.12.15'
def read_server_settings():
    print 'elo'
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
    return cnt

def check_duplicate(name):
    cnt = 0
    for x in threadip:
        if x[2] == name:
            cnt += 1
    if cnt > 0:
        cnt += 1
        name = name+'('+str(cnt)+')'
        if len(name) > 15:
            name = name[len(name)-15:]
        return name
    else:
        return name

def send_user_list(s,conn,oldusername,username,addr):
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
            broadcastData(s, conn,'SSERVER::'+username+'('+addr+')'+' joined')
    time.sleep(0.5)
    broadcastData(s, conn,'USRLIST::'+sendlist[:-1])

def recieveData(s, conn):# function to recieve data
    try:
        data = conn.recv(2048) # conn.recv(2048) waits for data of 2048 or less bytes and stores it in data
##        print conn, data, "\n" # print the connection and data sent
    except:
        data = 'close::'
    return data; # returns the contents of data

def broadcastData(s, conn, data): # function to send Data
##    conn.sendall(data)  # sends data received to connection
    for x in threadip:
        try:
            if x[2] is not '':
                x[1].sendall(data)
        except:
            print x[1],' NOT AVAILABLE\n'
##    print "Data sent to all clients \n"  # print to inform data was went


def clientHandler(i):
    global s, threadip, threads
    username,username_set = '',False
    conn, addr = s.accept() # awaits for a client to connect and then accepts 
    print addr," is now connected! \n"
    ## 0Thread, 1connecton, 2usrname, 3ip, 3-2port,4mode
    threadip.append([str(i),conn,'',[addr[0],addr[1]],1])
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
            send_user_list(s,conn,'','',addr[0])
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
            send_user_list(s,conn,'','',addr[0])
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
                            username2 = check_duplicate(username2)
                            x[2] = username2
                            send_user_list(s,conn,oldusername,username,addr[0])
                ## Login username received
                else:
                    for x in threadip:
                        b = x[0].find(str(i))
                        if b is not -1:
                            username2 = remove_spaces(username)
                            username2 = check_duplicate(username2)
                            x[2] = (username2)
                            send_user_list(s,conn,'',username,addr[0])
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