#!/usr/bin/env python
from socket import *
from threading import Thread
import threading, time
from time import sleep
ver = '1.05'
##welcome_comment = '\n Private offline messages enabled for registered users'
welcome_comment = ''
welcome_msg= 'SSERVER::Welcome to inSecure Plain Text Chat server - ver: '+ver+' '+welcome_comment

def read_server_usr_settings():
    text = readf('load/server_users.ini')
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
    try:
        f = open(file, 'rU')
    except:
        savef('',filename)
        f = open(file, 'rU')
    a = f.read()
    a = str.splitlines(a)
    f.close()
    return a

def savef(text,file):
    f = open(file, 'w')
    f.write(text)
    f.close()

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

def read_settings(*arg):
    global sys_path
    a = readf('load/server.ini')
    a = get_settings(a,arg[0],arg[1])
    return a

def get_settings(text,text_find,default_value):
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = lines[len(text_find):]
    ## Checks if it exists and appends something, if not
    try:
        if c == '':
            c = default_value
            if default_value != '':
                write_settings(text_find[:-1],'\n'+c)
    except:
        c = default_value
        fh = open('load/server.ini', 'a')
        fh.write('\n'+str(text_find)+str(c))
        fh.close()
    return c

def write_settings(text_find,new_value):
    global sys_path
    a = readf('load/server.ini')
    a = edit_settings(a,text_find,new_value)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,'load/server.ini')    

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
        event_list.append(['Send-Thread',conn,"WSERVER::You are a replicant, changing your name..."])
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
    ## Returns 0Reg True/False, passwd, level, [username, passwd, offline_msg 1/0]
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

def save_user_settings():
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
        for x in levels[1]:
            ## Adds space after each level
            regwrite.append('['+x[0]+']['+x[1]+']['+str(x[2])+']')
        regwrite.append('')
        level+=1
    # Overwrites and appends to file
    savef('','load/server_users.ini')
    for x in regwrite:
        fh = open('load/server_users.ini', 'a')
        fh.write(str(x)+'\n')
    fh.close()

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
    savef('','load/server_users.ini')
    for x in regwrite:
        fh = open('load/server_users.ini', 'a')
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
                sendlist+= '[[['+str(x[2])+']['+str(x[3][0])+']['+str(x[4])+']['+str(x[5])+']['+str(x[6])+']]]'
##        else:
##            sendlist+= '[[['+str(x[2])+']['+str(x[4])+']]]'
    for x in off_users:
        sendlist+= '[[['+str(x)+'][Offline][0][0]]]'
    event_list.append(['SEND','USRLIST::'+sendlist[:-1]])

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
                sendlist+= '[[['+str(x[2])+']['+str(x[3][0])+']['+str(x[4])+']['+str(x[5])+']['+str(x[6])+']]]'
##        else:
##            sendlist+= '[[['+str(x[2])+']['+str(x[4])+']]]'
    for x in off_users:
        sendlist+= '[[['+str(x)+'][Offline][0][0]]]'
    if username is not '':
        if oldusername is not '':
            event_list.append(['SEND','SSERVER::'+oldusername+' is now '+username])
        else:
            event_list.append(['SEND','SERVELJ::'+username+'('+addr+')'+' joined'])
    event_list.append(['SEND','USRLIST::'+sendlist[:-1]])

def recieveData_file(conn,bitr):# function to recieve data
    conn.settimeout(30)
    try:
        data = conn.recv(bitr) # waits for data and stores it in data
    except Exception as e:
        e = str(e)
        if e == 'timed out':
            return 'TIMEOUT::'
        else:
            data = 'close::'
    return data; # returns the contents of data


def recieveData(conn,bitr):# function to recieve data
    conn.settimeout(30)
    data_list = []
    buff = ''
    try:
        data = buff+conn.recv(bitr) # waits for data and stores it in data
        buff = ''
        cnt = 0
        while True:
            b = data.find('<e%$>')
            if b is not -1:
                data_list.append(data[:b])
                data = data[b+len('<e%$>'):]
            else:
                if cnt == 0:
                    if len(data) > 1:
                        data_list = [data]
                elif len(data) > 0:
                    buff += data
                break
            cnt += 1
            if cnt == 100:
                break
    except Exception as e:
        e = str(e)
        if e == 'timed out':
            return ['TIMEOUT::']
        else:
            data_list = ['close::']
    return data_list; # returns the contents of data

def broadcastPrivate(conn,user, data):
    is_online = False
    ## Find user
    for x in threadip:
        if x[2] == user:
            is_online = True
            try:
                x[1].send(data+'<e%$>')
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
        if is_registered == False and conn != '':
            try:
                event_list.append(['Send-Thread',conn,'WSERVER::User not found'])
            except:
                pass

def broadcastData(data): # function to send Data
    ## Send data to everyone connected
    for x in threadip:
        try:
            if x[2] is not '':
                x[1].send(data+'<e%$>')
        except:
            print x[1],' NOT AVAILABLE'
            chatlog.append([get_cur_time(),x[1],' NOT AVAILABLE'])
            threadip.remove(x)
            send_ulist_only()

def list_sender_thread(conn,lisst,typ):
    global shared_filelist
    if typ == 'filelist-message':
        event_list.append(['Send-Thread',conn,'WSERVER::File count - '+str(len(shared_filelist))])
        tflsize = 0
        for x in shared_filelist:
            tflsize += len(x[1])
            flsizemb = float(len(x[1]))/float(1052291)
            flsizemb =  round(flsizemb,2)
            event_list.append(['Send-Thread',conn,'WSERVER::'+x[0]+'  MB['+str(flsizemb)+'] '+' B['+str(len(x[1]))+']'])
            sleep(0.02)
        event_list.append(['Send-Thread',conn,'WSERVER::Total size '+str(tflsize)])
    elif typ == 'filelist-list':
        sendlist = ''
        cnt = 0
        for x in shared_filelist:
            flsizemb = float(len(x[1]))/float(1052291)
            flsizemb = round(flsizemb,2)
            sendlist+= '[[['+str(x[0])+']['+str(flsizemb)+' MB'+']['+x[2]+']['+str(x[3])+']['+str(x[4])+']]]'
            cnt += 1
        if cnt == 0:
            event_list.append(['Send-Thread',conn,'FILLIST::EMPTY-LIST'])
        else:
            event_list.append(['Send-Thread',conn,'FILLIST::'+sendlist])
    else:
        for x in lisst:
            tstring = ''
            for words in x:
                tstring += str(words)+' '
            event_list.append(['Send-Thread',conn,'WSERVER::'+tstring])
            sleep(0.005)

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
            event_list.append(['Send-Thread',conn,'WSERVER::We have '+str(cnt)+' messages stored for you'])
            deletlist = []
            cnt = 0
            for x in off_messages:
                if x[0].lower() == username2.lower():
                    event_list.append(['Send-Thread',conn,x[1]])
                    deletlist.append(cnt)
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
        event_list.append(['SEND','SERVELJ::'+username2+'('+addr[0]+')'+' was kicked, reason: TIMEOUT'])
##        broadcastData('SERVELJ::'+username2+'('+addr[0]+')'+' was kicked, reason: TIMEOUT')
    else:
        event_list.append(['SEND','SERVELJ::'+username2+'('+addr[0]+')'+' left'])
##        broadcastData('SERVELJ::'+username2+'('+addr[0]+')'+' left')
    print get_cur_time(),addr[0]," ",username2," disconnected!"
    chatlog.append([get_cur_time(),addr," disconnected!"])
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

def eventThread():
    global threadip
    user_count = 0
    sleep_more = 0
    while True:
        cnt = 0
        for x in event_list:
            ## 1Message
            if x[0] == 'SEND':
                broadcastData(x[1])
            ## 1Conn, 2Target user, 3Message
            elif x[0] == 'SEND-PRIVATE':
                broadcastPrivate(x[1],x[2],x[3])
            ## 1Conn, 2Message
            elif x[0] == 'Send-Thread':
                try:
                    x[1].send(x[2]+'<e%$>')
                except:
                    pass
            ## 0Thread, 1connecton, 2usrname, 3[0]ip, 3[1]port, 4lvl,5afk,6client version
            elif x[0] == 'USR-APPEND':
                threadip.append([x[1],x[2],x[3],x[4],x[5],x[6],x[7]])
                user_count += 1
            elif x[0] == 'USR-REM':
                usrLeaving(x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9])
                user_count -= 1
                try:
                    x[1].close()
                except Exception as e:
                    e = str(e)
                    print e
                Thread(target=clientHandler,args=(x[5],)).start()
            elif x[0] == 'Save-Users':
                save_user_settings()
            cnt += 1
        for x in range(0,cnt):
            del event_list[0]
        sleep(0.05)
        if user_count < 1000:
            sleep_more = 0.002*user_count
            sleep(sleep_more)
        else:
            sleep(2)
    

def clientHandler(i):
    global threadip, threads, msgprint_enabled, logging_enabled, welcome_msg, iplist, action_time, shared_filelist
    username,username2,username_set,authed_user,off_msg = '','', False, True, '0'
    level, timeouts, usr_ver = 1, 0, 'unknown'
    conn, addr = s.accept() # awaits for a client to connect and then accepts 
    print get_cur_time(),addr," connected!"
    chatlog.append([get_cur_time(),addr[0]," connected!"])
    ## 0Thread, 1connecton, 2usrname, 3[0]ip, 3[1]port, 4lvl,5afk,6client version
    event_list.append(['USR-APPEND',str(i),conn,'',[addr[0],addr[1]],1,'1',usr_ver])
    looping,cnt = True, 0
    while looping:
        sleep(0.01)
        for x in threadip:
            b = x[0].find(str(i))
            if b is not -1:
                looping = False
        cnt += 1
        if cnt == 15:
            break
    event_list.append(['Send-Thread',conn,welcome_msg])
    looping = True
    while looping:
        data_list = recieveData(conn,4096)
        if data_list == []:
            data_list = ['close::']
        for data in data_list:
            if data != 'kpALIVE::' and data != 'TIMEOUT::':
                chatmlog.append([get_cur_time(),username,data])
            ## User messages
            if data[0:9] == 'MESSAGE::' and username_set is True:
                timeouts = 0
                ## Prints message (if enabled)
                if msgprint_enabled == 1:
                    print get_cur_time(),username2,data[9:]
                ## Server commands lvl 7+
                if data[9:11] == 's/' and level > 7:
                    if data == 'MESSAGE::s/log':
                        event_list.append(['Send-Thread',conn,'WSERVER::Sending '+str(len(chatlog))+' lines'])
                        Thread(target=list_sender_thread,args=(conn,chatlog,'',)).start()
                    elif data == 'MESSAGE::s/mlog':
                        event_list.append(['Send-Thread',conn,'WSERVER::Sending '+str(len(chatmlog))+' lines'])
                        Thread(target=list_sender_thread,args=(conn,chatmlog,'',)).start()
                    elif data == 'MESSAGE::s/threadip':
                        Thread(target=list_sender_thread,args=(conn,threadip,'',)).start()
                    elif data == 'MESSAGE::s/fld':
                        for x in shared_filelist:
                            fh = open(x[0], 'a')
                            fh.write(x[1])
                            fh.close()
                        event_list.append(['Send-Thread',conn,'WSERVER::Saved'])
                ## Server commands lvl 3+
                if data[9:11] == 's/' and level > 3:
                    if data == 'MESSAGE::s/help':
                        event_list.append(['Send-Thread',conn,'WSERVER::Available commands to lvl 4+\n'+
                                           's/log - log\ns/mlog - message log\ns/threadip - thread list\n'+
                                           's/fld - save all files to disk\n'+
                                           's/clear files - clear all shared files from RAM\n'+
                                           's/filelist - returns list of shared files'])
                    elif data == 'MESSAGE::s/clear files':
                        shared_filelist = []
                        event_list.append(['SEND','SSERVER::'+username2+' cleared all shared files'])
                    elif data == 'MESSAGE::s/filelist':
                        Thread(target=list_sender_thread,args=(conn,threadip,'filelist-message',)).start()
                ## Low lvl warning
                elif data[9:11] == 's/' and level < 4:
                    event_list.append(['Send-Thread',conn,'WSERVER::Level too low'])

                ## Private user messages
                elif data[9:11] == '@@' and data[11] is not " ":
                    b = data[:].find(']')
                    if b is -1:
                        event_list.append(['Send-Thread',conn,'WSERVER::"]" has to be at the end of username'])
                    else:
                        usr_to_send = data[11:b]
                        event_list.append(['SEND-PRIVATE',conn,usr_to_send, 'm:'+sendlevel+username+'@@'+usr_to_send+data[b:]])
                ## User channel messages
                else:
                    event_list.append(['SEND','m:'+sendlevel+username+data[9:]])
            ## Leaving
            elif not data:
                event_list.append(['USR-REM',conn,username2,addr,threadip,i,username_set,authed_user,off_msg,'no'])
                looping = False
                break
            ## Leaving2
            elif data == 'close::' or data == 'TIMEOUT::':
                if data == 'close::':
                    event_list.append(['USR-REM',conn,username2,addr,threadip,i,username_set,authed_user,off_msg,'no'])
                else:
                    event_list.append(['USR-REM',conn,username2,addr,threadip,i,username_set,authed_user,off_msg,'TIMEOUT::'])
                looping = False
                break
            ## Requesting file list
            elif data[0:9] == 'RQFILES::':
                Thread(target=list_sender_thread,args=(conn,threadip,'filelist-list',)).start()
            ## Registration
            elif data[0:9] == 'aUSRREG::':
                registered = check_if_registered(username2,addr[0],False)
                if registered == True:
                    event_list.append(['Send-Thread',conn,'WSERVER::Already registered'])
                else:
                    usr_pass = data[9:]
                    if len(usr_pass) > 10:
                        usr_pass = usr_pass[:10]
                        event_list.append(['Send-Thread',conn,'SSERVER::Max length is 10, changed to: '+usr_pass])
                    illeg_chk = check_for_illegal_chr([' ','[',']'],usr_pass)
                    if illeg_chk == True:
                        event_list.append(['Send-Thread',conn,'WSERVER::Spaces, "[", "]" are not allowed'])
                    else:
                        event_list.append(['Send-Thread',conn,'WSERVER::Registering '+username2+' with '+usr_pass])
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
                    event_list.append(['SEND','SSERVER::'+remove_spaces(username)+' is level'+str(level)])
                    for x in threadip:
                        if x[0] == str(i):
                            x[2] = username2
                            x[4] = level
                            break
                    username_set, authed_user = True, True
                    remove_offline_usr(username2)
                    send_ulist_only()
                    event_list.append(['Send-Thread',conn,'WSERVER::Accepted'])
                    send_offline_msg(username_set,authed_user,username2,conn)
                    event_list.append(['Send-Thread',conn,'DUPLICT::'+username2])
                else:
                    event_list.append(['Send-Thread',conn,'WSERVER::Wrong pass'])
            ## Configure offline msg and client version
            elif data[0:9] == 'CONFIGR::':
                if username_set is True and authed_user is True:
                    b = data.find('offmsg=')
                    if b is not -1:
                        off_msg = data[b+len('offmsg=')]
                        for levels in iplist:
                            for x in levels[1]:
                                if x[0] == username2:
                                    x[2] = off_msg
                        register_user('a','a',False)
                        event_list.append(['Send-Thread',conn,'WSERVER::off_msg set to: '+off_msg])
                        event_list.append(['Save-Users'])
                b = data.find('ver=')
                if b is not -1:
                    usr_ver = data[b+len('ver='):]
                    b = usr_ver.find(' ')
                    if b is not -1:
                        usr_ver = usr_ver[:b]
                    if len(usr_ver) > 50:
                        usr_ver = usr_ver[:50]
                    for x in threadip:
                        if x[0] == str(i):
                            x[6] = usr_ver
                    send_ulist_only()
                            
                else:
    ##                sleep(0.1)
    ##                conn.send('WSERVER::You have no power here')
                    pass
            ## AFK
            elif data[0:9] == 'aAFKAFK::':
                for x in threadip:
                    if x[0] == str(i):
                        if x[5] == '1':
                            event_list.append(['SEND','SSERVER::'+username2+' is afk'])
                            newval = '0'
                        else:
                            event_list.append(['SEND','SSERVER::'+username2+' is no longer afk'])
                            newval = '1'
                        x[5] = newval
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
                        event_list.append(['Send-Thread',conn,'WSERVER::Name too long, shortened to 15 characters'])
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
                                    event_list.append(['Send-Thread',conn,'WSERVER::Name is registered, waiting for auth'])
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
                                    event_list.append(['Send-Thread',conn,'DUPLICT::'+username2])
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
                                    event_list.append(['Send-Thread',conn,'WSERVER::Name is registered, waiting for auth'])
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
                                    event_list.append(['Send-Thread',conn,'DUPLICT::'+username2])
                    send_offline_msg(username_set,authed_user,username2,conn)
        
            else:
                if data == 'kpALIVE::':
                    pass
                else:
                    sleep(0.05)
                    event_list.append(['Send-Thread',conn,"WSERVER::We don't accept this"])


def fileserver_handler():
    global shared_filelist, sf
    sf = socket(AF_INET, SOCK_STREAM)
    try:
        sf.bind(('', 44672))
    except:
        print "Can't bind address 2"
        sleep(2)
        quit()
    sf.listen(5)
    print "File server is running......"
    
    for i in range(1,6):
        new_fileserver_thread(i,sf)
    print '5 threads started\n'
    while True:
        cnt = 0
        for x in shared_filelist:
            x[4] -= 1
            if x[4] < 1: shared_filelist.pop(cnt)
            cnt += 1
        sleep(60)

def new_fileserver_thread(i,sf):
    Thread(target=fileserver_thread,args=(i,sf)).start()

def fileserver_thread(i,sf):
    global threadip, msgprint_enabled, logging_enabled, iplist, action_time, shared_filelist
    conn, addr = sf.accept() # awaits for a client to connect and then accepts 
    print get_cur_time(),addr," started a fileserver thread!"
    chatlog.append([get_cur_time(),addr[0]," connected to fileserver!"])
    ## 0Thread, 1connecton, 2usrname, 3[0]ip, 3[1]port, 4lvl,5afk
    state = 'auth'
    try:
        ## Sets client DL/UL mode
        conn.send('READY::')
        data = recieveData_file(conn,8192)
        sleep(0.05)
        ## DL
        if data[:10] == 'DOWNLOAD::':
            filename = data[10:]
            conn.send('READY::')
            data = recieveData_file(conn,8192)
            sleep(0.1)
            if data == 'SENDR::':
                found_file = False
                cnt = -1
                for x in shared_filelist:
                    cnt+=1
                    if x[0] == filename:
                        file_to_send = x[1] 
                        found_file = True
                if found_file == True:
                    pos = 0
                    filelen = len(shared_filelist[cnt][1])
                    cnt2 = 500
                    while True:
                        try:
                            conn.send(file_to_send[pos:pos+8192])
                        except:
                            conn.send(file_to_send[pos:])
                        cnt2 += 1
                        if cnt2 == 501:
                            if shared_filelist[cnt][4] < 5:
                                shared_filelist[cnt][4] = 5
                                cnt2 = 0
                        pos+=8192
                        if pos > filelen:
                            sleep(1)
                            conn.send('ENDING::')
                            break
                else:
                    conn.send('WrongName::')
      

        ## UL
        elif data == 'UPLOAD::':
            ## Gets username and password
            conn.send('READY::')
            data = recieveData_file(conn,8192)
            if data[0:9] == 'USRINFO::':
                b = data.find(']')
                if b is not -1 and len(data[b:]) > 2:
                    usr_pass = data[b+1:]
                    username = data[9:b]
                else:
                    usr_pass = ''
            else:
                usr_pass = ''
            registered = check_if_registered(username,addr,True)
            if registered[0] == True and registered[1] == usr_pass:
                state = 'filename'
            else:
                event_list.append(['SEND-PRIVATE','',username,'password is wrong'])
                conn.close()
            conn.send('READY::')
            ## Get filename
            if state == 'filename':
                data = recieveData_file(conn,8192)
                if data[0:9] == 'SENDFIL::' and len(data[9:]) > 0:
                    if len(data) > 140:
                        filename = data[9:140]+'...'
                    else:
                        filename = data[9:]
                    state = 'receiving'
                else:
                    conn.send('Wrong command, bye')
                    sf.close()
            ## Receive file
            if state == 'receiving':
                file_str = ''
                sleep(0.1)
                conn.send('SENDR::')
                while 1:
                    data = recieveData_file(conn,8192)
                    if data == 'ENDING::':
                        break
                    elif not data:
                        break
                    else:
                        file_str = file_str+data
                cnt = 0
                ## Check if duplicate
                again = False
                for x in shared_filelist:
                    if x[0] == filename:
                        cnt += 2
                if cnt > 0:
                    name_without_cnt = filename
                    while True:
                        again = False
                        filename = '('+str(cnt)+')'+name_without_cnt
                        for x in shared_filelist:
                            if x[0] == filename:
                                again = True
                        if again == False:
                            break
                        cnt += 1
                ## Gets file format
                file_format,cnt = str(filename), 0
                while True:
                    b = file_format.find('.')
                    if b is not -1:
                        file_format = file_format[b+1:]
                    else:
                        if cnt == 0:
                            file_format = 'unknown'
                            break
                        else:
                            break
                    cnt += 1
                        
                ## Puts in list and broadcasts
                global file_time
                shared_filelist.append([filename,file_str,file_format,get_cur_time(),file_time])
                event_list.append(['SEND','NEWFILE::'+username+']'+filename])
    except Exception as e:
        e = str(e)
        print 'File server thread crashed'
        print e
        try:
            conn.close()
        except:
            pass
    try:
        conn.close()
    except:
        pass
    new_fileserver_thread(i,sf)


def reset_offmsg_list():
    global off_users
    off_users = []
    for levels in iplist:
        for x in levels[1]:
            if x[2] == '1':
                off_users.append(x[0])

threads = int(read_settings('threadcnt=',60))
action_time = True
iplist,chatlog,chatmlog,threadip,off_users,off_messages,shared_filelist,event_list = [],[],[],[],[],[],[], []
read_server_usr_settings()
log_enabled = int(read_settings('logging=',1))
msgprint_enabled = int(read_settings('msgprint=',0))
file_time = int(read_settings('file_time=',2900))
reset_offmsg_list()
def main(): # main function
    global s,sf, action_time, msgprint_enabled, log_enabled, iplist, threads
    ## Chat server
    s = socket(AF_INET, SOCK_STREAM) # creates our socket; TCP socket
    try:
        s.bind(('', 44671)) # tells the socket to bind to localhost on port 44671
    except:
        print "Can't bind address"
        sleep(2)
        quit()
    s.listen(threads) # number of connections listening for
    print "Chat server is running......"

    for i in range(1,1+threads):
        Thread(target=clientHandler,args=(i,)).start()
    print str(threading.active_count()-1)+' threads started\n'
    
    Thread(target=fileserver_handler).start()
    
    Thread(target=eventThread).start()
    print 'eventThread started\n'
    
    while action_time is True:
        msg = raw_input('::: ')
        msg = str(msg)
        if msg == 'q':
            event_list.append(['SEND','CLOSING::'])
            action_time = False
            s.close()
            s = ''
            sleep(1)
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
            log-save, say, msgprint, msgprint-toggle, welcm, filelist, print-threads, start-threads, events"""
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
        elif msg == 'filelist':
            print 'Count ',len(shared_filelist)
            flsize = 0
            for x in shared_filelist:
                flsize += len(x[1])
                print x[0],'  MB:[',float(len(x[1]))/float(1052291),'] ', 'B:[',len(x[1]),']', 'Time:[',x[4],']'
            print 'Total size ',flsize
        elif msg == 'fld':
            for x in shared_filelist:
                fh = open(x[0], 'a')
                fh.write(x[1])
                fh.close()
        elif msg == 'msgprint-toggle':
            if msgprint_enabled is 1:
                msgprint_enabled = 0
            else:
               msgprint_enabled = 1
            write_settings('msgprint',msgprint_enabled)
        elif msg == 'say':
            x = raw_input(':::Say what? ')
            print 'Sending "'+x+'" to all'
            event_list.append(['SEND','SSERVER::'+x])
        elif msg == 'welcm':
            x = raw_input(':::message ')
            global welcome_msg
            welcome_msg = 'SSERVER::'+x
            event_list.append(['SEND','SSERVER::Welcome message is now: '+x])
        elif msg == 'print-threads':
            print str(threading.active_count())
        elif msg == 'start-threads':
            x = raw_input('How many?')
            try:
                x = int(x)
            except:
                x = 0
            threads += x
            for i in range(threads+1,threads+1+x):
                Thread(target=clientHandler,args=(i,)).start()
        elif msg == 'events':
            for x in event_list:
                print x
        else:
            print msg

main()
