#!/usr/bin/env python
from socket import *
from threading import Thread
import threading, time
ver = '0.91'
welcome_msg= 'SSERVER::Welcome to inSecure Plain Text Chat - ver: '+ver+'\nRegistration is now supported'

def read_server_usr_settings():
    text = readf('load/server_users.cfg')
    level = 9
    for x in range(-1,level+1):
        iplist.append([x])
    for x in range(-1,level+1):
        iplist[x].append([])
    for x in text:
        dont_append = False
        if len(x) < 1:
            dont_append = True
        elif x[:3] == '[[l':
            level = int(x[3:5])
            dont_append = True
        elif x[:2] == '##':
            dont_append = True
        if dont_append == False:
            b = x.find('[')+1
            c = x.find(']')
            IP_or_Name = x[b:c]
            x = x[c+1:]
            b = x.find('[')+1
            c = x.find(']')
            Auth_pass = x[b:c]
            iplist[level+1][1].append([IP_or_Name,Auth_pass])

def get_cur_time():
    return time.strftime("%H:%M")

def readf(filename):
    file = filename
    f = open(file, 'rU')
    a = f.read()
    a = str.splitlines(a)
    f.close()
    return a

def savef(text,file):
    f = open(file, 'w')
    f.write(text)
    f.close()

def get_settings(text,text_find):
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = lines[len(text_find):]
    return c

def edit_settings(text,text_find,new_value):
    count = 0
    newlist = []
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = text_find + '=' + str(new_value)
            newlist.append(c)
        else:
            newlist.append(lines)
        count+=1
    count = 1
    return newlist

def write_settings(text_find,new_value):
        a = readf('load/server.cfg')
        a = edit_settings(a,text_find,new_value)
        text = a = '\n'.join(str(e) for e in a)
        savef(text,'load/server.cfg')

def read_settings(text_find):
    a = readf('load/server.cfg')
    a = get_settings(a,text_find)
    return a

def add_spaces(username):
    while len(username) < 19:
        username = ' '+username
    return username

def remove_spaces(username):
    for x in username:
        if x == ' ':
            username = username[1:]
        else:
            break
    return username

def check_duplicate(name):
    cnt = 0
    again = False
    for x in threadip:
        if x[2] == name:
            cnt += 2
    if cnt > 0:
        name_without_cnt = name
        while True:
            again = False
            name = name_without_cnt+'('+str(cnt)+')'
            for x in threadip:
                if x[2] == name:
                    again = True
            if again == False:
                break
            cnt += 1
        return name
    else:
        return name

def set_threadip(i,addr,username2,pass_is_True):
    global iplist
    level = 1
    for levels in iplist:
        for x in levels[1]:
            if x[0] == addr or x[0] == username2:
                if x[1] == 'False':
                    level = levels[0]
                elif pass_is_True == True:
                    level = levels[0]
                else:
                    pass
    for x in threadip:
        if x[0] == i:
            x[4] = level
            break
    return level

def rm_illegal_chr(name):
    brktemp_list = []
    for x in name:
        brktemp_list.append(x)
    cnt = 0
    for x in brktemp_list:
        if x == '[':
            brktemp_list[cnt] = '{'
        elif x == ']':
            brktemp_list[cnt] = '}'
        cnt+=1
    name = ''
    for x in brktemp_list:
        name = name+x
    return name

def check_for_illegal_chr(illegal,name):
    found = False
    for x in illegal:
        b = name.find(x)
        if b is not -1:
            found = True
            break
    return found

def check_if_registered(usrname,addr,return_passlvl):
    global iplist
    for levels in iplist:
        for x in levels[1]:
##            if x[0] == usrname or x[0] == addr:
            if x[0] == usrname:
                if return_passlvl == True:
                    return True,x[1],levels[0]
                return True
    if return_passlvl == True:
        return False,False,False
    return False

def register_user(username,usr_pass):
    global iplist
    level = -1
    regwrite = []
    regwrite.append('## 0 is muted\n## -1 is banned')
    for levels in iplist:
        ## Appends level
        if level == -1:
            regwrite.append('[[l'+str(level)+'-none]]')
        else:
            regwrite.append('[[l0'+str(level)+'-none]]')
        if level == 2:
            ## Appends new user with default level 2
            levels[1].append([username,usr_pass])
        for x in levels[1]:
            ## Adds space after each level
            regwrite.append('['+x[0]+']['+x[1]+']')
        regwrite.append('')
        level+=1
    # Writes file
    savef('','load/server_users.cfg')
    for x in regwrite:
        fh = open('load/server_users.cfg', 'a')
        fh.write(str(x)+'\n')
        fh.close()

def send_ulist_only(s):
    ip_sending_enabled = True
    sendlist = ''
    sendlist+= '[[[Users: '+str(len(threadip))+'/'+str(threads)+'][][-1][ ]]]'
    for x in threadip:
        x[2] = rm_illegal_chr(x[2])
        if ip_sending_enabled == True:
            sendlist+= '[[['+str(x[2])+']['+str(x[3][0])+']['+str(x[4])+']['+str(x[5])+']]]'
        else:
            sendlist+= '[[['+str(x[2])+']['+str(x[4])+']]]'
    broadcastData(s, 'nav','USRLIST::'+sendlist[:-1])

def send_user_list(s,conn,oldusername,username,addr):
    global threads
    ip_sending_enabled = True
    if oldusername is not '':
        oldusername = remove_spaces(oldusername)
    if username is not '':
        username = remove_spaces(username)
    sendlist = ''
    sendlist+= '[[[Users: '+str(len(threadip))+'/'+str(threads)+'][][-1][ ]]]'
    for x in threadip:
        x[2] = rm_illegal_chr(x[2])
        if ip_sending_enabled == True:
            sendlist+= '[[['+str(x[2])+']['+str(x[3][0])+']['+str(x[4])+']['+str(x[5])+']]]'
        else:
            sendlist+= '[[['+str(x[2])+']['+str(x[4])+']]]'
    if username is not '':
        if oldusername is not '':
            broadcastData(s, conn,'SSERVER::'+oldusername+' is now '+username)
        else:
            broadcastData(s, conn,'SERVELJ::'+username+'('+addr+')'+' joined')
    time.sleep(0.4)
    broadcastData(s, conn,'USRLIST::'+sendlist[:-1])

def recieveData(s, conn):# function to recieve data
    try:
        data = conn.recv(2048) # conn.recv(2048) waits for data of 2048 or less bytes and stores it in data
    except:
        data = 'close::'
    return data; # returns the contents of data

def broadcastPrivate(user, data):
    ## Find user
    for x in threadip:
        if x[2] == user:
            try:
                x[1].send(data)
            except:
                print x[1],' NOT AVAILABLE\n'
            break

def broadcastData(s, conn, data): # function to send Data
    ## Send data to everyone connected
    for x in threadip:
        try:
            if x[2] is not '':
                x[1].sendall(data)
        except:
            print x[1],' NOT AVAILABLE\n'

def usrLeaving(s,conn,username2,addr,threadip,i):
    cnt = 0
    for x in threadip:
        b = x[0].find(str(i))
        if b is not -1:
           del threadip[cnt]
        cnt+=1
    send_user_list(s,conn,'','',addr[0])
    time.sleep(0.5)
    broadcastData(s, conn, 'SERVELJ::'+username2+'('+addr[0]+')'+' left')
    print addr," is now disconnected! \n"
    
def clientHandler(i):
    global s, threadip, threads, msgprint_enabled, logging_enabled, welcome_msg, iplist
    username,username_set = '',False
    level = 1
    conn, addr = s.accept() # awaits for a client to connect and then accepts 
    print get_cur_time(),addr," is now connected! \n"
    ## 0Thread, 1connecton, 2usrname, 3ip, 3-2port,4mode,5afk
    threadip.append([str(i),conn,'',[addr[0],addr[1]],1,'1'])
    conn.sendall(welcome_msg)
    while 1:
        data = recieveData(s, conn)
        chatlog.append([get_cur_time(),username,data])
        ##Normal messages
        if data[0:9] == 'MESSAGE::':
            while True:
                b = data[9:].find('MESSAGE::')
                if b is not -1:
                    data = data[:b]+data[b+9:]
                else:
                    break
            if msgprint_enabled == 1:
                print get_cur_time(),username2,data[9:]
            if data[9:11] == '@@' and data[11] is not " ":
                b = data[11:].find(' ')
                if b is -1:
                    usr_to_send = data[11:]
                else:
                    usr_to_send = data[11:b+11]
                broadcastPrivate(usr_to_send, 'm:'+sendlevel+username+data[9:])
            else:
                broadcastData(s, conn, 'm:'+sendlevel+username+data[9:])
        ## Leaving
        if not data:
            usrLeaving(s,conn,username2,addr,threadip,i)
            Thread(target=clientHandler,args=(i,)).start()
            break
        ## Leaving2
        elif data == 'close::':
            usrLeaving(s,conn,username2,addr,threadip,i)
            Thread(target=clientHandler,args=(i,)).start()
            break
        ## Registration
        elif data[0:9] == 'aUSRREG::':
            registered = check_if_registered(username2,addr[0],False)
            if registered == True:
                conn.send('SSERVER::Already registered')
                time.sleep(0.1)
            else:
                usr_pass = data[9:]
                if len(usr_pass) > 10:
                    usr_pass = usr_pass[:10]
                    conn.send('SSERVER::Max length is 10, changed to: '+usr_pass)
                    time.sleep(0.3)
                illeg_chk = check_for_illegal_chr([' ','[',']'],usr_pass)
                if illeg_chk == True:
                    conn.send('SSERVER::Spaces, "[", "]" are not allowed')
                else:
                    conn.send('SSERVER::Registering '+username2+' with '+usr_pass)
                    register_user(username2,usr_pass)
        ## User auth with passwd
        elif data[0:9] == 'USRLOGI::':
            usr_pass = data[9:]
            if len(usr_pass) > 15:
                usr_pass = usr_pass[:15]
            registered = check_if_registered(username2,addr,True)
            if registered[0] == True and usr_pass == registered[1]:
                level = registered[2]
                broadcastData(s, 'nav','SSERVER::'+remove_spaces(username)+' is level'+str(level))
                for x in threadip:
                    b = x[0].find(str(i))
                    if b is not -1:
                        x[2] = username2
                        x[4] = level
                        break
                send_ulist_only(s)
            else:
                conn.send('SSERVER::Wrong pass')
        ## AFK
        elif data[0:9] == 'aAFKAFK::':
            for x in threadip:
                b = x[0].find(str(i))
                if b is not -1:
                    if x[5] == '1':
                        broadcastData(s, 'nav','SSERVER::'+username2+' is afk')
                        newval = '0'
                    else:
                        broadcastData(s, 'nav','SSERVER::'+username2+' is no longer afk')
                        newval = '1'
                    x[5] = newval
            time.sleep(0.2)
            send_ulist_only(s)
        ## Username
        elif data[0:9] == 'USRINFO::':
            oldusername = str(username)
            for x in oldusername:
                if x == ' ':
                    oldusername = oldusername[1:]
                else:
                    pass
            ## Gets userpass
            b = data.find(']')
            if b is not -1 and len(data[b:]) > 2:
                usr_pass = data[b+1:]
                data = data[:b]
            else:
                usr_pass = False
            if len(data) > 11:
                username = data[9:]
                if len(username) > 15:
                    username = username[:15]
                ## Username gets changed
                if username_set is True:
                    for x in threadip:
                        b = x[0].find(str(i))
                        if b is not -1:
                            username2 = remove_spaces(username)
                            username2 = rm_illegal_chr(username2)
                            x[2] = ''
                            username2 = check_duplicate(username2)
                            username = add_spaces(username2)
                            registered = check_if_registered(username2,addr,True)
                            if registered[0] == True and usr_pass == registered[1]:
                                level = set_threadip(str(i),addr[0],username2,True)
                                x[2] = username2
                            elif registered[0] == True and usr_pass != registered[1]:
                                x[2] = oldusername
                                username2 = oldusername
                                conn.send('SSERVER::Name is registered, reverting')
                            else:
                                x[2] = (username2)
                            if len(str(level)) == 1:
                                sendlevel = '0'+str(level)
                            else:
                                sendlevel = str(level)
                            print addr[0],' is level ',level,' !'
                            broadcastData(s, 'nav','SSERVER::'+username2+' is level '+str(level))
                            time.sleep(0.4)
                            send_user_list(s,conn,'',username2,addr[0])
                ## Login username received
                else:
                    for x in threadip:
                        b = x[0].find(str(i))
                        if b is not -1:
                            username2 = remove_spaces(username)
                            username2 = rm_illegal_chr(username2)
                            x[2] = ''
                            username2 = check_duplicate(username2)
                            username = add_spaces(username2)
                            registered = check_if_registered(username2,addr,True)
                            if registered[0] == True and usr_pass == registered[1]:
                                level = set_threadip(str(i),addr[0],username2,True)
                                x[2] = username2
                            elif registered[0] == True and usr_pass != registered[1]:
                                conn.send('SSERVER::Name is registered, waiting for auth')
                            else:
                                x[2] = (username2)
                            if len(str(level)) == 1:
                                sendlevel = '0'+str(level)
                            else:
                                sendlevel = str(level)
                            print addr[0],' is level ',level,' !'
                            broadcastData(s, 'nav','SSERVER::'+username2+' is level '+str(level))
                            time.sleep(0.4)
                            send_user_list(s,conn,'',username2,addr[0])
                username_set = True


threads = int(read_settings('threadcnt='))
action_time = True
iplist,chatlog,threadip = [],[],[]
read_server_usr_settings()
log_enabled = int(read_settings('logging='))
msgprint_enabled = 0
msgprint_enabled = int(read_settings('msgprint='))
def main(): # main function
    global s, action_time, msgprint_enabled, log_enabled
    s = socket(AF_INET, SOCK_STREAM) # creates our socket; TCP socket
    try:
        s.bind(('', 44671)) # tells the socket to bind to localhost on port 8000
    except:
        print "Can't bind address"
        time.sleep(2)
        quit()
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
            print 'disabled'
##            lvluser = raw_input('Username:')
##            lvluserlvl = raw_input('level')
##            broadcastData(s, 'nav','SSERVER::'+str(lvluser)+' is now level '+str(lvluserlvl)+' !')
            
        elif msg == 'threadip':
            for x in threadip:
                print x
        elif msg == 'iplist':
            for x in iplist:
                print x
        elif msg == 'help':
            print 'Type: quit, lvluser, threadip, iplist, log, log-toggle, log-save, say, msgprint, msgprint-toggle'
        elif msg == 'log-toggle':
            if log_enabled == 1:
                log_enabled = 0
                print 'Logging disabled'
            if log_enabled == 0:
                log_enabled = 1
                print 'Logging enabled'
            write_settings('logging',log_enabled)
        elif msg == 'log':
            for x in chatlog:
                print x
        elif msg == 'log-save':
            chat_len = len(chatlog)
            for cnt in range(0,chat_len):
                print cnt
                fh = open('load/chatlog.txt', 'a')
                x = chatlog[cnt]
                if len(x) < 1:
                    x = ' '
                print 'Writing ',str(x)
                fh.write(str(x)+'\n')
                fh.close()
            print chatlog
            for cnt in range(0,chat_len):
                chatlog.pop(0)
        elif msg == 'msgprint':
            global msgprint_enabled
            print 'msgprint is: ',msgprint_enabled
        elif msg == 'msgprint-toggle':
            if msgprint_enabled is 1:
                msgprint_enabled = 0
            else:
               msgprint_enabled = 1
            write_settings('msgprint',msgprint_enabled)
        elif msg == 'chatlog':
            print chatlog
        elif msg == 'say':
            x = raw_input(':::Say what? ')
            print 'Sending "'+x+'" to all'
            broadcastData(s, 'nav','SSERVER::'+x)
        else:
            print msg

main() # calls up out main function
