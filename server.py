#!/usr/bin/env python
from socket import *
from threading import Thread
import threading, time
ver = '0.95c'
##welcome_comment = '\n Private offline messages enabled for registered users'
welcome_comment = ''
welcome_msg= 'SSERVER::Welcome to inSecure Plain Text Chat server - ver: '+ver+' '+welcome_comment

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
            x = x[c+1:]
            b = x.find('[')+1
            c = x.find(']')
            Offline_msg = x[b:c]
            iplist[level+1][1].append([IP_or_Name,Auth_pass,Offline_msg])

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

def check_duplicate(name,conn):
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
        conn.send("WSERVER::You are a replicant, changing your name...")
        time.sleep(0.2)
        return name
    else:
        return name

def set_threadip(i,addr,username2,pass_is_True):
    global iplist
    level = 1
    for levels in iplist:
        for x in levels[1]:
            if x[0] == addr or x[0].lower() == username2.lower():
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
            if x[0].lower() == usrname.lower():
                if return_passlvl == True:
                    return True,x[1],levels[0],levels[1]
                return True
    if return_passlvl == True:
        return False,False,False,False
    return False

def register_user(username,usr_pass,add_user):
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
        if level == 2 and add_user == True:
            ## Appends new user with default level 2
            levels[1].append([username,usr_pass,1])
        for x in levels[1]:
            ## Adds space after each level
            regwrite.append('['+x[0]+']['+x[1]+']['+str(x[2])+']')
        regwrite.append('')
        level+=1
    # Overwrites and appends to file
    savef('','load/server_users.cfg')
    for x in regwrite:
        fh = open('load/server_users.cfg', 'a')
        fh.write(str(x)+'\n')
        fh.close()

def send_ulist_only():
    ## 0Thread, 1connecton, 2usrname, 3[0]ip, 3[1]port,4lvl,5afk
    ip_sending_enabled = True
    sendlist = ''
    sendlist+= '[[[Users: '+str(len(threadip))+'/'+str(threads)+'][][-1][ ]]]'
    for x in threadip:
        x[2] = rm_illegal_chr(x[2])
        if ip_sending_enabled == True:
            ## Checks if username is set and appends to list
            if len(x[2]) > 1:
                sendlist+= '[[['+str(x[2])+']['+str(x[3][0])+']['+str(x[4])+']['+str(x[5])+']]]'
##        else:
##            sendlist+= '[[['+str(x[2])+']['+str(x[4])+']]]'
    for x in off_users:
        sendlist+= '[[['+str(x)+'][Offline][0][0]]]'
    broadcastData('USRLIST::'+sendlist[:-1])

def send_user_list(s,conn,oldusername,username,addr,level):
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
            ## Checks if username is set and appends to list
            if len(x[2]) > 1:
                sendlist+= '[[['+str(x[2])+']['+str(x[3][0])+']['+str(x[4])+']['+str(x[5])+']]]'
##        else:
##            sendlist+= '[[['+str(x[2])+']['+str(x[4])+']]]'
    for x in off_users:
        sendlist+= '[[['+str(x)+'][Offline][0][0]]]'
    if username is not '':
        if oldusername is not '':
            broadcastData('SSERVER::'+oldusername+' is now '+username)
        else:
            broadcastData('SERVELJ::lvl['+str(level)+'] '+username+'('+addr+')'+' joined')
    time.sleep(0.4)
    broadcastData('USRLIST::'+sendlist[:-1])

def recieveData(conn):# function to recieve data
    conn.settimeout(30)
    try:
        data = conn.recv(2048) # conn.recv(2048) waits for data of 2048 or less bytes and stores it in data
    except Exception as e:
        e = str(e)
        if e == 'timed out':
            return 'TIMEOUT::'
        else:
            data = 'close::'
    return data; # returns the contents of data

def broadcastPrivate(conn,user, data):
    is_online = False
    ## Find user
    for x in threadip:
        if x[2] == user:
            is_online = True
            try:
                x[1].send(data)
            except:
##                print x[1],' NOT AVAILABLE'
                chatlog.append([get_cur_time(),x[1],' NOT AVAILABLE'])
                threadip.remove(x)
                send_ulist_only()
            break
    if is_online == False:
        is_registered = False
        for x in off_users:
            if x.lower() == user.lower():
                is_registered = True
                off_messages.append([user,data])
        if is_registered == False:
            conn.send('WSERVER::User not found')
            time.sleep(0.2)

def broadcastData(data): # function to send Data
    ## Send data to everyone connected
    for x in threadip:
        try:
            if x[2] is not '':
                x[1].sendall(data)
        except:
##            print x[1],' NOT AVAILABLE'
            chatlog.append([get_cur_time(),x[1],' NOT AVAILABLE'])
            threadip.remove(x)
            send_ulist_only()

def remove_offline_usr(username2):
    cnt = 0
    for x in off_users:
        if x.lower() == username2.lower():
            del off_users[cnt]
        cnt+=1

def send_offline_msg(username_set,authed_user,username2,conn):
    if username_set is True and authed_user is True:
        cnt = 0
        for x in off_messages:
            if x[0].lower() == username2.lower():
                cnt+=1
        if cnt > 0:
            time.sleep(0.2)
            conn.send('WSERVER::We have '+str(cnt)+' messages stored for you')
            time.sleep(0.2)
            deletlist = []
            cnt = 0
            for x in off_messages:
                if x[0].lower() == username2.lower():
                    conn.send(x[1])
                    deletlist.append(cnt)
                    time.sleep(0.2)
                cnt+=1
            deletlist.reverse()
            for x in deletlist:
                off_messages.pop(x)

def usrLeaving(conn,username2,addr,threadip,i,username_set,authed_user,off_msg,reason):
    cnt = 0
    for x in threadip:
        if x[0] == str(i):
           del threadip[cnt]
        cnt+=1
    if reason == 'TIMEOUT::':
        broadcastData('SERVELJ::'+username2+'('+addr[0]+')'+' was kicked, reason: TIMEOUT')
    else:
        broadcastData('SERVELJ::'+username2+'('+addr[0]+')'+' left')
    time.sleep(0.2)
    print get_cur_time(),addr[0]," ",username2," is now disconnected!"
    chatlog.append([get_cur_time(),addr," is now disconnected!"])
    ## Enables private offline messaging for registered and authed user
    if off_msg == '1':
        if username_set is True and authed_user is True:
            is_appended = False
            for x in off_users:
                if x == username2:
                    is_appended = True
            if is_appended == False:
                off_users.append(username2)
    send_ulist_only()

def clientHandler(i):
    global threadip, threads, msgprint_enabled, logging_enabled, welcome_msg, iplist, action_time
    username,username2,username_set,authed_user,off_msg = '','', False, True, '0'
    level, timeouts = 1, 0
    conn, addr = s.accept() # awaits for a client to connect and then accepts 
    print get_cur_time(),addr," is now connected!"
    chatlog.append([get_cur_time(),addr[0]," is now connected!"])
    ## 0Thread, 1connecton, 2usrname, 3[0]ip, 3[1]port, 4lvl,5afk
    threadip.append([str(i),conn,'',[addr[0],addr[1]],1,'1'])
    conn.sendall(welcome_msg)
    while 1:
        data = recieveData(conn)
        if data == 'kpALIVE::':
            timeouts = 0
        else:
            chatmlog.append([get_cur_time(),username,data])
        ##Normal messages
        if data[0:9] == 'MESSAGE::' and username_set is True:
            timeouts = 0
            b = data[9:].find('MESSAGE::')
            if b is not -1:
                conn.send('WSERVER::Removed')
            else:
                if msgprint_enabled == 1:
                    print get_cur_time(),username2,data[9:]
                if data[9:11] == 's/' and level > 7:
                    if data == 'MESSAGE::s/log':
                        conn.send('WSERVER::Sending '+str(len(chatlog))+' lines')
                        time.sleep(0.1)
                        for x in chatlog:
                            conn.send('WSERVER::'+str(x))
                            time.sleep(0.1)
                    elif data == 'MESSAGE::s/mlog':
                        conn.send('WSERVER::Sending '+str(len(chatmlog))+' lines')
                        time.sleep(0.1)
                        for x in chatmlog:
                            conn.send('WSERVER::'+str(x))
                            time.sleep(0.1)
                    elif data == 'MESSAGE::s/threadip':
                        for x in threadip:
                            conn.send('WSERVER::'+str(x))
                            time.sleep(0.1)
                elif data[9:11] == '@@' and data[11] is not " ":
                    b = data[:].find(']')
                    if b is -1:
                        conn.send('WSERVER::] has to be at the end of username')
                    else:
                        usr_to_send = data[11:b]
                        broadcastPrivate(conn,usr_to_send, 'm:'+sendlevel+username+'@@'+usr_to_send+data[b:])
                else:
                    broadcastData('m:'+sendlevel+username+data[9:])
        ## Leaving
        elif not data:
            usrLeaving(conn,username2,addr,threadip,i,username_set,authed_user,off_msg,'no')
            conn.close()
            Thread(target=clientHandler,args=(i,)).start()
            break
        ## Leaving2
        elif data == 'close::' or data == 'TIMEOUT::':
            if data == 'close::':
                usrLeaving(conn,username2,addr,threadip,i,username_set,authed_user,off_msg,'no')
            else:
                usrLeaving(conn,username2,addr,threadip,i,username_set,authed_user,off_msg,'TIMEOUT::')
            conn.close()
            Thread(target=clientHandler,args=(i,)).start()
            break
        ## Registration
        elif data[0:9] == 'aUSRREG::':
            registered = check_if_registered(username2,addr[0],False)
            if registered == True:
                conn.send('WSERVER::Already registered')
                time.sleep(0.1)
            else:
                usr_pass = data[9:]
                if len(usr_pass) > 10:
                    usr_pass = usr_pass[:10]
                    conn.send('SSERVER::Max length is 10, changed to: '+usr_pass)
                    time.sleep(0.3)
                illeg_chk = check_for_illegal_chr([' ','[',']'],usr_pass)
                if illeg_chk == True:
                    conn.send('WSERVER::Spaces, "[", "]" are not allowed')
                else:
                    conn.send('WSERVER::Registering '+username2+' with '+usr_pass)
                    register_user(username2,usr_pass,True)
        ## User auth with passwd
        elif data[0:9] == 'USRLOGI::':
            usr_pass = data[9:]
            if len(usr_pass) > 15:
                usr_pass = usr_pass[:15]
            registered = check_if_registered(username2,addr,True)
            if registered[0] == True and usr_pass == registered[1]:
                level = set_threadip(str(i),addr[0],username2,True)
                ## Sendlevel string is used by clients to color the username in messages
                if len(str(level)) == 1:
                        sendlevel = '0'+str(level)
                else:
                    sendlevel = str(level)
                broadcastData('SSERVER::'+remove_spaces(username)+' is level'+str(level))
                for x in threadip:
                    if x[0] == str(i):
                        x[2] = username2
                        x[4] = level
                        break
                username_set, authed_user = True, True
                remove_offline_usr(username2)
                send_ulist_only()
                time.sleep(0.2)
                conn.send('WSERVER::Accepted')
                time.sleep(0.2)
                send_offline_msg(username_set,authed_user,username2,conn)
                conn.send('DUPLICT::'+username2)
                time.sleep(0.2)
            else:
                time.sleep(0.1)
                conn.send('WSERVER::Wrong pass')
        ## Configure offline msg
        elif data[0:9] == 'CONFIGR::':
            if username_set is True and authed_user is True:
                b = data.find('offmsg=')
                if b is not -1:
                    off_msg = data[b+len('offmsg='):]
                    for levels in iplist:
                        for x in levels[1]:
                            if x[0] == username2:
                                x[2] = off_msg
                    register_user('a','a',False)
                    time.sleep(0.1)
                    conn.send('WSERVER::off_msg set to: '+off_msg)
                    time.sleep(0.1)
            else:
                time.sleep(0.1)
                conn.send('WSERVER::You have no power here')
                time.sleep(0.1)
        ## AFK
        elif data[0:9] == 'aAFKAFK::':
            for x in threadip:
                if x[0] == str(i):
                    if x[5] == '1':
                        broadcastData('SSERVER::'+username2+' is afk')
                        newval = '0'
                    else:
                        broadcastData('SSERVER::'+username2+' is no longer afk')
                        newval = '1'
                    x[5] = newval
            time.sleep(0.2)
            send_ulist_only()
        ## Username
        elif data[0:9] == 'USRINFO::':
            data = data.rstrip()
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
                ## Removes it from data string
                data = data[:b]
            else:
                usr_pass = False
                ## Checks length
            if len(data) > 11:
                username = data[9:]
                if len(username) > 15:
                    username = username[:15]
                ## Username gets changed
                if username_set is True:
                    for x in threadip:
                        if x[0] == str(i):
                            username2 = remove_spaces(username)
                            username2 = rm_illegal_chr(username2)
                            x[2] = ''
                            username2 = check_duplicate(username2,conn)
                            username = add_spaces(username2)
                            registered = check_if_registered(username2,addr,True)
                            if registered[0] == True and usr_pass == registered[1]:
                                level = set_threadip(str(i),addr[0],username2,True)
                                x[2] = username2
                                username_set, authed_user = True, True
                            elif registered[0] == True and usr_pass != registered[1]:
                                conn.send('WSERVER::Name is registered, waiting for auth')
                                level = 0
                                x[4] = level
                                username_set, authed_user = False, False
                            else:
                                x[2] = (username2)
                                level = 1
                                x[4] = level
                                username_set, authed_user = True, False
                            ## Sendlevel string is used by clients to color the username in messages
                            if len(str(level)) == 1:
                                sendlevel = '0'+str(level)
                            else:
                                sendlevel = str(level)
                            if username_set is True:
                                chatlog.append([get_cur_time(),addr[0],' is level ',level,' !'])
                                
                                if authed_user is True:
                                    remove_offline_usr(username2)
                                send_user_list(s,conn,'',username2,addr[0],level)
                                time.sleep(0.1)
                                conn.send('DUPLICT::'+username2)
                                time.sleep(0.2)
                ## Login username received
                else:
                    for x in threadip:
                        if x[0] == str(i):
                            username2 = remove_spaces(username)
                            username2 = rm_illegal_chr(username2)
                            x[2] = ''
                            username2 = check_duplicate(username2,conn)
                            username = add_spaces(username2)
                            registered = check_if_registered(username2,addr,True)
                            if registered[0] == True and usr_pass == registered[1]:
                                level = set_threadip(str(i),addr[0],username2,True)
                                x[2] = username2
                                username_set, authed_user = True, True
                            elif registered[0] == True and usr_pass != registered[1]:
                                conn.send('WSERVER::Name is registered, waiting for auth')
                                level = 0
                                x[4] = level
                                username_set, authed_user = False, False
                            else:
                                x[2] = (username2)
                                level = 1
                                x[4] = level
                                username_set, authed_user = True, False
                            ## Sendlevel string is used by clients to color the username in messages
                            if len(str(level)) == 1:
                                sendlevel = '0'+str(level)
                            else:
                                sendlevel = str(level)
                            if username_set is True:
                                chatlog.append([get_cur_time(),addr[0],' is level ',level,' !'])
                                if authed_user is True:
                                    remove_offline_usr(username2)
                                send_user_list(s,conn,'',username2,addr[0],level)
                                time.sleep(0.1)
                                conn.send('DUPLICT::'+username2)
                send_offline_msg(username_set,authed_user,username2,conn)
    
        else:
            if data == 'kpALIVE::':
                pass
            else:
                time.sleep(0.1)
                conn.send("WSERVER::We don't accept this")
    

def reset_offmsg_list():
    global off_users
    off_users = []
    for levels in iplist:
        for x in levels[1]:
            if x[2] == '1':
                off_users.append(x[0])

threads = int(read_settings('threadcnt='))
action_time = True
iplist,chatlog,chatmlog,threadip,off_users,off_messages = [],[],[],[],[],[]
read_server_usr_settings()
log_enabled = int(read_settings('logging='))
msgprint_enabled = 0
msgprint_enabled = int(read_settings('msgprint='))
reset_offmsg_list()
def main(): # main function
    global s, action_time, msgprint_enabled, log_enabled, iplist
    s = socket(AF_INET, SOCK_STREAM) # creates our socket; TCP socket
    try:
        s.bind(('', 44671)) # tells the socket to bind to localhost on port 44671
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
        if msg == 'q':
            broadcastData('CLOSING::')
            action_time = False
            s.close()
            s = ''
            time.sleep(1)
        elif msg == 'thread':
            print threading.active_count()
        elif msg == 'lvluser':
            print 'disabled'
##            lvluser = raw_input('Username:')
##            lvluserlvl = raw_input('level')
##            broadcastData('SSERVER::'+str(lvluser)+' is now level '+str(lvluserlvl)+' !')
            
        elif msg == 'threadip':
            for x in threadip:
                print x
        elif msg == 'iplist':
            for x in iplist:
                print x
        elif msg == 'iplist-reload':
            iplist = []
            read_server_usr_settings()
            reset_offmsg_list()
        elif msg == 'help':
            print """ Type: quit, lvluser, threadip, iplist, iplist-reload, log, mlog, log-toggle,
            log-save, say, msgprint, msgprint-toggle, welcm """
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
        elif msg == 'mlog':
            for x in chatmlog:
                print x
        elif msg == 'offusers':
            for x in off_users:
                print x    
        elif msg == 'log-save':
            chat_len = len(chatmlog)
            print 'Writing ',str(chat_len),' lines'
            for cnt in range(0,chat_len):
                fh = open('load/chatlog.txt', 'a')
                x = chatmlog[cnt]
                if len(x) < 1:
                    x = ' '
                fh.write(str(x)+'\n')
                fh.close()
            for cnt in range(0,chat_len):
                chatmlog.pop(0)
            print 'Done'
        elif msg == 'msgprint':
            global msgprint_enabled
            print 'msgprint is: ',msgprint_enabled
        elif msg == 'msgprint-toggle':
            if msgprint_enabled is 1:
                msgprint_enabled = 0
            else:
               msgprint_enabled = 1
            write_settings('msgprint',msgprint_enabled)
        elif msg == 'say':
            x = raw_input(':::Say what? ')
            print 'Sending "'+x+'" to all'
            broadcastData('SSERVER::'+x)
        elif msg == 'welcm':
            x = raw_input(':::message ')
            global welcome_msg
            welcome_msg = 'SSERVER::'+x
            broadcastData('SSERVER::Welcome message is now: '+x)
        else:
            print msg

main()
