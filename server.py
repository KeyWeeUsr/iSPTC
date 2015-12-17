#!/usr/bin/env python
from socket import *
from threading import Thread
import threading, time
ver = '0.81'
def read_server_settings():
    text = readf('load/server')
    for x in text:
        iplist.append(x)

def readf(filename):
    file = filename
    f = open(file, 'rU')
    a = f.read()
    a = str.splitlines(a)
    f.close()
    return a

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

def set_threadip(i,addr,which):
    level = 1
    addr = str(addr)
    for x in iplist:
        if str(x) == addr:
            level = 2
            for x2 in threadip:
                if x2[0] == i:
                    x2[which] = 2
                    return level
    return level

def send_user_list(s,conn,oldusername,username,addr):
    ip_sending_enabled = False
    if oldusername is not '':
        oldusername = remove_spaces(oldusername)
    if username is not '':
        username = remove_spaces(username)
    sendlist = ''
    for x in threadip:
        if ip_sending_enabled == True:
            sendlist+= '[[['+str(x[3][0])+']['+str(x[2])+']['+str(x[4])+']]]'
        else:
            sendlist+= '[[['+str(x[2])+']['+str(x[4])+']]]'
    if username is not '':
        if oldusername is not '':
            broadcastData(s, conn,'SSERVER::'+oldusername+' is now '+username)
        else:
            broadcastData(s, conn,'SERVELJ::'+username+'('+addr+')'+' joined')
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
    level = 1
    conn, addr = s.accept() # awaits for a client to connect and then accepts 
    print addr," is now connected! \n"
    ## 0Thread, 1connecton, 2usrname, 3ip, 3-2port,4mode
    threadip.append([str(i),conn,'',[addr[0],addr[1]],1])
    conn.sendall('SSERVER::Welcome to inSecure Plain Text Chat - ver: '+ver+'\nhyperlink test is http://mans.bot.nu')
    while 1:
        data = recieveData(s, conn)
        ##Normal messages
        if data[0:9] == 'MESSAGE::':
            broadcastData(s, conn, 'm::'+str(level)+username+data[9:])
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
            broadcastData(s, conn, 'SERVELJ::'+username2+' left')
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
            broadcastData(s, conn, 'SERVELJ::'+username2+' left')
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
                            level = set_threadip(str(i),addr[0],4)
                            print addr[0],' is level ',level,' !'
                            broadcastData(s, 'nav','SSERVER::'+remove_spaces(username)+' is level'+str(level))
                            time.sleep(0.5)
                            send_user_list(s,conn,oldusername,username,addr[0])
                ## Login username received
                else:
                    for x in threadip:
                        b = x[0].find(str(i))
                        if b is not -1:
                            username2 = remove_spaces(username)
                            username2 = check_duplicate(username2)
                            x[2] = (username2)
                            level = set_threadip(str(i),addr[0],4)
                            print addr[0],' is level ',level,' !'
                            broadcastData(s, 'nav','SSERVER::'+username2+' is level'+str(level))
                            time.sleep(0.5)
                            send_user_list(s,conn,'',username,addr[0])
                username_set = True
        
threads = 10
action_time = True
iplist = []
threadip = []
read_server_settings()
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
        elif msg == 'lvluser':
            lvluser = raw_input('Username:')
            lvluserlvl = raw_input('level')
            broadcastData(s, 'nav','SSERVER::'+str(lvluser)+' is now level '+str(lvluserlvl)+' !')
        elif msg == 'threadip':
            print threadip
        elif msg == 'iplist':
            print iplist
        elif msg == 'help':
            print 'Type: quit, lvluser, threadip, iplist'
        else:
            print msg

main() # calls up out main function
