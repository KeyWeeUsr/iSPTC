#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from Tkinter import Button as tkButton
from Tkinter import Label as tkLabel
from ttk import Style as ttkStyle
from ttk import Button
from ttk import Checkbutton
from ttk import Radiobutton
from ttk import Combobox
from ttk import Menubutton
from ttk import Scale
from ttk import Separator
from ttk import Treeview
from ttk import Label
##from ttk import Entry
from ttk import Widget
##from ttk import Frame as ttkFrame
from threading import Thread
from random import randrange
from time import strftime,gmtime,sleep,time
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from tkColorChooser import askcolor
from subprocess import *
from PIL import Image as Pillow_image
from PIL import ImageTk
import socket,os,platform,webbrowser, tkFont, urllib, urllib2, tkMessageBox, importlib

def set_winicon(window,name):
    global OS
    if OS is 'Windows':
        try:
            window.iconbitmap(sys_path+"\\"+"load\\"+name+".ico")
        except:
            print "Couldn't load windows icon"
    else:
        try:
            img = PhotoImage(file='load/'+name+'.png')
            window.tk.call('wm', 'iconphoto', window._w, img)
        except:
            print "Couldn't load Linux icon"
    

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
    a = readf('load/settings.ini')
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
        fh = open('load/settings.ini', 'a')
        fh.write('\n'+str(text_find)+str(c))
        fh.close()
    return c

def write_settings(text_find,new_value):
    global sys_path
    a = readf('load/settings.ini')
    a = edit_settings(a,text_find,new_value)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,'load/settings.ini')      

def play_sound(name,ignore):
    if sound_settings[0] == 1:
        global OS,sound_interval,dsound_interval
        if sound_interval < 0.5 or ignore == True:
            Thread(target=sound_thread,args=(name,)).start()
            if ignore == False:
                sound_interval = dsound_interval

def sound_thread(name):
    global OS
    if OS == 'Linux':
        os.popen('aplay %s' % ('load/'+name))
    elif OS == 'Windows':
        winsound.PlaySound(sys_path+"\\"+"load\\"+name,winsound.SND_FILENAME)

def list_from_file(path,delimiter):
    file_str = readf(path)
    templist = []
    cnt = 0
    for x in file_str:
        templist.append([])
        while True:
            b = x.find(delimiter)
            if b != -1:
                templist[cnt].append(x[:b])
                x = x[b+1:]
            else:
                templist[cnt].append(x)
                break
        cnt += 1
    return templist

class HyperlinkManager:
    def __init__(self, text,tag):
        self.text = text
        self.tagname = tag
        self.tag_hyper_colors(tag)

    def tag_hyper_colors(self,hyper):
        self.text.tag_config(hyper, underline=1)
        self.text.tag_bind(hyper, "<Enter>", self._enter)
        self.text.tag_bind(hyper, "<Leave>", self._leave)
        self.text.tag_bind(hyper, "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, addr):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = self.tagname+"-%d" % len(self.links)
        self.links[tag] = addr
        linklist.append([tag,addr])
        return self.tagname, tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == self.tagname+"-" or tag[:7] == self.tagname+"-":
                open_address_in_webbrowser(self.links[tag])
                return

class TT(Text):
    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)
        
    def copy(self, event=None):
        self.config(state="normal")
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)
        self.config(state="disabled")
    
    def cut(self, event):
        self.config(state="normal")
        self.copy()
        self.delete("sel.first", "sel.last")
        self.config(state="disabled")

    def paste(self, event):
        self.config(state="normal")
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)
        self.config(state="disabled")

def download_urlfile(filelink):
    filelink = filelink.rstrip()
    b = filelink.find('http://')
    if b is -1:
        filelink = 'http://'+filelink
    name = str(filelink)
    filehandle = urllib.urlopen(filelink)
    
    while True:
        nametemp = name.find('/')
        if nametemp is -1:
            break
        if nametemp is not -1:
            name = name[nametemp+1:]
    filer = urllib2.urlopen(filelink)
    name = name.rstrip()
    output = open(name,'wb')
    output.write(filer.read())
    output.close()

def lenghten_name(name,symbols):
    global nadd_spaces
    if nadd_spaces is 1:
        while len(name) < symbols:
            name = " " + name
    return name

def closewin():
    global s, action_time
    print 'Goodbye'
    write_settings('X_size',root.winfo_width())
    write_settings('Y_size',root.winfo_height())
    try:
        sender_thread_list.append('close::')
        action_time = False
        sleep(0.2)
        s.close()
        root.quit()
        try:
            root.destroy()
            quit
        except:
            pass
    except:
        sleep(0.2)
        root.quit()
        try:
            root.destroy()
            quit
        except:
            pass
    thread_message_list.append('QUIT::')

def get_cur_time():
    global show_ttime
    if show_ttime == 1:
        return ''
    if show_ttime == 2:
        return strftime("%H:%M")+' '
    if show_ttime == 3:
        return strftime("%H:%M:%S")+' '

def get_cur_time_log():
    global show_logtime
    if show_logtime == 1:
        return ''
    if show_logtime == 2:
        return strftime("%H:%M")+' '
    if show_logtime == 3:
        return strftime("%H:%M:%S")+' '

def cp_destroy(*arg):
    try:
        bb1.destroy()
    except:
        pass

def open_in_browser_btn():
    try:
        clipboardData = root.selection_get(selection="CLIPBOARD")
        done = True
    except:
        done = False
    try:
        copy_text()
        open_address_in_webbrowser(str(root.selection_get(selection="CLIPBOARD")))
    except:
        print 'Nothing in clipboard'
    if done == True:
        E.clipboard_clear()
        E.clipboard_append(clipboardData)    

def focus_hover_widget(*arg):
    try:
        global activated_widget
        activated_widget[1].focus_set()
    except:
        pass

def copy_paste_buttons_del_thread(*arg):
    focus_hover_widget()
    sleep(0.1)
    cp_destroy()

def copy_paste_buttons_del(*arg):
    Thread(target=copy_paste_buttons_del_thread).start()

def copy_paste_buttons(*arg):
    global bb1,m_x, m_y, activated_widget, usra_len, X_size, Y_size, show_users
    if activated_widget[0] == 'T' and show_users == 1:
        m_x += usra_len*8
    elif activated_widget[0] == 'E':
        m_y += Y_size-130
        if show_users == 0:
            m_x += usra_len*8
    elif activated_widget[0] == 'S2' and show_users == 1:
        m_x += usra_len*7
        
    if m_x > X_size-130:
        m_x = X_size-130
    if m_y > Y_size - 130:
        m_y = Y_size - 130
        
    cp_destroy()
    bb1 = Frame(root, height=108,width=142,borderwidth=2,relief=RIDGE)
    bb1.pack_propagate(0)
    bb1.place(x=m_x-2, y=m_y-2)
    
    bb2 = tkButton(bb1, text='Command window',justify=LEFT, width=20, command=lambda: {command_window(),cp_destroy()})
    bb2.pack()
    bb3 = tkButton(bb1, text='Clear', width=20,anchor=W, justify=LEFT, command=lambda: {textt.set(''),cp_destroy()})
    bb3.pack()
    bb4 = tkButton(bb1, text='Copy', width=20,anchor=W, justify=LEFT, command=lambda: {copy_text(),cp_destroy()})
    bb4.pack()
    bb5 = tkButton(bb1, text='Paste', width=20,anchor=W, justify=LEFT, command=lambda: {entry_paste(),cp_destroy()})
    bb5.pack()
    bb2.config(bd=0)
    bb3.config(bd=0)
    bb4.config(bd=0)
    bb5.config(bd=0)

def sender_thread():
    global sender_thread_list, s, action_time
    tim = 0
    while True:
        if len(sender_thread_list) > 0:
            try:
                s.send(sender_thread_list[0]+'<e%$>')
                sender_thread_list.pop(0)
            except Exception as e:
                print str(e)
                action_time = False
        else:
            if action_time == False:
                break
        tim+=(0.15)
        if tim > 6:
            sender_thread_list.append('kpALIVE::')
            tim = 0
        sleep(0.15)
        
def recv_thread():
    global action_time, s, connected_server
    buff = ''
    while action_time is True:
        try:
            data = buff+s.recv(4096)
            buff = ''
            if not data:
                if action_time is True:
                    action_time = False
                    Thread(target=jlost_reconnect).start()
                break
            ## Finds messages and appends
            cnt = 0
            while True:
                b = data.find('<e%$>')
                if b is not -1:
                    data_list.append(data[:b])
                    if len(data[b:]) > 4:
                        data = data[b+len('<e%$>'):]
                else:
                    if len(data) > 0:
                        buff += data
                    break
                cnt+= 1
                if cnt == 500:
                    tkMessageBox.showerror(title='Error', message='recv_thread looped 500 times')
                    break
        except:
            action_time = False
            Thread(target=jlost_reconnect).start()

def jlost_reconnect():
    global connected_server,kill_reconnect,User_area
    scroller = S.get()
    T_ins_warning(T,S,'Connection lost, attempting reconnect')
    clear_textbox(User_area,True)
    kill_reconnect = False
    cnt = 1
    while kill_reconnect is False:
        if cnt > 1:
            T_ins_warning(T,S,'attempting reconnect '+str(cnt)+'. time')
            if scroller[1] == 1.0:  
                T.yview(END)
        join_server(connected_server)
        cnt += 1
        sleep(15)
        if cnt == 50:
            kill_reconnect = True
        
def join_typing():
    global server_list
    server_list = []
    temp_text = readf('load/serverlist.ini')
    for x in temp_text:
        server_list.append(x)
    joinaddr = str(read_settings('joinaddr=',''))
    jaddr = StringVar()
    jaddr.set(joinaddr)
    jsrv = Toplevel()
    set_winicon(jsrv,'icon_grey')
    jsrv.title("Server address")
    jsrv.minsize(340,410)
    jsrv.resizable(FALSE,FALSE)

    frame = Frame(jsrv, height=260,width=300, relief=SUNKEN)
    frame.pack_propagate(0)
    frame.pack(padx=10,side=TOP)

    Label(frame, text="").pack(anchor=NW)
    Label(frame, text="Select from list:").pack(anchor=NW)
    display = Listbox(frame)
    scroll = Scrollbar(frame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    display.pack(fill=BOTH, expand=YES, side=TOP)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)
    for item in server_list:
        display.insert(END, item)

    Label(jsrv, text="").pack(side=TOP)
    Label(jsrv, text="Or type manually:").pack(side=TOP)
    usrEntry = Entry(jsrv,textvariable=jaddr)
    usrEntry.pack(side=TOP)
    usrEntry.focus_set()
    buttonframe = Frame(jsrv, height=30,width=120, relief=SUNKEN)
    buttonframe.pack_propagate(0)
    buttonframe.pack(padx=10,pady=20, side=TOP)
    button = Button(buttonframe, text='Join',command=lambda: {join_srv_check(display.curselection(),jaddr.get()),
                                                                jsrv.destroy()})
    button.pack(fill=BOTH, expand=1)
    def cmdbind(*arg):
        join_srv_check(display.curselection(),jaddr.get())
        jsrv.destroy()
    jsrv.bind('<Return>', cmdbind)
    def close_func(*arg):
        jsrv.destroy()
    jsrv.bind('<Escape>', close_func)

def join_srv_check(curselection,jaddr):
    global server_list
    if curselection is not ():
        join_server(server_list[curselection[0]])
    else:
        dontadd = False
        for x in server_list:
            if x == jaddr:
                dontadd = True
        if dontadd == False:
            fh = open('load/serverlist', 'a')
            fh.write(str(jaddr)+'\n')
            fh.close()
        join_server(jaddr)
                
def join_server(typing):
    global username, s, action_time, passwd, autoauth, offline_msg, kill_reconnect, connected_server, ver, sender_thread_list
    scroller = S.get()
    try:
        action_time = False
        s.send('close::'+'<e%$>')
        sleep(0.3)
        s.close()
    except:
        pass
    try:
        sender_thread_list = []
        if typing is not False:
            TCP_IP = typing
            TCP_PORT = 44671
            write_settings('joinaddr',TCP_IP)
            connected_server = typing
        else:
            joinaddr = str(read_settings('joinaddr=',''))
            TCP_IP = joinaddr
            TCP_PORT = 44671
            connected_server = joinaddr
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'joining',TCP_IP, TCP_PORT
        s.connect((TCP_IP, TCP_PORT))
        action_time = True
        Thread(target=recv_thread).start()
        if passwd is '' or autoauth is 0:
            s.send('USRINFO::'+username+'<e%$>')
        else:
            s.send('USRINFO::'+username+']'+passwd+'<e%$>')
        sleep(0.3)
        Thread(target=sender_thread).start()
        sender_thread_list.append('CONFIGR::offmsg='+str(offline_msg)+' ver=iSPTC-'+ver)
        kill_reconnect = True
    except Exception as e:
        e = str(e)
        T.config(yscrollcommand=S.set,state="normal")
        war = lenghten_name('WARNING: ',21)
        T.insert(END, get_cur_time()+war+e+"\n", 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")
    if scroller[1] == 1.0:  
        T.yview(END)

def scroller_to_end():
    scroller = S.get()
    if scroller[1] == 1.0:  
        T.yview(END)

def open_address_no_http(address):
    webbrowser.open(address)

def open_address_in_webbrowser(address):
    a = address.find('http://')
    b = address.find('https://')
    c = address.find('www.')
    if a == -1 and b == -1:
        webbrowser.open('http://'+address)
    else:
        webbrowser.open(address)

def Tbox_insert_lock(Tbx,Scr,text,tag):
    scroller = Scr.get()
    Tbx.config(yscrollcommand=Scr.set,state="normal")
    Tbx.insert(END, text, tag)
    Tbx.config(yscrollcommand=Scr.set,state="disabled")
    Tbx.yview(END)

def T_ins_userlist():
    global USRLIST
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, '[Userlist]\n', 'light-grey-bg')
    T.insert(END, '[Level] [AFK] [Name] [IP]\n', 'light-grey-bg')
    for x in USRLIST:
        while len(x) < 5:
            x.append('')
        try:
            ## Inserts Online and Offline text tagged
            if x[1] == 'olfo-':
                T.insert(END, x[0]+'\n','olfo-backgr')
            else:
                if x[0] == '' and x[1] == '' and x[2] == '':
                    pass
                elif x[2]!='-1':
                    if x[4] == 'unknown' or x[4] == '':
                        T.insert(END, x[2]+', '+x[3]+', '+x[0]+', '+x[1]+'\n', 'blackcol')
                    else:
                        T.insert(END, x[2]+', '+x[3]+', '+x[0]+', '+x[1]+', '+x[4]+'\n', 'blackcol')
        except Exception as e:
            print e
    T.config(yscrollcommand=S.set,state="disabled")
    T.yview(END)

def restore_toolbar():
    global show_toolbar, use_alternative_tlb, T, E, S, S2, User_area, toolbar
    if show_toolbar == 0:    
        if show_users == 1:
            User_area.destroy()
        T.destroy()
        E.destroy()
        S.destroy()
        S2.destroy()

        show_toolbar = 1
        create_widgets()
        user_area_insert()
        write_settings('show_toolbar',show_toolbar)
    else:
        toolbar.destroy()
        show_toolbar = 0
        write_settings('show_toolbar',show_toolbar)

def T_ins_help():
    global USRLIST
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, '[Help]\n', 'light-grey-bg')
    T.insert(END, 'Type:\n/help to see this message \n/u to show userlist\n/log to show chatlog\n'+
                '/afk to go afk\n/ll to see all links\n'+'/reg "password" to register\n'+
                '/auth "password" to authenticate\n/clear to clear textbox\n/share to share a file\n'+
                '/dl "filename" to download\n'+
                '/fm or /file_manager to open file manager\n/fl or /file_list to show file list\n'+
                '/files to open download folder\n'+
                '/join to open server join window\n/ljoin to join last server\n'+
                '/leave to leave\n/quit or /exit to close this application\n/about to open about window\n'+
                '/changelog to open changelog\n/toolbar to show/hide toolbar\n'
                , 'light-grey-bg')
    T.config(yscrollcommand=S.set,state="disabled")
    T.yview(END)

def T_ins_log():
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, '[Log]\n', 'light-grey-bg')
    for x in userlog_list:
        T.insert(END, x+'\n','light-grey-bg')
    T.config(yscrollcommand=S.set,state="disabled")
    T.yview(END)

def T_ins_datalist():
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, '[data_list]\n', 'light-grey-bg')
    for x in data_list:
        T.insert(END, x+'\n','light-grey-bg')
    T.config(yscrollcommand=S.set,state="disabled")
    T.yview(END)
    
def T_ins_linklist():
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, '[Link list]\n', 'light-grey-bg')
    for x in linklist:
        T.insert(END, x[1]+'\n','bluecol')
    T.config(yscrollcommand=S.set,state="disabled")
    T.yview(END)

def send_afk():
    try:
        sender_thread_list.append('aAFKAFK::')
    except:
        pass

def attempt_registration(s,authps):
    if len(authps) < 4:
        T_ins_warning(T,S,'Too short')
    else:
        try:
            sender_thread_list.append('aUSRREG::'+authps)
        except Exception as e:
            T.config(yscrollcommand=S.set,state="normal")
            war = lenghten_name('WARNING: ',21)
            if str(e)[:10] == '[Errno 32]':
                T.insert(END, get_cur_time()+war+'Not connected\n', 'redcol')
            else:
                T.insert(END, get_cur_time()+war+str(e)+'\n', 'redcol')
            T.config(yscrollcommand=S.set,state="disabled")
    T.yview(END)

def attempt_auth(s,authps):
    try:
        sender_thread_list.append('USRLOGI::'+authps)
    except Exception as e:
        T.config(yscrollcommand=S.set,state="normal")
        war = lenghten_name('WARNING: ',21)
        if str(e)[:10] == '[Errno 32]':
            T.insert(END, get_cur_time()+war+'Not connected\n', 'redcol')
        else:
            T.insert(END, get_cur_time()+war+str(e)+'\n', 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")
    T.yview(END)

def auth_register(auth_reg_var,t_passwd):
    global s, passwd
    passwd = t_passwd.get()
    write_settings('usrauth',passwd)   
    if auth_reg_var == 'register':
        attempt_registration(s,passwd)
        print 'Register with', passwd
    elif auth_reg_var == 'auth':
        attempt_auth(s,passwd)
        print 'Auth with', passwd
    T.yview(END)
    
def t_auth_window(auth_or_register):
    global passwd
    try:
        hhw.destroy()
    except:
        pass
    t_passwd = StringVar()
    t_passwd.set(passwd)
    hhw = Toplevel()
    set_winicon(hhw,'icon_grey')
    if auth_or_register == 'register':
        hhw.title("Register")
    if auth_or_register == 'auth':
        hhw.title("Auth")
    hhw.minsize(250,170)
    hhw.resizable(FALSE,FALSE)
    
    Label(hhw, text="Passwd:").pack(anchor=NW,padx=30,pady=10)
    usrEntry = Entry(hhw,textvariable=t_passwd)
    usrEntry.pack(side=TOP)
    usrEntry.focus_set()
    
    button = Button(hhw, text='Auth', command=lambda: {auth_register(auth_or_register,t_passwd),
                                                                hhw.destroy()})
    button.pack(side=BOTTOM,pady=10)
    def cmdbind(*arg):
        auth_register(auth_or_register,t_passwd)
        hhw.destroy()
    hhw.bind('<Return>', cmdbind)

def T_ins_file_list():
    global file_list, s
    sender_thread_list.append('RQFILES::')
    def append_files():
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, '[File list]\n', 'light-grey-bg')
        for x in file_list:
            T.insert(END, x[0]+' - '+x[1]+'\n', 'light-grey-bg')
        T.config(yscrollcommand=S.set,state="disabled")
        T.yview(END)
    root.after(300, append_files)

def T_ins_warning(T,S,text):
    T.config(yscrollcommand=S.set,state="normal")
    war = lenghten_name('WARNING: ',21)
    T.insert(END, get_cur_time()+war+text+'\n', 'redcol')
    T.config(yscrollcommand=S.set,state="disabled")

def chat_commands(text):
    global fdl_path
    if text == '/u' or text == '/usr' or text == '/users':
        T_ins_userlist()
    elif text == '/help':
        T_ins_help()
    elif text == '/log':
        T_ins_log()
    elif text == '/datal':
        T_ins_datalist()
    elif text == '/afk':
        send_afk()
    elif text == '/ll':
        T_ins_linklist()
    elif text[:len('reg')+2] == '/reg ':
        attempt_registration(s,text[5:])
    elif text[:6] == '/auth ':
        attempt_auth(s,text[6:])
    elif text[:4] == '/dl ':
        Thread(target=fldownloader_thread,args=(text[4:],)).start()
    elif text[:6] == '/clear':
        reset_textbox()
    elif text == '/share':
        share_file()
    elif text == '/fm' or text == '/file_manager':
        file_manager()
    elif text == '/fl' or text == '/file_list':
        T_ins_file_list()
    elif text == '/files':
        open_address_no_http(fdl_path)
    elif text == '/join':
        join_typing()
    elif text == '/ljoin':
        join_server(False)
    elif text == '/leave':
        leave_server()
    elif text == '/quit' or text == '/exit':
        closewin()
    elif text == '/changelog' or text == '/changes':
        Changelog()
    elif text == '/about':
        About()
    elif text == '/toolbar':
        restore_toolbar()
    else:
        return True
    return False
                
def enter_text(*arg):
    global s, USRLIST, entry_message_arch
    E.focus_set()
    text_from_commandwin = False
    try:
        if arg[0] == 'command_window':
            text = arg[1]
            text_from_commandwin = True
    except:
        pass
    if text_from_commandwin == False:
        text = textt.get()
    check = True
    sending = True
    if len(text) > 0:
        entry_mlist.append(text)
        entry_message_arch = 0
        if text[0] == '/':
            sending = False
            chat_commands(text)
            textt.set('')
        elif text[0] is '@':
            b = text.find('/')
            if b is not -1:
                check = chat_commands(text[b:])
                if check == False:
                    sending = False
                    textt.set(text[:b])
        if check == True:
            if text[0] == '@':
                b = text.find(' ')
                if text[1] == '@':
                    c = text.find(']')
                    if c is not -1:
                        T.config(yscrollcommand=S.set,state="normal")
                        name = lenghten_name('Sending private: ',21)
                        T.insert(END, get_cur_time(), 'blackcol')
                        T.insert(END, name, 'browncol')
                        T.insert(END, text[1:]+'\n', 'blackcol')
                        T.config(yscrollcommand=S.set,state="disabled")
                        textt.set(text[:c+1])
                else:
                    if b is not -1:
                        textt.set(text[:b]+" ")
                    else:
                        textt.set(text+" ")
            else:
                textt.set('')
            if sound_settings[1] == 1:
                play_sound('beep1.wav',True)
            if sending is True:
                try:
                    mesig = unicode('MESSAGE::'+text)
                    mesig = mesig.encode('utf-8')
                    sender_thread_list.append(mesig)
                except Exception as ee:
                    T_ins_warning(T,S,str(ee))
    T.yview(END)

def clear_textbox(clt,disable):
    clt.config(yscrollcommand=S.set,state="normal")
    clt.delete(1.0,END)
    if disable == True:
        User_area.config(yscrollcommand=S.set,state="disabled")

def leave_server():
    global s,action_time, username
    root.title("iSPTC - "+username)
    war = lenghten_name('WARNING: ',21)
    try:
        sender_thread_list.append('close::')
        action_time = False
        sleep(0.2)
        s.close()
        s = ''
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, get_cur_time()+war+'Left server\n', 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")
        User_area.config(state="normal")
        User_area.delete(1.0,END)
        User_area.config(state="disabled")
    except Exception as e:
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, get_cur_time()+war+str(e)+'\n', 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")

def winf_is(vv):
    global windowfocus,icon_was_switched
    windowfocus = True
    if icon_was_switched is True:
        set_winicon(root,'icon')
        icon_was_switched = False
def winf_isnt(vv):
    global windowfocus
    windowfocus = False

def get_dict_item(dictio,item,default):
    for k, v in dictio.iteritems():
        if k == item:
            return v
    return default

class Log_viewer:       
    def __init__(self,**kwargs):
        global text_font
        self.title = get_dict_item(kwargs,'title','default')
        self.filefolder = get_dict_item(kwargs,'filefolder','/log')
        self.thread_status = 'Ready:'
        
        self.topwin = Toplevel()
        set_winicon(self.topwin,'icon_grey')
        self.topwin.title(self.title)
        self.topwin.minsize(700,500)

        self.frame3 = Frame(self.topwin, width=700,height=40, relief=SUNKEN)
        self.frame3.pack_propagate(0)
        self.frame3.pack(side=BOTTOM,pady=10)
        self.frame1 = Frame(self.topwin, width=150,height=460, relief=SUNKEN)
        self.frame1.pack_propagate(0)
        self.frame1.pack(side=LEFT,padx=10,pady=10)
        self.frame2 = Frame(self.topwin, width=550,height=460, relief=SUNKEN)
        self.frame2.pack_propagate(0)
        self.frame2.pack(side=LEFT,padx=10,pady=10)
        self.frame4 = Frame(self.frame3, width=450,height=40, relief=SUNKEN)
        self.frame4.pack_propagate(0)
        self.frame4.pack(side=RIGHT)

        self.label1 = Label(self.frame1,text='Files:')
        self.label1.pack(side=TOP)
        self.Fscroll = Scrollbar(self.frame1)
        self.Fscroll.pack(side=RIGHT, fill=Y, expand=NO)
        self.listbox = Listbox(self.frame1)
        self.listbox.pack(expand=1, fill="both")
        self.Fscroll.configure(command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.Fscroll.set)

        self.Tbox = Text(self.frame2, height=12, width=40,wrap=WORD)
        self.Tbox.tag_configure('blackcol', font=text_font, foreground='black')
        self.Tbox.tag_configure('redcol', font=text_font, foreground='red')
        self.Tbox.configure(inactiveselectbackground="#6B9EB7", selectbackground="#4283A4")
        self.Tbox.tag_raise("sel")
        self.Tscroll = Scrollbar(self.frame2)
        self.Tbox.focus_set()
        self.Tbox.config(yscrollcommand=self.Tscroll.set)
        self.Tscroll.config(command=self.Tbox.yview)
        self.Tscroll.pack(side=RIGHT, fill=Y)
        self.Tbox.pack(side=BOTTOM,fill=BOTH,expand=1)

        self.loadLabel = Label(self.frame3,text='Ready:')
        self.loadLabel.pack(side=LEFT,padx=30)
        bb1 = Button(self.frame4, text='Change folder', command=self.load_other_folder)
        bb1.pack(side=LEFT,padx=30)
        bb2 = Button(self.frame4, text='Save', command=self.save_file)
        bb2.pack(side=LEFT)
        bb3 = Button(self.frame4, text='Close', command=self.close_func)
        bb3.pack(side=LEFT,padx=30)

        self.reload_file_list()
        self.topwin.bind('<Escape>', self.close_func)
        self.topwin.bind("<Control-a>", widget_sel_all)
        self.Tbox.bind('<Control-f>',lambda x: search_text_dialog(self.Tbox))
        self.listbox.bind('<Button-1>', lambda x: self.topwin.after(20,self.file_loader))
        self.topwin.protocol('WM_DELETE_WINDOW', self.close_func)
        self.topwin.after(200,self.after_task)
        self.colortag()

    def after_task(self):
        self.topwin.bind('<Configure>', self.on_resize)

    def reload_file_list(self):
        try:
            self.listbox.delete(0, END)
            file_list = os.listdir(self.filefolder)
            for x in file_list:
                self.listbox.insert("end", x)
        except Exception as e:
            self.Tbox.insert(END, str(e), 'redcol')
            self.Tbox.yview(END)

    def load_other_folder(self):
        self.topwin.lower()
        try:
            self.topwin.unbind('<Configure>')
            self.filefolder = (askdirectory()+'/')
            self.reload_file_list()
            self.topwin.after(300,self.after_task)
        except Exception as e:
            self.Tbox.insert(END, str(e), 'redcol')
            self.Tbox.yview(END)
        self.topwin.lift()
        self.colortag()

    def save_file(self):
        self.topwin.unbind('<Configure>')
        if self.thread_status == 'Ready:':
            self.thread_status = 'Working:'
            self.loadLabel.configure(text= self.thread_status)
            try:
                if os.path.exists(self.filefolder + self.title):
                    savef('',self.filefolder + self.title)
                    fh = open(self.filefolder + self.title, 'a')
                    text = self.Tbox.get(1.0, END)
                    fh.write(text)
                fh.close()
                self.thread_status = 'Ready:'
                self.loadLabel.configure(text= self.thread_status)
            except Exception as e:
                self.Tbox.insert(END, str(e), 'redcol')
                self.Tbox.yview(END)
        self.topwin.after(200,self.after_task)
                
    def file_loader(self):
        num = self.listbox.get(self.listbox.curselection())
        try:
            text = readf(self.filefolder+num)
        except Exception as e:
            self.Tbox.insert(END, str(e), 'redcol')
            self.Tbox.yview(END)
        if self.thread_status == 'Ready:':
            self.thread_status = 'Working:'
            self.topwin.unbind('<Configure>')
            self.loadLabel.configure(text= self.thread_status)
            self.title = num
            self.topwin.title(self.title)
            try:
                Thread(target=self.file_loader_thread,args=(text,)).start()
            except Exception as e:
                self.Tbox.insert(END, str(e), 'redcol')
                self.Tbox.yview(END)
    def file_loader_thread(self,text):
        try:
            cnt = [0,0.01]
            filelen = len(text)
            self.Tbox.delete(1.0,END)
            for x in text:
                self.Tbox.insert(END, x+'\n','blackcol')
                cnt[0]+= 1
                if cnt[0] > filelen*cnt[1]:
                    self.loadLabel.configure(text = self.thread_status+' '+str(cnt[0])+'/'+str(filelen))
                    self.Tbox.yview(END)
                    cnt[1] += 0.01
        except Exception as e:
            self.Tbox.insert(END, str(e), 'redcol')
        self.thread_status = 'Ready:'
        self.loadLabel.configure(text= self.thread_status)
        self.Tbox.yview(END)
        self.topwin.after(200,self.after_task)

    def on_resize(self,*arg):
        try:
            self.wX = self.topwin.winfo_width()
            self.wY = self.topwin.winfo_height()
            self.frame1_xsize = 120+0.05*self.wX
            self.frame1_ysize = self.wY-50
            self.frame2_xsize = self.wX-(120+0.05*self.wX)
            self.frame2_ysize = self.wY-50
            self.frame3_xsize = self.wX*1.00
            self.frame3_ysize = 40
            self.frame4_xsize = self.frame3_xsize/1.55
            self.frame4_ysize = self.frame3_ysize
            self.frame1.config(width=self.frame1_xsize,height=self.frame1_ysize)
            self.frame2.config(width=self.frame2_xsize,height=self.frame2_ysize)
            self.frame3.config(width=self.frame3_xsize,height=self.frame3_ysize)
            self.frame4.config(width=self.frame4_xsize,height=self.frame4_ysize)
        except Exception as e:
            self.Tbox.insert(END, str(e), 'redcol')
            self.Tbox.yview(END)

    def colortag(self):
        tag_colors(text=[self.Tbox],scroll=[self.Tscroll,self.Fscroll],listbox=[self.listbox],window=[self.topwin],
                   frame=[self.frame1,self.frame2,self.frame3,self.frame4],label=[self.label1,self.loadLabel])

    def widget_sel_all(self,*arg):
        self.Tbox.tag_add(SEL, "1.0", END)
        self.Tbox.mark_set(INSERT, "1.0")
        self.Tbox.see(INSERT)
    def close_func(self,*arg):
        self.topwin.destroy()

def popen_text_editor(file_folder):
    global OS
    INPUT = 'python editor.py '+file_folder
    if OS == 'Windows':
        if os.path.exists('editor.exe') == True: INPUT = 'editor.exe '+file_folder
    elif OS == 'Linux': INPUT = 'python editor.py '+file_folder
    Popen([INPUT], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)

def start_update(update_list):
    global OS
    upd_str = ""
    savef('','load/upd_filelist')
    for x in update_list:
        fh = open('load/upd_filelist', 'a')
        fh.write(x)
        fh.close()
    if OS == 'Windows':
        if os.path.exists('updater.exe') == True:
            INPUT = 'updater.exe'
    elif OS == 'Linux':
        INPUT = 'python updater.py'
    Popen([INPUT], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    closewin()

def autojoiner():
    global autojoin
    if autojoin == 1:
            join_server(False)

def updater_updater(ufile):
    global updater_ver, update_link
    ## Checks ver
    temp_list, yes = [], False
    for x in ufile:
        x = x.rstrip()
        temp_list.append(x)
        
    if temp_list[0] != updater_ver:
        print temp_list[0] , updater_ver
        yes = True
    ## Creates dialogue window
    if yes == True:
        def update_updater():
            global updater_ver
            try:
                for x in temp_list[1:]:
                    download_urlfile(x)
                    print x
                write_settings('updater_ver',temp_list[0])
                tkMessageBox.showinfo(title='Update', message='Updater has been updated')
                updater_ver = temp_list[0]
                topwin.destroy()
                update_checker(update_link)
            except Exception as e:
                e = str(e)
                tkMessageBox.showerror(title='Error', message=str(e))
        
        def close_func(*arg):
            topwin.destroy()
    
        topwin = Toplevel()
        set_winicon(topwin,'icon_grey')
        topwin.title("Updater updater")
        topwin.minsize(400,150)
        topwin.resizable(FALSE,FALSE)

        msg = Message(topwin,width=300, text="Updater has to be updated\nNew version is - ver: "+temp_list[0])
        msg.config(font=('Arial', 16))
        msg.pack(pady=15)

            
        topwin.bind('<Escape>', close_func)
        
        button = Button(topwin, text='Update', command=update_updater)
        button.place(x=80,y=100)
        button = Button(topwin, text='Close', command=close_func)
        button.place(x=220,y=100)
        topwin.lift()
            
    return yes

def update_checker(update_link):
    global ver, updater_ver
    strver = str(ver)
    update = False
    strver = '0'+str(ver)
    
    ## Downloads update information from http://exampleaddr.com/example/win_exe/latest and /latest_updater
    if update_link[-1:] == '/':
        update_link = update_link[:-1]
    b = update_link.find('http://')
    if b is -1:
        update_link = 'http://'+update_link
    update_link_file = update_link+'/latest_updater'
    filehandle = urllib.urlopen(update_link_file)
    print update_link_file
    ## Updates updater
    new_update_ver = updater_updater(filehandle)

    ## Checks client version and opens update window if ver is different
    if new_update_ver == False:
        update_link_file = update_link+'/latest'
        filehandle = urllib.urlopen(update_link_file)

        temp = []
        for x in filehandle:
            temp.append(x)
            
        upd_ver = temp[0]
        upd_ver = upd_ver.rstrip()
        if upd_ver != strver:
            update = True
        if update == True:
            update_window(update_link,strver,update,temp,upd_ver)
        else:
            autojoiner()

def update_window(update_link,strver,update,temp,upd_ver):
    global text_font, show_users
    global ver
    topwin = Toplevel()
    set_winicon(topwin,'icon_grey')
    topwin.title("Updater")
    topwin.minsize(700,600)
    topwin.resizable(FALSE,FALSE)

    Label(topwin, text="Update link is "+update_link).pack()
    Label(topwin, text="Current version is "+strver).pack()
    Label(topwin, text="New version is "+upd_ver).pack()
    Label(topwin, text="Update file:").pack(pady=10)

    frame = Frame(topwin, height=210,width=680, relief=SUNKEN)
    frame.pack_propagate(0)
    frame.pack(anchor=NE,side=TOP,padx=20)
    frame2 = Frame(topwin, height=210,width=680, relief=SUNKEN)
    frame2.pack_propagate(0)
    frame2.pack(anchor=NE,side=TOP,padx=20)

    Label(frame, text="Comment:").pack(side=BOTTOM)
    Tbox2 = Text(frame, height=12, width=50,wrap=WORD)
    S11 = Scrollbar(frame)
    S11.pack(side=RIGHT, fill=Y)
    Tbox2.pack(side=BOTTOM,fill=BOTH,expand=1)
    Tbox2.config(yscrollcommand=S11.set,state="normal")
    S11.config(command=Tbox2.yview)
    for x in temp:
        Tbox2.insert(END, x,'blackcol')
        
    Tbox2.config(yscrollcommand=S11.set,state="disabled")
    Tbox = Text(frame2, height=12, width=50,wrap=WORD)
    Tbox.tag_configure('blackcol', font=text_font, foreground='black')
    Tbox.tag_configure('CL-bg', font=text_font, background='#80ccff',foreground='black')
    Tbox.tag_configure('SE-bg', font=text_font, background='#66cc66',foreground='black')
    Tbox.tag_configure('light-bg', font=text_font, background='#f3f3f3',foreground='black')
    Tbox2.tag_configure('blackcol', font=text_font, foreground='black')
    S1 = Scrollbar(frame2)
    S1.pack(side=RIGHT, fill=Y)
    Tbox.pack(side=BOTTOM,fill=BOTH,expand=1)
    Tbox.config(yscrollcommand=S1.set,state="normal")
    S1.config(command=Tbox.yview)

    downlist= []
    if update == True:
         for x in temp:
            ## Inserts comments into Text box
            b = x.find('comment,')
            if b is not -1:
                commentlink = x[len('comment')+1:]
                if commentlink.find('http://') is -1:
                    commentlink = 'http://'+commentlink
                filer = urllib2.urlopen(commentlink)
                for x in filer:
                    if x[:5] == '## Cl':
                        Tbox.insert(END, x,'CL-bg')
                    elif x[:5] == '## Se':
                        Tbox.insert(END, x,'SE-bg')
                    elif x[:3] == '###':
                        Tbox.insert(END, x,'light-bg')
                    else:
                        Tbox.insert(END, x,'blackcol')
            ## Passes information to updater
            else:
                downlist.append(x)
    Tbox.config(yscrollcommand=S1.set,state="disabled")

    def close_func(*arg):
        topwin.destroy()
    topwin.bind('<Escape>', close_func)
    button = Button(topwin, text='Update', command=lambda: {start_update(downlist)})
    button.place(x=180,y=540)
    button2 = Button(topwin, text='Close', command=lambda: {autojoiner(),topwin.destroy()})
    button2.place(x=360,y=540)
    topwin.lift()

def command_window(*arg):
    global text_font
    cww = Toplevel()
    set_winicon(cww,'icon_grey')
    cww.title("Command..")
    cww.minsize(500,70)
    cww.resizable(FALSE,FALSE)
    frame = Frame(cww, height=70,width=460, relief=SUNKEN)
    frame.pack(side=TOP,pady=20)
    frame.pack_propagate(0)

    t_encommand = StringVar()
    Label(frame, text="Enter command:").pack(anchor=NW)
    tEntry = Entry(frame,textvariable=t_encommand)
    tEntry.pack(pady=5,fill=BOTH)
    tEntry.focus_set()
    tEntry.configure(font=text_font, foreground='black')
    button = Button(cww, text='Close', command=lambda: {enter_text('command_window',t_encommand.get()),
                                                                  cww.destroy()})
    button2 = Button(cww, text='Run', command=lambda: {enter_text('command_window',t_encommand.get()),
                                                                  cww.destroy()})
    button.pack(side=LEFT,padx=60,pady=20)
    button2.pack(side=LEFT,padx=60,pady=20)
    def run_func(*arg):
        enter_text('command_window',t_encommand.get())
        cww.destroy()
    def close_func(*arg):
        cww.destroy()
    cww.bind('<Return>', run_func)
    cww.bind('<Escape>', close_func)

def change_name(t_new_name,t_passwd,t_offline_msg):
    global username, s, passwd, offline_msg
    new_name = t_new_name.get()
    new_passwd = t_passwd.get()
    if new_passwd != passwd or new_name != username:
        passwd = t_passwd.get()
        write_settings('usrauth',passwd)
        if len(new_name) <3:
            T.config(yscrollcommand=S.set,state="normal")
            war = lenghten_name('WARNING: ',21)
            T.insert(END, get_cur_time()+war+'Name is too short\n', 'redcol')
            T.config(yscrollcommand=S.set,state="disabled")
        else:
            username = new_name
            root.title("iSPTC - "+new_name)
            write_settings('username',username)
            try:
                if passwd is '':
                    sender_thread_list.append('USRINFO::'+username)
                else:
                    sender_thread_list.append('USRINFO::'+username+']'+passwd)
            except:
                pass
        
    new_offline_msg = t_offline_msg.get()
    if new_offline_msg != offline_msg:
        offline_msg = new_offline_msg
        write_settings('offline_msg',offline_msg)
        try:
            sender_thread_list.append('CONFIGR::offmsg='+str(offline_msg))
        except:
            pass

def username_menu():
    global username, passwd, offline_msg
    uw = Toplevel()
    set_winicon(uw,'icon_grey')
    uw.title("User")
    uw.minsize(250,170)
    uw.resizable(FALSE,FALSE)
    
    t_new_name = StringVar()
    t_new_name.set(username)
    t_passwd = StringVar()
    t_offline_msg = IntVar()
    t_passwd.set(passwd)
    t_offline_msg.set(offline_msg)
    
    Label(uw, text="Username:").pack(anchor=NW,padx=35,pady=5)
    usrEntry = Entry(uw,textvariable=t_new_name)
    usrEntry.pack(pady=5)
    usrEntry.focus_set()

    Label(uw, text="Password (leave blank, if unused):").pack(anchor=NW,padx=35)
    usrEntry = Entry(uw,textvariable=t_passwd)
    usrEntry.pack(pady=5)
    usrEntry.focus_set()
    Checkbutton(uw, text="Enable offline messages", variable=t_offline_msg).pack(anchor=NW,padx=35)
    button = Button(uw, text='Save', command=lambda: {change_name(t_new_name,t_passwd,
                                                            t_offline_msg),uw.destroy()})
    button.pack(side=BOTTOM,pady=10)
    Label(uw, text="(Requires registration)").pack(anchor=N,padx=35)
    def cmdbind(*arg):
        change_name(t_new_name,t_passwd,t_offline_msg)
        uw.destroy()
    uw.bind('<Return>', cmdbind)
    def close_func(*arg):
        uw.destroy()
    uw.bind('<Escape>', close_func)
    
def change_sound_set(a,b,c,d):
    global dsound_interval
    ### 0all_sound, 1entry, 2user textbox
    sound_settings[0] = a
    sound_settings[1] = b
    sound_settings[2] = c
    dsound_interval = float(d)
    write_settings('enable_sound',a)
    write_settings('entry_enabled',b)
    write_settings('user_textbox',c)
    write_settings('sound_interval',d)

def sound_menu():
    global dsound_interval
    sw = Toplevel()
    set_winicon(sw,'icon_grey')
    sw.title("Sound settings")
    sw.minsize(280,180)
    sw.resizable(FALSE,FALSE)

    sound_enabled = IntVar()
    entry_enabled = IntVar()
    user_textbox = IntVar()
    snd_interval = StringVar()
    snd_interval.set(str(int((dsound_interval))))
    sound_enabled.set(sound_settings[0])
    entry_enabled.set(sound_settings[1])
    user_textbox.set(sound_settings[2])
    
    Checkbutton(sw, text="Enable sound", variable=sound_enabled).grid(row=1, sticky=W,padx=20)
    Checkbutton(sw, text="Entry sound", variable=entry_enabled).grid(row=2, sticky=W,padx=20)
    Checkbutton(sw, text="Textbox sound", variable=user_textbox).grid(row=3, sticky=W,padx=20)
    Label(sw, text="Chat sound interval").grid(row=1,padx=140)
    snd_interval_Entry = Entry(sw,textvariable=snd_interval,width=5).place(x=145,y=20)
    Label(sw, text="seconds").place(x=190,y=22)
##    snd_interval = Scale(sw, from_=0, to=30,length=120, orient=HORIZONTAL)
##    snd_interval.grid(row=2,padx=160)
##    snd_interval.set(int(dsound_interval))
    button = Button(sw, text='Save', command=lambda: {change_sound_set(sound_enabled.get(),entry_enabled.get(),
                                                user_textbox.get(),snd_interval.get()),sw.destroy()})
    button.grid(row=6, padx=60,pady=30)
    def close_func(*arg):
        sw.destroy()
    sw.bind('<Escape>', close_func)
    
def color_asker(color):
    global default_os_color
    try:
        if color == 'default':
            color = default_os_color
        color2 = askcolor(color)[1]
    except:
        print 'Unknown color, using default'
        color2 = askcolor()[1]
    if color2 == None:
        return color
    return color2

            
def restore_window(name,Xpos,Ypos):
    name.wm_state('normal')
    name.lift()
    name.geometry('+'+Xpos+'+'+Ypos) 

def color_menu():
    global text_font, chat_color_list, saved_theme, default_os_color
    class Change_color_button(object):
        def __init__(self,frame2):
            self.ffg = 'red'
            self.fbg = 'white'
            self.make_buttons()
            self.theme_name = 'Default'
            listbox.bind('<Button-1>',lambda x: self.reset_colorbutton())
            listbox_theme.bind('<Button-1>',lambda x: self.theme_loader())

        def theme_loader_after(self,*arg):
            num2 = listbox_theme.curselection()
            num = num2[0]
            self.theme_name = theme_list[num]
            load_theme(self.theme_name)
            self.reset_colorbutton()
            theme_var.set(self.theme_name)
        def theme_loader(self,*arg):
            topwin.after(10, self.theme_loader_after)
            
        def color_picker(self,which):
            try:
                num2 = listbox.curselection()
                num = num2[0]
                self.ffg=chat_color_list[num][3]
                self.fbg=chat_color_list[num][4]
                topwin.lower()
                if which == 'Foreground':
                    chat_color_list[num][3] = color_asker(self.ffg)
                elif which == 'Background':
                    chat_color_list[num][4] = color_asker(self.fbg)
                elif which == 'All backgrounds':
                    newcol = askcolor()[1]
                    if newcol == None:
                        pass
                    else:
                        normalcol = chat_color_list[4][4]
                        answer = tkMessageBox.askquestion(title='W', message='Replace '+normalcol+' color only?')
                        if answer == 'yes':
                            for x in chat_color_list:
                                if x[4] == normalcol:
                                    x[4] = newcol
                        else:
                            for x in chat_color_list:
                                    x[4] = newcol
                self.reset_colorbutton()
                topwin.lift()
            except Exception as e:
                e = str(e)
                print e
                if e == 'tuple index out of range':
                    topwin.lower()
                    tkMessageBox.showerror(title='Error', message='Select a color')
                    topwin.lift()

        def set_default_colors(self):
            global chat_color_list, default_colors_list
            chat_color_list = []
            for x in default_colors_list:
                chat_color_list.append(list(x))
            self.reset_colorbutton()
            tag_colors(preset='default')
            
        def make_buttons(self):
            global default_os_color
            self.resbt = tkButton(frame2,text='Reset default', fg='black', bg='white',width=40,height=3,command=self.set_default_colors)
            self.resbt.pack(side=TOP,pady=15)
            self.frameb = Frame(frame2, height=380,width=450, relief=SUNKEN)
            self.frameb.pack_propagate(0)
            self.frameb.pack(side=BOTTOM,padx=50)
            normalc = (chat_color_list[4][3], chat_color_list[4][4])
            if normalc[1] == 'default':
                normalc = default_os_color
            fbg = self.fbg
            if fbg =='default':
                fbg = default_os_color
            self.button = tkButton(self.frameb,text='Foreground', fg=self.ffg, bg=fbg,width=10,height=3,
                                    command=lambda : self.color_picker('Foreground'))
            self.button.pack(side=LEFT,padx=5)
            self.button = tkButton(self.frameb,text='Background', fg=self.ffg, bg=fbg,width=10,height=3,
                                    command=lambda : self.color_picker('Background'))
            self.button.pack(side=LEFT,padx=5)
            self.button = tkButton(self.frameb,text='All backgrounds', fg=normalc[0], bg=normalc[1],width=10,height=3,
                                    command=lambda : self.color_picker('All backgrounds'))
            self.button.pack(side=LEFT,padx=5)

            
        def reset_colorbutton(self,*arg):
            topwin.after(10, self.after_timer)
            
        def after_timer(self):
            self.resbt.destroy()
            self.frameb.destroy()
            num2 = listbox.curselection()
            if num2 == ():
                num = 1
            else:
                num = num2[0]
            self.ffg=chat_color_list[num][3]
            self.fbg=chat_color_list[num][4]
            self.make_buttons()
            cnt = 0
            for x in chat_color_list:
                try:
                    listbox.itemconfig(cnt, bg=x[4])
                except:
                    listbox.itemconfig(cnt, bg='#DBDBDB')
                listbox.itemconfig(cnt, foreground=x[3])
                cnt += 1
            topwin.lift()

    def load_theme(saved_theme):
        templist = list_from_file('load/themes/'+saved_theme,',')
        global chat_color_list
        chat_color_list = []
        for x in templist:
            chat_color_list.append(list(x))
        if chat_color_list == []:
            chat_color_list = list(default_colors_list)
        
    def save_theme(*arg):
        global saved_theme
        savef('','load/themes/'+theme_var.get())
        fh = open('load/themes/'+theme_var.get(), 'a')
        for x in chat_color_list:
            fh.write(x[0]+','+x[1]+','+x[2]+','+x[3]+','+x[4]+'\n')
        fh.close()
        saved_theme = cColor_obj.theme_name
        write_settings('theme',cColor_obj.theme_name)

    def delete_theme(*arg):
        answer = tkMessageBox.askquestion(title='Delete theme', message='Are you sure?')
        if answer == 'yes':
            name = cColor_obj.theme_name
            os.remove('load/themes/'+name)
            listbox_theme.delete(0, END)
            theme_list = os.listdir('load/themes/')
            for x in theme_list:
                listbox_theme.insert("end", x)
        
            
    topwin = Toplevel()
    set_winicon(topwin,'icon_grey')
    topwin.title("Color settings")
    topwin.minsize(700,400)
    topwin.resizable(FALSE,FALSE)

    frame = Frame(topwin, height=380,width=400, relief=SUNKEN)
    frame.pack_propagate(0)
    frame.pack(anchor=NW,side=LEFT,padx=20,pady=15)
    frame5 = Frame(frame, height=380,width=195, relief=SUNKEN)
    frame5.pack_propagate(0)
    frame5.pack(side=LEFT)
    frame6 = Frame(frame, height=380,width=195, relief=SUNKEN)
    frame6.pack_propagate(0)
    frame6.pack(side=RIGHT)
    
    frame2 = Frame(topwin, height=380,width=450, relief=SUNKEN)
    frame2.pack_propagate(0)
    frame2.pack(anchor=NW,side=LEFT,padx=20)
    frame3 = Frame(frame2, height=30,width=450, relief=SUNKEN)
    frame3.pack_propagate(0)
    frame3.pack(side=BOTTOM)
    frame4 = Frame(frame2, height=40,width=450, relief=SUNKEN)
    frame4.pack_propagate(0)
    frame4.pack(side=TOP,pady=15)

    Label(frame5,text='Theme').pack()
    scroll = Scrollbar(frame5)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    listbox_theme = Listbox(frame5)
    listbox_theme.pack(expand=1, fill="both")
    scroll.configure(command=listbox_theme.yview)
    listbox_theme.configure(yscrollcommand=scroll.set)
    
    Label(frame6,text='Color').pack()
    scroll2 = Scrollbar(frame6)
    scroll2.pack(side=RIGHT, fill=Y, expand=NO)
    listbox = Listbox(frame6)
    listbox.pack(expand=1, fill="both")
    scroll2.configure(command=listbox.yview)
    listbox.configure(yscrollcommand=scroll2.set)
    theme_list = os.listdir('load/themes/')
    theme_list = sorted(theme_list)

    # Listbox
    for x in theme_list:
        listbox_theme.insert("end", x)
    for x in chat_color_list:
        listbox.insert("end", x[1])
    cnt = 0
    for x in chat_color_list:
        try:
            listbox.itemconfig(cnt, bg=x[4])
        except:
            listbox.itemconfig(cnt, bg='#DBDBDB')
        listbox.itemconfig(cnt, foreground=x[3])
        cnt += 1
            
    def close_func(*arg):
        topwin.destroy()
    def set_global_ntag(*arg):
        global saved_theme
        saved_theme = cColor_obj.theme_name
        tag_colors(preset='default')
    topwin.bind('<Escape>', close_func)

    lb = Label(frame4,text='Theme name')
    lb.pack(side=TOP)

    theme_var = StringVar()
    theme_var.set(saved_theme)
    themeEntry = Entry(frame4, textvariable=theme_var)
    themeEntry.textvariable = theme_var
    themeEntry.pack()
    
    cColor_obj = Change_color_button(frame2)
    button = Button(frame3, text='Delete', command=delete_theme)
    button.pack(side=LEFT,padx=55)
    button = Button(frame3, text='Apply', command=set_global_ntag)
    button.pack(side=LEFT,padx=10)
    button = Button(frame3, text='Save', command=lambda: {save_theme(),tag_colors(preset='default'), topwin.destroy()})
    button.pack(side=LEFT,padx=10)
    

def set_font(font,font_size,style, t_usra_len):
    global T,E,User_area, text_font, usra_len
    text_font = (font, font_size, style)
    
    User_area.config(width=t_usra_len)
    tag_colors(preset='default')
    usra_len = t_usra_len
    write_settings('font1',font)
    write_settings('font2',font_size)
    write_settings('font3',style)
    write_settings('usra_len',usra_len)
    
def font_menu():
    global text_font, usra_len
    fom = Toplevel()
    set_winicon(fom,'icon_grey')
    fom.title("Font settings")
    fom.minsize(700,400)
    fom.resizable(FALSE,FALSE)

    frame = Frame(fom, height=480,width=300, relief=SUNKEN)
    frame2 = Frame(fom, height=500,width=400, relief=SUNKEN)
    frame.pack_propagate(0)
    frame2.pack_propagate(0)
    frame.pack(anchor=NE,side=LEFT,padx=10,pady=10)
    frame2.pack(anchor=NE,side=LEFT)

    frame1 = Frame(frame, height=20,width=300, relief=SUNKEN)
    frame1.pack_propagate(0)
    frame1.pack(side=TOP,pady=5)
    frame1a = Frame(frame1, height=20,width=40, relief=SUNKEN)
    frame1a.pack_propagate(0)
    frame1a.pack(side=LEFT)
    frame1b = Frame(frame1, height=20,width=260, relief=SUNKEN)
    frame1b.pack_propagate(0)
    frame1b.pack(side=LEFT)

    t_font_size = IntVar()
    t_usra_len = IntVar()
    t_fontname = StringVar()
    t_style = StringVar()
    t_style_bold = StringVar()
    t_style_italic = StringVar()
    t_usra_len.set(usra_len)
    t_fontname.set(text_font[0])
    t_font_size.set(text_font[1])
    t_style.set(text_font[2])
    t_style_bold.set(0)
    t_style_italic.set(0)
    b = text_font[2].find('bold')
    if b != -1:
        t_style_bold.set(1)
    b = text_font[2].find('italic')
    if b != -1:
        t_style_italic.set(1)
        
    fonts=list(tkFont.families())
    fonts.sort()
    Label(frame1a, text="Font:",justify = LEFT).pack(side=LEFT)
    Efont_size = Entry(frame1b,textvariable=t_fontname,width=220).pack(side=LEFT)
    display = Listbox(frame)
    scroll = Scrollbar(frame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    display.pack(fill=BOTH, expand=YES, side=LEFT)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)
    for item in fonts:
        display.insert(END, item)
    
    Checkbutton(frame2, text="Bold ", variable=t_style_bold).place(x=180,y=370)
    Checkbutton(frame2, text="Italic", variable=t_style_italic).place(x=250,y=370)
    Label(frame2, text="Font size:",justify = LEFT).place(x=20,y=370)
    Efont_size = Entry(frame2,textvariable=t_font_size,width=3).place(x=100,y=370)
    Label(frame2, text="User_area length:",justify = LEFT).place(x=20,y=400)
    User_area_length = Entry(frame2,textvariable=t_usra_len,width=3).place(x=140,y=400)
    
    display_text = Text(frame2, height=22, width=50,wrap=WORD)
    display_text.place(x=10,y=15)
    display_text.insert(END, get_cur_time()+' Monospace: equal length\n','monocol')
    display_text.insert(END, get_cur_time()+' MONOSPACE: EQUAL LENGTH\n','monocol')
    display_text.insert(END, get_cur_time()+' Mouse: hello cat\n','privatecol')
    display_text.insert(END, get_cur_time()+' Twitterbot: Falcon has landed\n','olfo-backgr')
    display_text.insert(END, get_cur_time()+' SERVER: Hello human\n','bluecol')
    display_text.insert(END, get_cur_time()+' WARNING: Hello human\n','redcol')
    display_text.insert(END, get_cur_time()+' Human: Hello\n','greencol')
    display_text.insert(END, get_cur_time()+' SERVER: human is afk\n','greycol')
    display_text.insert(END, get_cur_time()+' Admin: /kick human\n','purplecol')
    display_text.insert(END, get_cur_time()+' Cat: hello\n','blackcol')
    display_text.insert(END, get_cur_time()+' Orange: the new color\n','orangecol')
    

    button2 = Button(frame2, text='Apply', command=lambda: {apply_chat_font(t_fontname.get(), t_font_size.get(),
                                                                             t_style.get())})
    button = Button(frame2, text='Save', command=lambda: {set_font(t_fontname.get(),t_font_size.get(),t_style.get(),
                                              t_usra_len.get()), fom.destroy()})
    button.place(x=200,y=450)
    button2.place(x=40,y=450)


    def preview_loop(*arg):
        show_selected_font()
        fom.after(100, preview_loop)
    def close_func(*arg):
        fom.destroy()
    def focusList(event):
        display.focus_set()
    def show_selected_font(*arg):
        style = ''
        if t_style_bold.get() == '1' and t_style_italic.get() == '1':
            style = 'bold italic'
        else:
            yes = False
            if t_style_bold.get() == '1':
                style = 'bold'
                yes = True
            if t_style_italic.get() == '1':
                style = 'italic'
                yes = True
            if yes == False:
                style = 'normal'
        t_style.set(style)
        if display.curselection() != ():
            t_fontname.set(fonts[display.curselection()[0]])
        apply_display_font(display_text,t_fontname.get(),t_font_size.get(),t_style.get())

    fom.bind('<Escape>', close_func)
    if OS != 'Windows':
        fom.bind("<Button-4>", focusList)
        fom.bind("<Button-5>", focusList)
    if OS == 'Windows':
        fom.bind("<MouseWheel>", focusList)
    fom.after(40, preview_loop)

def apply_chat_font(font,font_s,ttype):
    global text_font
    text_font = (font,font_s,ttype)
    tag_colors(preset='default')

def apply_display_font(display_text,selFont,font_size,ttype):
    try:
        font_size = t_font_size
    except:
        pass
    display_text.tag_configure('redcol', font=(selFont,font_size,ttype), foreground='red')
    display_text.tag_configure('bluecol', font=(selFont, font_size,ttype), foreground='blue')
    display_text.tag_configure('greencol', font=(selFont, font_size,ttype), foreground='#009900')
    display_text.tag_configure('purplecol', font=(selFont, font_size,ttype), foreground='purple')
    display_text.tag_configure('greycol', font=(selFont, font_size,ttype), foreground='#7F7F7F')
    display_text.tag_configure('blackcol', font=(selFont, font_size,ttype), foreground='black')
    display_text.tag_configure('orangecol', font=(selFont, font_size,ttype), foreground='#e65b00')
    display_text.tag_configure('privatecol', font=(selFont, font_size,ttype),foreground='white', background='#222222')
    display_text.tag_configure('olfo-backgr', font=(selFont, font_size,ttype),foreground='black', background='#c8d9ea')
    display_text.tag_configure('monocol', font=(selFont, font_size,ttype), foreground='#77ccff', background='#1e2c3c')
    

def save_update_settings(a,b):
    global update_enabled,update_link
    update_enabled = a
    update_link = b
    write_settings('update_enabled',a)
    write_settings('update_link',b)

def update_menu():
    global update_enabled,update_link
    upd = Toplevel()
    set_winicon(upd,'icon_grey')
    upd.title("Update settings")
    upd.minsize(500,100)
    upd.resizable(FALSE,FALSE)

    frame = Frame(upd, height=80,width=460, relief=SUNKEN)
    frame.pack(side=TOP,pady=20)
    frame.pack_propagate(0)

    t_update_enabled = IntVar()
    t_update_link = StringVar()
    t_update_enabled.set(update_enabled)
    t_update_link.set(update_link)
    
    Checkbutton(frame, text="Check at launch", variable=t_update_enabled).pack(anchor=NW,pady=5)
    Label(frame, text="Update webserver folder:").pack(anchor=NW)
    linkEntry = Entry(frame,textvariable=t_update_link)
    linkEntry.pack(pady=5,fill=BOTH)
    linkEntry.focus_set()
    
    button = Button(upd, text='Save', command=lambda: {save_update_settings(t_update_enabled.get(),t_update_link.get()),
                                                                upd.destroy()})
    button.pack(side=BOTTOM,pady=20)
    def cmdbind(*arg):
        save_update_settings(t_update_enabled.get(),t_update_link.get())
        upd.destroy()
    upd.bind('<Return>', cmdbind)
    def close_func(*arg):
        upd.destroy()
    upd.bind('<Escape>', close_func)

def save_download_settings(a):
    global fdl_path
    fdl_path = a
    write_settings('fdl_path',a)

def download_menu():
    global fdl_path, OS
    dwlw = Toplevel()
    set_winicon(dwlw,'icon_grey')
    dwlw.title("Download path")
    dwlw.minsize(500,70)
    dwlw.resizable(FALSE,FALSE)

    t_fdl_path = StringVar()
    t_fdl_path.set(fdl_path)

    frame = Frame(dwlw, height=70,width=460, relief=SUNKEN)
    frame.pack(side=TOP,pady=20)
    frame.pack_propagate(0)
    
    Label(frame, text="Edit download path:").pack(anchor=NW)
    linkEntry = Entry(frame,textvariable=t_fdl_path)
    linkEntry.pack(pady=5,fill=BOTH)
    linkEntry.focus_set()
    def set_default(*arg):
        t_fdl_path.set('downloads/')
    def select_folder(*arg):
        t_fdl_path.set(askdirectory()+'/')
    button = Button(dwlw, text='Default', command=set_default)
    button2 = Button(dwlw, text='Browse', command=select_folder)  
    button3 = Button(dwlw, text='Save', command=lambda: {save_download_settings(t_fdl_path.get()),
                                                                dwlw.destroy()})
    button.pack(side=LEFT,padx=20,pady=20)
    button2.pack(side=LEFT,padx=20,pady=20)
    button3.pack(side=LEFT,padx=20,pady=20)
    def close_func(*arg):
        dwlw.destroy()
    dwlw.bind('<Escape>', close_func)  

def file_manager():
    global OS , s, file_list
    '''
    Here the TreeView widget is configured as a multi-column listbox
    with adjustable column width and column-header-click sorting.
    '''

    try:
        sender_thread_list.append('RQFILES::')
    
        class MultiColumnListbox(object):
            """use a ttk.TreeView as a multicolumn ListBox"""

            def __init__(self,frame,frame2,frame3,Tbox,Scroll):
                self.selected = 'none'
                self.dl_ul_event_counter = 0
                self.windowX = topwin.winfo_width()
                self.windowY = topwin.winfo_height()
                self.frame_xsize = 500
                self.frame_ysize = 400
                self.frame2_xsize = 400
                self.frame2_ysize = 390
                self.frame3_xsize = 400
                self.frame3_ysize = 50
                
                self.tree = None
                self._setup_widgets(frame)
                self._build_tree()
                self.setup_buttons(frame3,Tbox,Scroll)
                topwin.after(10,lambda: self.aftertask2(Tbox,Scroll,frame,frame2,frame3))

            def aftertask2(self,Tbox,Scroll,frame,frame2,frame3,*arg):
                global dl_ul_events
                try:
                    self.selected = self.tree.item(self.tree.selection()[0])
                except Exception as e:
                    e = str(e)
                    self.selected = 'none'
                for x in dl_ul_events[self.dl_ul_event_counter:]:
                    Tbox_insert_lock(Tbox,Scroll,x[0]+' '+x[1]+' '+x[2]+'\n','black')
                    self.dl_ul_event_counter += 1

                ## Automatically readjusts frame sizes when window size is changed
                topwin.after(10,lambda: self.aftertask2(Tbox,Scroll,frame,frame2,frame3))
                self.windowX = topwin.winfo_width()
                self.windowY = topwin.winfo_height()
                self.frame_xsize = self.windowX*0.53
                self.frame_ysize = self.windowY*0.95
                self.frame2_xsize = self.windowX*0.43
                self.frame2_ysize = self.windowY*0.95
                self.frame3_xsize = self.windowX*0.43
                self.frame3_ysize = self.windowY*0.1
                frame.config(width=self.frame_xsize,height=self.frame_ysize)
                frame2.config(width=self.frame2_xsize,height=self.frame2_ysize)
                frame3.config(width=self.frame3_xsize,height=self.frame3_ysize)
                
            def _setup_widgets(self,frame):
                s = """\click on header to sort by that column
        to change width of column drag boundary
                """
                msg = Label(frame,wraplength="4i", justify="left", anchor="n",
                    padding=(10, 2, 10, 6), text=s)
                msg.pack(fill='x')
                container = Frame(frame)
                container.pack(fill='both', expand=True)
                # create a treeview with dual scrollbars
                self.tree = Treeview(frame,columns=multi_header, show="headings")
                vsb = Scrollbar(frame,orient="vertical",
                    command=self.tree.yview)
                hsb = Scrollbar(frame,orient="horizontal",
                    command=self.tree.xview)
                self.tree.configure(yscrollcommand=vsb.set,
                    xscrollcommand=hsb.set)
                self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
                vsb.grid(column=1, row=0, sticky='ns', in_=container)
                hsb.grid(column=0, row=1, sticky='ew', in_=container)
                container.grid_columnconfigure(0, weight=1)
                container.grid_rowconfigure(0, weight=1)
                vsb.focus_set()

            def _build_tree(self):
                for col in multi_header:
                    self.tree.heading(col, text=col.title(),
                        command=lambda c=col: sortby(self.tree, c, 0))
                    # adjust the column's width to the header string
                    self.tree.column(col,
                        width=tkFont.Font().measure(col.title()))
                    
                for item in multi_list:
                    self.tree.insert('', 'end', values=item)
                    # adjust column's width if necessary to fit each value
                    for ix, val in enumerate(item):
                        col_w = tkFont.Font().measure(val)
                        if self.tree.column(multi_header[ix],width=None)<col_w:
                            self.tree.column(multi_header[ix], width=col_w)

            def delete_all_button(self,Tbox,Scroll):
                topwin.lower()
                answer = tkMessageBox.askquestion(title='Delete all files', message='Are you sure?')
                if answer == 'yes':
                    enter_text('command_window','s/clear files')
                    Tbox_insert_lock(Tbox,Scroll,get_cur_time()+'Deleting files'+'\n','red')
                topwin.lift()

            def share_button(self,Tbox,Scroll):
                filename = share_file()
                topwin.lift()
                
            def download_button(self,Tbox,Scroll):
                try:
                    for key in self.selected.iteritems():
                        if key[0] == 'values':
                            selFilename = str(key[1][0])
                    enter_text('command_window','/dl '+selFilename)
                except Exception as e:
                    topwin.lower()
                    e = str(e)
                    if e == "'str' object has no attribute 'iteritems'":
                        e = 'No file selected!'
                    tkMessageBox.showerror(title='Error', message=str(e))
                topwin.lift()

            def setup_buttons(self,frame,Tbox,Scroll):
                button = Button(frame, text='Share', command=lambda :self.share_button(Tbox,Scroll))
                button.pack(anchor=SW,side=LEFT)
                button = Button(frame, text='Download', command=lambda :self.download_button(Tbox,Scroll))
                button.pack(padx=10,anchor=SW,side=LEFT)
                button = Button(frame, text='Clear memory', command=lambda :self.delete_all_button(Tbox,Scroll))
                button.pack(padx=50,anchor=SW,side=LEFT)

        def sortby(tree, col, descending):
            """sort tree contents when a column header is clicked on"""
            # grab values to sort
            data = [(tree.set(child, col), child) \
                for child in tree.get_children('')]
            # if the data to be sorted is numeric change to float
            #data =  change_numeric(data)
            # now sort the data in place
            data.sort(reverse=descending)
            for ix, item in enumerate(data):
                tree.move(item[1], '', ix)
            # switch the heading so it will sort in the opposite direction
            tree.heading(col, command=lambda col=col: sortby(tree, col, \
                int(not descending)))

        def file_list_to_MultiColl(*arg):
            if len(file_list) > 0:
                if file_list == ['EMPTY-LIST']:
                    topwin.lower()
                    tkMessageBox.showerror(title='File list', message='File list is empty')
                    topwin.lift()
                else:
                    for x in file_list:
                        try:
                            multi_list.append([x[0],x[1],x[2],x[3],x[4]])
                        except Exception as e:
                            e = str(e)
                            print e
                            try:
                                multi_list.append([x[0]])
                            except:
                                multi_list.append(['Bad list'])
                msg.destroy()
                frame = Frame(topwin, height=400,width=500)
                frame.pack_propagate(0)
                frame.pack(padx=10,anchor=NE,side=LEFT)
                frame2 = Frame(topwin, height=390,width=400)
                frame2.pack_propagate(0)
                frame2.pack(padx=10,anchor=NE,side=LEFT)
                frame3 = Frame(frame2, height=50,width=400)
                frame3.pack_propagate(0)
                frame3.pack(side=BOTTOM)

                Label(frame2,text= '\n\n').pack(side=TOP,pady=4)
                Scroll = Scrollbar(frame2)
                Tbox = Text(frame2, height=46, width=114,wrap=WORD)
                Scroll.pack(side=RIGHT, fill=Y)
                Tbox.pack(side=BOTTOM,fill=BOTH,expand=1)
##                Tbox.config(background='black',highlightthickness=0,highlightbackground='black',bd=0,)
##                Tbox.tag_configure('greencol', font=('OCR A Extended', 16), foreground='#00FF00')
                Scroll.config(command=Tbox.yview)
                Tbox.config(yscrollcommand=Scroll.set,state="disabled")
    
                listbox = MultiColumnListbox(frame,frame2,frame3,Tbox,Scroll)
            else:
                topwin.after(200,file_list_to_MultiColl)

        topwin = Toplevel()
        topwin.minsize(800,420)
        set_winicon(topwin,'icon_grey')
        topwin.title("File manager")

        multi_list ,file_list  = [],[]
        multi_header = ['Name', 'Size MB','Format','Uploaded','Remaining']
        msg = Message(topwin, width=550,text = "Downloading file list...")
        msg.config(fg='black',font=('Arial', 26))
        msg.pack(anchor=NW)
        topwin.after(200,file_list_to_MultiColl)
        topwin.lift()
        topwin.focus_set()

        def close_func(*arg):
            topwin.destroy()
        topwin.bind('<Escape>', close_func)
    except Exception as e:
        topwin.lower()
        e = str(e)
        if e == "global name 's' is not defined" or e == "'str' object has no attribute 'send'":
            e = 'Not connected!'
        tkMessageBox.showerror(title='Error', message=str(e))
        topwin.lift()

def configure_border_size(widget,size):
    try:
        widget.config(bd=size)
    except:
        print 'Can not change '+str(widget)+' border'
    try:
        widget.config(highlightthickness=0)
    except:
        print 'Can not change '+str(widget)+' highlightthickness'
    

def change_other_settings(a,c,e,f,g,h,i,j,k,l,m,n):
    global X_size,Y_size ,autojoin, leave_join, nadd_spaces, show_ttime, show_users, autoauth
    global User_area, S2, T, S, E, s, username, write_log, show_logtime, toolbar, scroll_class_u
    global E_borderlen, T_borderlen, S_borderlen, show_toolbar, use_alternative_tlb
    widliste = (T,User_area, S, S2)
    autojoin = a
    leave_join = c
    nadd_spaces = e
    autoauth = h
    write_log = i
    show_logtime = j
    scroll_class_u = k
    # Configures border length for E, T, S
    try:
        for x in l:
            x = int(x)
        E_borderlen, T_borderlen, S_borderlen = l[0],l[1],l[2]
        configure_border_size(E,E_borderlen)
        configure_border_size(T,T_borderlen)
        try:
            configure_border_size(User_area,T_borderlen)
            configure_border_size(S2,S_borderlen)
        except:
            pass
        configure_border_size(S,S_borderlen)
    except:
        T_ins_warning(T,S,'Not a number')

    # Removes all root window widgets and adds new
    if show_users is not g or show_toolbar is not m or use_alternative_tlb is not n:
        if show_users == 1:
            User_area.destroy()
        if show_toolbar == 1:
            toolbar.destroy()
        show_users = g
        show_toolbar = m
        use_alternative_tlb = n
        T.destroy()
        E.destroy()
        S.destroy()
        S2.destroy()
        create_widgets()
        user_area_insert()
        if show_toolbar == 0:
            T_ins_warning(T,S,'Toolbar can be restored by typing /toolbar')
        
    show_ttime = f
    write_settings('show_ttime',f)
    write_settings('autojoin',a)
    write_settings('leave_join',c)
    write_settings('nadd_spaces',e)
    write_settings('show_users',g)
    write_settings('autoauth',h)
    write_settings('chlog',i)
    write_settings('show_logtime',j)
    write_settings('scrollbar_class',k)
    write_settings('E_borderlen',E_borderlen)
    write_settings('T_borderlen',T_borderlen)
    write_settings('S_borderlen',S_borderlen)
    write_settings('show_toolbar',show_toolbar)
    write_settings('use_alternative_tlb',use_alternative_tlb)
##    root.geometry('%sx%s' % (X_size,Y_size))
    
def other_menu():
    global autojoin, leave_join, nadd_spaces, show_ttime, show_users, autoauth, write_log, show_logtime
    global scroll_class_u, E_borderlen, T_borderlen, S_borderlen, show_toolbar, use_alternative_tlb
    sm = Toplevel()
    set_winicon(sm,'icon_grey')
    sm.title("Other settings")
    sm.minsize(500,300)
    sm.resizable(FALSE,FALSE)
    frame = Frame(sm, height=220,width=210, relief=SUNKEN)
    frame.pack_propagate(0)
    frame.pack(anchor=NE,side=LEFT,padx=10,pady=10)
    frame2 = Frame(sm, height=220,width=210, relief=SUNKEN)
    frame2.pack_propagate(0)
    frame2.pack(anchor=NE,side=LEFT,padx=10,pady=10)
    frame3 = Frame(sm, height=40,width=500, relief=SUNKEN)
    frame3.pack_propagate(0)
    frame3.place(x=180,y=200)
    frame4 = Frame(sm, height=220,width=210, relief=SUNKEN)
    frame4.pack_propagate(0)
    frame4.pack(anchor=NE,side=LEFT,padx=10,pady=10)
    
    t_leave_join = IntVar()
    t_autoauth = IntVar()
    t_autojoin = IntVar()
    t_write_log = IntVar()
    t_lenghten = IntVar()
    t_show_users = IntVar()
    t_box_time = IntVar()
    t_log_time = IntVar()
    t_E_borderlen, t_T_borderlen, t_S_borderlen = StringVar(),StringVar(),StringVar()
    t_scroll_class_u = StringVar()
    t_show_toolbar = IntVar()
    t_use_alternative_tlb = IntVar()
    t_leave_join.set(leave_join)
    t_autoauth.set(autoauth)
    t_autojoin.set(autojoin)
    t_write_log.set(write_log)
    t_lenghten.set(nadd_spaces)
    t_show_users.set(show_users)
    t_box_time.set(show_ttime)
    t_log_time.set(show_logtime)
    t_scroll_class_u.set(scroll_class_u)
    t_E_borderlen.set(E_borderlen)
    t_T_borderlen.set(T_borderlen)
    t_S_borderlen.set(S_borderlen)
    t_show_toolbar.set(show_toolbar)
    t_use_alternative_tlb.set(use_alternative_tlb)
    
    Checkbutton(frame, text="Show leave and join", variable=t_leave_join).pack(anchor=NW)
    Checkbutton(frame, text="Enable autoauthentication", variable=t_autoauth).pack(anchor=NW)
    Checkbutton(frame, text="Enable autojoin", variable=t_autojoin).pack(anchor=NW)
    Label(frame, text="\nLog file time:",justify = LEFT).pack(anchor=NW)
    Radiobutton(frame,text="Show full",variable=t_log_time,value=3).pack(anchor=NW)
    Radiobutton(frame,text="Without seconds",variable=t_log_time,value=2).pack(anchor=NW)
    Radiobutton(frame,text="Hide",variable=t_log_time,value=1).pack(anchor=NW)

    Checkbutton(frame2, text="Enable log writing", variable=t_write_log).pack(anchor=NW)
    Checkbutton(frame2, text="Force 19chr length usernames", variable=t_lenghten).pack(anchor=NW)
    Label(frame2, text="\n\nText box time:",justify = LEFT).pack(anchor=NW)
    Radiobutton(frame2,text="Show full",variable=t_box_time,value=3).pack(anchor=NW)
    Radiobutton(frame2,text="Without seconds",variable=t_box_time,value=2).pack(anchor=NW)
    Radiobutton(frame2,text="Hide",variable=t_box_time,value=1).pack(anchor=NW)

    Checkbutton(frame4, text="Show user box", variable=t_show_users).pack(anchor=NW)
    Checkbutton(frame4, text="Show toolbar", variable=t_show_toolbar).pack(anchor=NW)
    Checkbutton(frame4, text="Use alternative toolbar", variable=t_use_alternative_tlb).pack(anchor=NW)
    Label(frame4, text="Scrollbar:",justify = LEFT).pack(anchor=NW)
    Combobox(frame4, textvariable=t_scroll_class_u,values=['default','system','alternative']).pack(anchor=NW)

    Label(frame4, text="Entry widget border:",justify = LEFT).pack(anchor=NW)
    E_border = Entry(frame4,textvariable=t_E_borderlen).pack(anchor=NW)
    Label(frame4, text="Text widget border:",justify = LEFT).pack(anchor=NW)
    T_border = Entry(frame4,textvariable=t_T_borderlen).pack(anchor=NW)
    Label(frame4, text="Scrollbar widget border:",justify = LEFT).pack(anchor=NW)
    S_border = Entry(frame4,textvariable=t_S_borderlen).pack(anchor=NW)

    button = Button(frame3, text='Save', command=lambda: {change_other_settings(t_autojoin.get(),
                    t_leave_join.get(),t_lenghten.get(),t_box_time.get(),t_show_users.get(),
                    t_autoauth.get(),t_write_log.get(),t_log_time.get(),t_scroll_class_u.get(),
                    (t_E_borderlen.get(),t_T_borderlen.get(),t_S_borderlen.get()),
                     t_show_toolbar.get(),t_use_alternative_tlb.get()),
                    sm.destroy()})
    button.pack(side=LEFT)
    def close_func(*arg):
        sm.destroy()
    sm.bind('<Escape>', close_func)

    
def find_2name(text,name,uname,beeped):
    global username
    uname = remove_spaces(uname)
    if uname == username:
        return False, beeped
    text = text.lower()
    name = name.lower()
    text = text[:-1]
    if name == text or '@'+name == text or '@@'+name == text:
        if sound_settings[2] == 1 and beeped == False:
            play_sound('beep1.wav',False)
            beeped = True
        return True, beeped
    else:
        return False, beeped

def reset_entry(var):
    textt.set('')

def reset_textbox():
    T.config(yscrollcommand=S.set,state="normal")
    T.delete(1.0,END)
    T.config(yscrollcommand=S.set,state="disabled")

def string_to_list(data):
##    print data
    temp_list,strlist = [], []
    while True:
        ## Separates user strings and puts them in a temp. list
        begn = data.find('[[')
        end = data.find(']]')
        if begn is -1 or end is -1:
            break
        temp_list.append(data[begn+2:end+1])
        data = data[end+2:]
    cnt = 0
    ## Creates a list for each user
    for x in temp_list:
        strlist.append([])
    ## Separates individual values in each users list
    for x in temp_list:
        while True:
            begn = x.find('[')+1
            end = x.find(']')
            if begn is -1 or end is -1:
                break
            strlist[cnt].append(x[begn:end])
            x = x[end+1:]
        cnt+=1
    return strlist

def organise_file_list(data):
    string_to_list(file_list)

def organise_USRLIST(data):
    global USRLIST, show_users
    USRLIST, temp_list, off_usr, on_usr = [], [], [], []
    while True:
        ## Separates user strings and puts them in a temp. list
        begn = data.find('[[')
        end = data.find(']]')
        if begn is -1 or end is -1:
            break
        temp_list.append(data[begn+2:end+1])
        data = data[end+2:]
    cnt = 0
    ## Creates a list for each user
    for x in temp_list:
        USRLIST.append([])
    ## Separates individual values in each users list
    for x in temp_list:
        while True:
            begn = x.find('[')+1
            end = x.find(']')
            if begn is -1 or end is -1:
                break
            USRLIST[cnt].append(x[begn:end])
            x = x[end+1:]
        cnt+=1
    cnt = 0
    ## Separates user count from user list
    for x in USRLIST:
        if x[0][:6] == 'Users:' and x[1] == '':
            usercount = x
            USRLIST.pop(cnt)
            break
        cnt+=1
    ## Separates online and offline users and sorts them
    for x in USRLIST:
        if x[1] == 'Offline':
            off_usr.append(x)
        else:
            on_usr.append(x)
    off_usr.sort()  
    on_usr.sort()
    ## Inserts Online and usercount at the beginning, and inserts Offline after the last online user
##    on_usr.insert(0,usercount)
    on_usr.insert(0,['Online'+str(usercount[0][6:]),'olfo-','1','1'])
    off_usr.insert(0,['Offline '+str(len(off_usr)),'olfo-','1','1'])
    off_usr.insert(0,[])
    ## Combines online and offline users into one list for the user_area_insert() function
    USRLIST = []
    for x in on_usr:
        USRLIST.append(x)
    for x in off_usr:
        USRLIST.append(x)

    if show_users == 1:
        user_area_insert()

def user_area_insert():
    global USRLIST
    User_area.config(state="normal")
    User_area.delete(1.0,END)
    for x in USRLIST:
        try:
            if x == []:
                User_area.insert(END,'\n')
            else:
                usercol = get_user_color(x[2],x[0],False)
                ## Offline color
                if x[1] == 'Offline':
                    User_area.insert(END, x[0]+'\n','offcol')
                ## Online and Offline
                elif x[1] == 'olfo-':
                    User_area.insert(END, x[0]+'\n','olfo-backgr')
                ## AFK color
                elif x[3] == '0':
                    User_area.insert(END, x[0]+'\n','greycol')
                ## Normal user color
                else:
                    User_area.insert(END, x[0]+'\n',usercol)
        except:
            User_area.insert(END, x[0]+'\n','blackcol')
    User_area.config(state="disabled")

def add_spaces(name):
    for x in name:
        while len(name) < 15:
            name = ' '+name
    return name

def remove_spaces(name):
    for x in name:
        if x is ' ':
            name = name[1:]
        else:
            break
    return name

def get_user_color(col,name,add_zero):
    global nadd_spaces
    if nadd_spaces is 1:
        name = add_spaces(name)
    elif nadd_spaces is 0:
        name = remove_spaces(name)
    if add_zero == True:
        addz = '0'
    else:
        addz = ''
    if col == '-1':
        return 'redcol',name
    elif col == addz+'0':
        return 'greycol',name
    elif col == addz+'1':
        return 'blackcol',name
    elif col == addz+'2':
        return 'blackcol',name
    elif col == addz+'3':
        return 'pinkcol',name
    elif col == addz+'4':
        return 'orangecol',name
    elif col == addz+'5':
        return 'purplecol',name
    elif col == addz+'6':
        return 'purplecol',name
    elif col == addz+'7':
        return 'purplecol',name
    elif col == addz+'8':
        return 'purplecol', name
    elif col == addz+'9':
        return 'purplecol', name
    return '0','0'

def find_link(data):
    global TLDS
    data = data + ' '
    ## Looks for http, https, www at the beginning of string
    begn = data.find('http://')
    linktext = ''
    data = data[:-1]
    if len(data) > 5:
        if begn is not -1:
            while True:
                if data[begn] is not ' ':
                    linktext = linktext+data[begn]
                    begn+=1
                else:
                    return linktext
        begn = data.find('https://')        
        if begn is not -1:
            while True:
                if data[begn] is not ' ':
                    linktext = linktext+data[begn]
                    begn+=1
                else:
                    return linktext
        begn = data.find('www.')        
        if begn is not -1 and len(data) > 4:
            return data
        ## Compares all top domains when previous are not found
        b = data.find('.')
        if b != -1:
            for x in TLDS:
                b = data.find('.'+x)
##                print x, data
                if b != -1:
                    x = x.rstrip()
                    data = data.rstrip()
                    if data == data[:-len(x)]+x:
                        return data
        else:
            return 'False'
    return 'False'

def copy_text(*arg):
    try:
        try:
            T.config(state="normal")
            T.clipboard_clear()
            text = T.get("sel.first", "sel.last")
            T.clipboard_append(text)
        except:
            try:
                User_area.config(state="normal")
                User_area.clipboard_clear()
                text = User_area.get("sel.first", "sel.last")
                User_area.clipboard_append(text)
            except:
                E.clipboard_clear()
                text = E.selection_get()
                E.clipboard_append(text)
    except:
        pass
    T.config(state="disabled")
    User_area.config(state="disabled")

def entry_paste(*arg):
    try:
        text = root.selection_get(selection='CLIPBOARD')
        E.insert('insert', text)
    except:
        print 'Nothing in clipboard'

def autocomplete_name(*arg):
    is_private = False
    commandli = ('/help','/users','/log','/afk','/reg','/auth','/clear','/share','/file','/files','/file_list',
                '/join','/ljoin','/leave','/changelog','/about','/quit','/exit','/datal', '/toolbar')
    try:
    ## Finds the last word in entry widget
        text = textt.get()
        text = text[::-1]
        cnt = 0
        for x in text:
            if x == ' ':
                text = text[:cnt]
                break
            cnt += 1
        text = text[::-1]
        ## Selects command loop or user name loop
        if text[0] == '/':
            ## Finds the name in commandli
            for x in commandli:
                b = x.find(text)
                if b == 0:
                    ## Completes it and moves the cursor to the end
                    textt.set(textt.get()+x[len(text):])
                    lentext = textt.get()
                    E.icursor(len(lentext))
                    break
        elif len(USRLIST) > 0:
            ## Removes "@"
            if text[0] == '@':
                text = text[1:]
            if text[0] == '@':
                text = text[1:]
                is_private = True
            ## Finds the name in USRLIST
            if text != '' and text != ' ':
                for x in USRLIST:
                    try:
                        if x[1] is not 'olfo-':
                            b = x[0].find(text)
                            if b == 0 and x[0] != text:
                                ## Completes it and moves the cursor to the end
                                    ## Adds "]" instead of space, if message is private
                                if is_private == True:
                                    textt.set(textt.get()+x[0][len(text):]+']')
                                    lentext = textt.get()
                                    E.icursor(len(lentext))
                                else:
                                    textt.set(textt.get()+x[0][len(text):]+' ')
                                    lentext = textt.get()
                                    E.icursor(len(lentext))
                                break

                    except:
                        pass
    except:
        pass
    ## Stops tkinter from tabbing
    return "break"

def entrym_FORWARD(*arg):
    global entry_message_arch
    if len(entry_mlist) > 0:
        if entry_message_arch == -1:
            textt.set('')
            entry_message_arch += 1
        elif entry_message_arch < 0:
            entry_message_arch += 1
            textt.set(entry_mlist[entry_message_arch])
    
def entrym_BACK(*arg):
    global entry_message_arch
    entrilen = len(entry_mlist)
    if entrilen > 0:
        if entry_message_arch*-1 < entrilen:
            entry_message_arch -= 1
            textt.set(entry_mlist[entry_message_arch])

def search_text_dialog(widget):
    widget.tag_configure("search", background="green")
    def color_tagger_thread(name):
        start = 1.0
        try:
            while start != widget.index(CURRENT):
                pos = widget.search(name, start, stopindex=END)
                b = pos.find('.')
                pos2 = pos[b+1:]
                pos2 = pos[:b]+'.'+str(int(pos2)+int(countVar.get()))
                if not pos:
                    break
                widget.tag_add("search", pos, pos2)
                start = pos + "+1c"
        except:
            pass
    def text_finder(*arg):
        widget.tag_remove("sel",1.0,END)
        widget.tag_remove("search",1.0,END)
        ftext = t_findtext.get()
        pos = widget.search(ftext, start.get(), count=countVar)
        widget.see(pos)
        b = pos.find('.')
        pos2 = pos[b+1:]
        pos2 = pos[:b]+'.'+str(int(pos2)+int(countVar.get()))
##        widget.tag_add("search", pos, pos2)
        widget.tag_add(SEL, pos, pos2)
        widget.tag_raise("sel")
        start.set(pos2)
        Thread(target=color_tagger_thread,args=(ftext,)).start()
    topwin = Toplevel()
    set_winicon(topwin,'icon_grey')
    topwin.title("Search dialog")
    topwin.minsize(600,120)
    topwin.resizable(FALSE,FALSE)

    frame4 = Frame(topwin, height=120,width=120, relief=SUNKEN,bg='')
    frame4.pack_propagate(0)
    frame4.pack(side=RIGHT)
    frame1 = Frame(topwin, height=40,width=480, relief=SUNKEN,bg='')
    frame1.pack_propagate(0)
    frame1.pack(side=TOP)
    frame2 = Frame(topwin, height=40,width=480, relief=SUNKEN,bg='')
    frame2.pack_propagate(0)
    frame2.pack(side=TOP)
    frame3 = Frame(topwin, height=40,width=480, relief=SUNKEN,bg='')
    frame3.pack_propagate(0)
    frame3.pack(side=TOP)

    start = StringVar()
    countVar = StringVar()
    
    t_match_case = IntVar()
    t_wrap_around = IntVar()
    t_findtext = StringVar()
    t_search_direction = IntVar()
    t_findtext.set('')
    t_match_case.set(0)
    t_wrap_around.set(1)
    t_search_direction.set(1)
    
    start.set("1.0")
    Label(frame1, text="Find text: ").pack(side=LEFT)
    tEntry = Entry(frame1,textvariable=t_findtext,width=50)
    tEntry.pack(side=LEFT)
    tEntry.focus_set()

    Label(frame2, text="Options: ").pack(side=LEFT)
    Checkbutton(frame2, text="Match case", variable=t_match_case).pack(side=LEFT,padx=5)
    Checkbutton(frame2, text="Wrap around", variable=t_wrap_around).pack(side=LEFT,padx=5)

    Label(frame3, text="Direction:   ").pack(side=LEFT)
    search_UP = Radiobutton(frame3, text='IP', variable=t_search_direction, value=1)
    search_DOWN = Radiobutton(frame3, text='Down', variable=t_search_direction, value=0)
    search_UP.pack(side=LEFT)
    search_DOWN.pack(side=LEFT)

    def close_func(*arg):
        widget.tag_remove("search",1.0,END)
        topwin.destroy()
    button = Button(frame4, text='Find', command=text_finder).pack(side=TOP,pady=15, padx=10)
    button = Button(frame4, text='Close', command=close_func).pack(side=TOP, padx=10)
    
    topwin.protocol('WM_DELETE_WINDOW', close_func)
    topwin.bind('<Escape>', close_func)
    topwin.bind('<Return>', text_finder)
    
def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''
    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')
        def rOpenBrowser(e):
            open_in_browser_btn()
        def rCommandWin(e):
            command_window()
        def rClick_Clear(e):
            textt.set('')
        def rClick_Paste(e):
            entry_paste()

        e.widget.focus()

        nclst=[(' Command window', lambda e=e: rCommandWin(e)),
               (' Clear entry', lambda e=e: rClick_Clear(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        print ' - rClick menu, something wrong'
        pass
    focus_hover_widget()
    return "break"

def rClickbinder(r):
    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except TclError:
        print ' - rClickbinder, something wrong'
        passwd

def motion(event):
    global m_x,m_y
    m_x, m_y = event.x, event.y

def file_recvd(conn):
    conn.settimeout(10)
    try:
        data = conn.recv(8192)
    except Exception as e:
        e = str(e)
        scroller = S.get()
        T_ins_warning(T,S,e)
        if scroller[1] == 1.0:  
            T.yview(END)
        if e == 'timed out':
            return 'TIMEOUT::'
    return data

def TCPconnect(ip,port):
    contcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    contcp.connect((ip, port))
    return contcp   

def fldownloader_thread(name):
    global connected_server, fdl_path, dl_ul_events
    print 'File download thread started - ',name
    dl_ul_events.append([get_cur_time(),'Downloading',name])
    buflen, flstring = 0, ''
    scroller = S.get()
    try:
        os.makedirs('downloads')
    except:
        pass
    tim = time()
    Tbox_insert_lock(T,S,get_cur_time()+' Downloading "'+name+'"\n','blackcol')
    if scroller[1] == 1.0:  
            T.yview(END)
    sf = TCPconnect(connected_server,44672)
    
    data = file_recvd(sf)
    sleep(0.05)
    if data == 'READY::':
        sf.send('DOWNLOAD::'+name)
    data = file_recvd(sf)
    sleep(0.05)
    sf.send('SENDR::')
    data = file_recvd(sf)
    if data != 'WrongName::':
        while True:
            flstring= flstring + data
            data = file_recvd(sf)
            if data == 'ENDING::' or data == 'TIMEOUT::':
                break
            elif not data:
                break
        try:
            fh = open(fdl_path+name, 'ab')
            fh.write(flstring)
        except:
            T_ins_warning(T,S,'Download path is wrong, saving in downloads/')
            fh = open('downloads/'+name, 'ab')
            fh.write(flstring)
        fh.close()
        tim2 = round(time() - tim,2)
        buflen = len(flstring)
        Tbox_insert_lock(T,S,get_cur_time()+' File downloaded in '+str(tim2)+'sec. - '+str(round(buflen/tim2/1000/1024,2))+' MB/s\n','blackcol')
    else:
        T_ins_warning(T,S,'File does not exist')
        
    try:
        sf.close()
    except:
        pass
    if scroller[1] == 1.0:  
            T.yview(END)
    print 'File download thread stopped - ',name
    dl_ul_events.append([get_cur_time(),'Downloaded',name])
        

def share_file_thread(path,name):
    global connected_server, username, action_time, passwd, dl_ul_events
    print 'File share thread started - ',name
    dl_ul_events.append([get_cur_time(),'Uploading',name])
    scroller = S.get()
    registered = False
    try:
        sf = TCPconnect(connected_server,44672)
        state = 'connected'
        tim = time()
        Tbox_insert_lock(T,S,get_cur_time()+' Sending "'+name+'"\n','blackcol')
        if scroller[1] == 1.0:  
                T.yview(END)

        data = file_recvd(sf)
        sleep(0.05)
        if data == 'READY::':
            sf.send('UPLOAD::')
        data = file_recvd(sf)
        sleep(0.05)
        if data == 'READY::':
            if passwd is '':
                registered = False
            else:
                registered = True
                sf.send('USRINFO::'+username+']'+passwd)
        data = file_recvd(sf)
        sleep(0.05)
        sf.send('SENDFIL::'+name)
        buflen = 0
        if registered == True:
            data = file_recvd(sf)
            sleep(0.05)
            if data == 'SENDR::':
                with open(path, "rb") as fi:
                    buf = fi.read(8192)
                    while (buf):
                        sf.send(buf)
                        buf = fi.read(8192)
                        buflen += 1
                tim2 = round(time() - tim,2)
                Tbox_insert_lock(T,S,get_cur_time()+' File sent in '+str(tim2)+'sec. - '+str(round(buflen/tim2*8/1024,2))+' MB/s\n','blackcol')
                sleep(1)
                sf.send('ENDING::')
                print 'File share thread stopped - ',name
                dl_ul_events.append([get_cur_time(),'Uploaded',name])
    except Exception as e:
        e = str(e)
        T_ins_warning(T,S,e)
    if scroller[1] == 1.0:  
            T.yview(END)
    try:
        sf.close
    except:
        pass

def share_file():
    path= askopenfilename()
    name = str(path)
    while True:
        b = name.find('/')
        if b is not -1:
            name = name[b+1:]
        c = name.find('\\')
        if c is not -1:
            name = name[c+1:]
        elif b is -1 and c is -1:
            break
    if len(name) > 0:
        Thread(target=share_file_thread,args=(path,name,)).start()
        return name

def write_logfile(dirpath,filename,text):
    b = filename.find('.txt')
    if b is -1:
        filename = filename+'.txt'
    try:
        fh = open(dirpath+filename, 'a')
        fh.write(text)
        fh.close()
    except:
        try:
            print 'Wrong path, saving in /log'
            os.makedirs('log')
        except:
            pass
        fh = open('log/'+filename, 'a')
        fh.write(text)
        fh.close()

def load_lib_scripts(root):
    global data_list,thread_message_list,dl_ul_events,entry_mlist
    if os.path.exists('lib/loadscripts.ini'):
        scriptlist = readf('lib/loadscripts.ini')
        for module in scriptlist:
            module = module.rstrip()
            try:
                # because we want to import using a variable, do it this way
                module_obj = __import__(module)
                # create a global object containging our module
                globals()[module] = module_obj
                globals()[module].main(data_list,thread_message_list,dl_ul_events,entry_mlist)
                print 'Loaded module: '+module
##            except ImportError:
##                sys.stderr.write("ERROR: missing python module: " + module + "\n")
##                sys.exit(1)
            except Exception as e:
                e = str(e)
                T_ins_warning(T, S, 'ERROR: loading '+module+'\n')
                T_ins_warning(T, S, e)

def Changelog():
    global text_font, window_sizes
    def closethis():
        write_settings('win_changelog_x',topwin.winfo_width())
        write_settings('win_changelog_y',topwin.winfo_height())
        window_sizes[0][0], window_sizes[0][1] = str(topwin.winfo_width()),str(topwin.winfo_height())
        topwin.destroy()
    topwin = Toplevel()
    set_winicon(topwin,'icon_grey')
    topwin.title("Changelog")
    topwin.minsize(750,550)
    try:
        if window_sizes[0][0] > 500 and window_sizes[0][1] > 300:
            win_sizeX = ''.join(window_sizes[0][0])
            win_sizeY = ''.join(window_sizes[0][1])
            topwin.geometry(win_sizeX+'x'+win_sizeY)
    except Exception as e:
        e = str(e)
        T_ins_warning(T, S, e)
    
    Tbox = Text(topwin, height=12, width=50,wrap=WORD)
    Tbox.tag_configure('blackcol', font=text_font, foreground='black')
    Tbox.tag_configure('CL-bg', font=text_font, background='#80ccff',foreground='black')
    Tbox.tag_configure('SE-bg', font=text_font, background='#66cc66',foreground='black')
    Tbox.tag_configure('UP-bg', font=text_font, background='#FF7373',foreground='black')
    Tbox.tag_configure('dark-bg', font=text_font, background='#cccccc',foreground='black')
    Tbox.tag_configure('light-bg', font=text_font, background='#f3f3f3',foreground='black')
    Tbox.configure(inactiveselectbackground="#6B9EB7", selectbackground="#4283A4")
    Tbox.tag_raise("sel")
    S1 = Scrollbar(topwin)
    Tbox.focus_set()
    Tbox.config(yscrollcommand=S1.set,state="normal")
    S1.config(command=Tbox.yview)

    bb1 = Button(topwin, text='Close', command=closethis)
    bb1.pack(side=BOTTOM,pady=10)
    S1.pack(side=RIGHT, fill=Y)
    Tbox.pack(side=BOTTOM,fill=BOTH,expand=1)
    
    changelogfile = readf('changelog.txt')
    for x in changelogfile:
        if x[:6] == '## Cli':
            Tbox.insert(END, x+'\n','CL-bg')
        elif x[:6] == '## Ser':
            Tbox.insert(END, x+'\n','SE-bg')
        elif x[:6] == '## Upd':
            Tbox.insert(END, x+'\n','UP-bg')
        elif x[:3] == '###':
            Tbox.insert(END, x+'\n','light-bg')
        else:
            Tbox.insert(END, x+'\n','blackcol')
    Tbox.config(yscrollcommand=S1.set,state="normal")
    topwin.protocol('WM_DELETE_WINDOW', closethis)
    def widget_sel_all(*arg):
        Tbox.tag_add(SEL, "1.0", END)
        Tbox.mark_set(INSERT, "1.0")
        Tbox.see(INSERT)
    def close_func(*arg):
        topwin.destroy()
    topwin.bind('<Escape>', close_func)
    topwin.bind("<Control-a>", widget_sel_all)
    Tbox.bind('<Control-f>',lambda x: search_text_dialog(Tbox))

class msg_binder:
    def __init__(self,_frame,_text,_font,l_width,_color,_bgcolor,function,function_exc,gui_add,*arg):
        self.msg = Message(_frame, text = _text,width=l_width)
        self.msg.config(bg=_bgcolor,fg=_color,width=l_width,font=_font)
        if gui_add == 'pack':
            self.msg.pack(anchor=NW)
        elif gui_add == 'place':
            self.msg.place(x=arg[0][0],y=arg[0][1])
        self.function = function
        self.function_exc = function_exc
        self.msg.bind("<Enter>", self._enter)
        self.msg.bind("<Leave>", self._leave)
        self.msg.bind("<Button-1>", self._click)

    def _enter(self, event):
        self.msg.config(cursor="hand2")

    def _leave(self, event):
        self.msg.config(cursor="")

    def _click(self, event):
        if self.function == 'func':
            self.function_exc()
        elif self.function == 'link' and self.function_exc != 'none':
            open_address_in_webbrowser(self.function_exc)

def About():
    global ver, updater_ver
                
    winwi = 650
    aboutwin = Toplevel()
    aboutwin.minsize(winwi,300)
    aboutwin.resizable(FALSE,FALSE)
    set_winicon(aboutwin,'icon_grey')

    font_progname = ('Arial', 26,'bold')
    font_text = ('Arial', 14,'bold')
    font_text_small = ('Arial', 12)
    font_text_smaller = ('Arial', 10)
    backg1 = '#F9F8F6'
    backg2 = '#EFEEEC'
    text_color1 = '#595856'
    text_blue = '#1569C7'
    l_width = 350
    
    aboutwin.title("About iSPTC")
    aboutwin.config()
    frame = Frame(aboutwin, height=240,width=winwi*0.4, relief=SUNKEN,bg=backg1)
    frame.pack_propagate(0)
    frame.grid(column=1,row=1)
    frame2 = Frame(aboutwin, height=240,width=winwi*0.6, relief=SUNKEN,bg=backg1)
    frame2.pack_propagate(0)
    frame2.grid(column=2,row=1)
    frame3 = Frame(aboutwin, height=60,width=winwi, relief=SUNKEN,bg=backg2)
    frame3.pack_propagate(0)
    frame3.place(x=0,y=240)

    ## Frame 1 - Picture
    sep = Message(frame, text = " ")
    sep.config(background=backg1,font=('Arial', 12))
    sep.pack(side=TOP)
    img = Pillow_image.open("load/icon3.png")
    img2 = ImageTk.PhotoImage(img)
    label = tkLabel(frame,image=img2,bg=backg1)
    label.image = img2
    label.pack()

    ## Frame 2 - Title and description
    sep = Message(frame2, text = " ")
    sep.config(background=backg1,font=('Arial', 10))
    sep.pack(side=TOP)
    
##    Text = ("iSPTC ver%s" % (ver))
    Text = ("iSPTC")
    msg = Message(frame2, text = Text,width=l_width)
    msg.config(bg=backg1,fg=text_color1,width=l_width,font=font_progname)
    msg.pack(anchor=NW)

    Text = ("inSecure Plain Text Chat")
    msg = Message(frame2, text = Text,width=l_width)
    msg.config(bg=backg1,fg=text_color1,width=l_width,font=font_text)
    msg.pack(anchor=NW)

    Text = ("Client ver: "+ver)
    msg = Message(frame2, text = Text,width=l_width)
    msg.config(bg=backg1,fg=text_color1,width=l_width,font=font_text_small)
    msg.pack(anchor=NW)
    Text = ("Updater ver: "+updater_ver)
    msg = Message(frame2, text = Text,width=l_width)
    msg.config(bg=backg1,fg=text_color1,width=l_width,font=font_text_small)
    msg.pack(anchor=NW)

    msg = Message(frame2, text = " ",width=l_width)
    msg.config(background=backg1,width=l_width,font=('Arial', 20))
    msg.pack(anchor=NW)

    
    git_label = msg_binder(frame2,"Github page: github.com/Bakterija",font_text_smaller,l_width,
                          text_color1,backg1,'link','https://github.com/Bakterija','pack')
##    li = msg_binder(frame3,"Li",font_text_smaller,l_width,
##                          text_blue,backg2,'func',lifunc,'place',[260,10])
    
    def close_func(*arg):
        aboutwin.destroy()
    aboutwin.bind('<Escape>', close_func)

def set_activated_T(*arg):
    global activated_widget
    activated_widget = ('T',T)
def set_activated_U(*arg):
    global activated_widget
    activated_widget = ('U',User_area)
def set_activated_E(*arg):
    global activated_widget
    activated_widget = ('E',E)
def set_activated_S(*arg):
    global activated_widget
    activated_widget = ('S',S)
def set_activated_S2(*arg):
    global activated_widget
    activated_widget = ('S2',S2)

if __name__ == '__main__':
    global sys_path, OS
    sys_path = os.getcwd()
    OS = platform.system()
    print 'Path ',sys_path

    ## Top domain list
    sys.path.insert(0, './lib')
    from top_domains import TLDS
    for x in TLDS:
        x = x.decode('utf-8')

    if OS is 'Windows':
        import winsound
        
    ## Loading from settings file
    ### 0all_sound, 1entry, 2username mention in textbox
    sound_settings = [1,1,1]
    task_loop_interval = int(read_settings('chat_interval=',500))
    sound_settings[0] = int(read_settings('enable_sound=',1))
    sound_settings[1] = int(read_settings('entry_enabled=',0))
    sound_settings[2] = int(read_settings('user_textbox=',1))
    dsound_interval=float(read_settings('sound_interval=',2.0))
    leave_join = int(read_settings('leave_join=',1))
    show_ttime= int(read_settings('show_ttime=',2))
    nadd_spaces= int(read_settings('nadd_spaces=',1))
    username = str(read_settings('username=','User'+str(randrange(1,999,1))))
    if len(username) < 1:
        username = 'User'+str(randrange(1,999,1))
    autojoin = int(read_settings('autojoin=',0))
    show_users = int(read_settings('show_users=',1))
    X_size = int(read_settings('X_size=',800))
    Y_size = int(read_settings('Y_size=',600))
    font1 = str(read_settings('font1=','Arial'))
    font2 = int(read_settings('font2=',10))
    font3 = str(read_settings('font3=','normal'))
    text_font = (font1,font2,font3)
    passwd = str(read_settings('usrauth=',''))
    autoauth = int(read_settings('autoauth=',1))
    offline_msg = int(read_settings('offline_msg=',1))
    update_enabled = int(read_settings('update_enabled=',0))
    update_link = str(read_settings('update_link=',''))
    fdl_path = str(read_settings('fdl_path=','downloads/'))
    write_log = int(read_settings('chlog=',1))
    usra_len = int(read_settings('usra_len=',20))
    day_number_old = str(read_settings('day_number=','0'))
    window_sizes = []
    window_sizes.append([[str(read_settings('win_changelog_x=','700'))],[str(read_settings('win_changelog_y=','500'))]])
    updater_ver = str(read_settings('updater_ver=','1'))
    show_logtime = int(read_settings('show_logtime=',2))
    saved_theme = str(read_settings('theme=','Default'))
    scroll_class_u = str(read_settings('scrollbar_class=','system'))
    if scroll_class_u == 'system':
        from ttk import Scrollbar
    E_borderlen = int(read_settings('E_borderlen=',1))
    T_borderlen = int(read_settings('T_borderlen=',1))
    S_borderlen = int(read_settings('S_borderlen=',1))
    show_toolbar = int(read_settings('show_toolbar=',1))
    use_alternative_tlb = int(read_settings('use_alternative_tlb=',0))
    default_colors_list = [['chat','Warnings','redcol','red','white'],
                        ['chat','Server msg','bluecol','blue','white'],
                        ['chat','Server warnings','browncol','#862d2d','white'],
                        ['chat','Username','greencol','#009900','white'],
                        ['chat','Normal msg','blackcol','black','white'],
                        ['chat','User lvl3','pinkcol','pink','white'],
                        ['chat','User lvl4','orangecol','#e65b00','white'],
                        ['chat','High lvl msg','purplecol','purple','white'],
                        ['chat','AFK','greycol','#7F7F7F','white'],
                        ['chat','Offline','offcol','#7F7F7F','white'],
                        ['chat','Links','blue_link','blue','white'],
                        ['chat','Cyocol','cycol','#007f80','white'],
                        ['chat','Private msg','privatecol','white','#262626'],
                        ['chat','Private username','privatgreen','#00cc00','#262626'],
                        ['chat','Private link','privatlink','#4d93ff','#262626'],
                        ['chat','Dark background','olfo-backgr','black','#c8d9ea'],
                        ['chat','Bright background','light-grey-bg','black','#eaeefa'],
                        ['window','Select background','selectbg','#6B9EB7','#4283A4'],
                        ['window','Rootcolor','rootcolor','black','#DBD9D9'],
                        ['window','Text widget','text-widget','black','white'],
                        ['window','Entry widget','entry-widget','black','white'],
                        ['window','Border-text','border-text','black','default'],
                        ['window','Border-entry','border-entry','black','default'],
                        ['window','Scrollbar','troughcolor','#606060','#9f9f9f'],
                        ['window','Toolbar','toolbar','black','#d9d9d9'],
                        ['window','Toolbar-selected','toolbar-selected','black','#d9d9d9'],
                        ['window','Toolbar-menu','toolbar-menu','black','#d9d9d9'],
                           ]
    ## Windows seems to be the only system that supports these colors, they have to be replaced
    ## Will hardcode for now and fix some day in the future *tm
    if OS == 'Windows':
        default_colors_list[24][4] = 'SystemMenu'
        default_colors_list[25][3] = 'SystemHighlightText'
        default_colors_list[25][4] = 'SystemHighlight'
        default_colors_list[26][4] = 'SystemMenu'
        
    if saved_theme == 'Default':
        chat_color_list = list(default_colors_list)
    else:
        chat_color_list = list_from_file('load/themes/'+saved_theme,',')
    if chat_color_list == []:
        chat_color_list = list(default_colors_list)

    ## Setting global vars
    ver = '1.09z'
    sound_interval = 0
    msg_thrd = 0
    action_time = True
    data_list = []
    msg_recv = 0
    windowfocus = True
    icon_was_switched = False
    kill_reconnect = False
    connected_server = ''
    sender_thread_list, userlog_list, dl_ul_events, linklist = [], [], [], []
    entry_mlist, file_list, thread_message_list = [], [], []
    day_number = strftime("%d")
    entry_message_arch = 0
    USRLIST = []
    default_os_color = ''

    ## Tkinter below
    root = Tk()
    root.title("iSPTC - "+username)
    root.minsize(300,300)
    root.geometry('%sx%s' % (X_size,Y_size))
    maxsize = "5x5"
    textt = StringVar()
    textt.set("")
    ###Toolbar
    class toolbar_alternative:
        def __init__(self):
            self.frame = Frame(root, height=20,width=X_size)
            self.frame.pack_propagate(0)
            self.frame.pack(side=TOP,fill=Y)
            self.menu_btn= tkButton(self.frame,text='Menu', command=self.open_submenu,bd=0,width=10,highlightthickness=0)
            self.menu_btn.pack(side=LEFT)
            self.menu = Menu(None, tearoff=0, takefocus=0)
            self.submenus = toolbar_menus(self.menu)
            self.frame.bind("<Configure>", self.on_resize)
            
        def open_submenu(self):
            self.menu.tk_popup(self.menu_btn.winfo_rootx()+55, self.menu_btn.winfo_rooty()+40,entry="0")

        def destroy(self):
            self.frame.destroy()

        def on_resize(self,event):
            windowX = root.winfo_width()
            self.frame.configure(width=windowX)
            
    class toolbar_default:
        def __init__(self):
            self.menu = Menu(root,tearoff=0,borderwidth=0)
            root.config(menu=self.menu)
            self.submenus = toolbar_menus(self.menu)
            
        def destroy(self):
            self.menu.destroy()
        
    def toolbar_menus(menu):
        menu1 = Menu(menu,tearoff=0)
        menu.add_cascade(label='Server',menu=menu1)
        menu1.add_command(label='Join', command=join_typing)
        menu1.add_command(label='Join last', command=lambda: join_server(False))
        menu1.add_separator()
        menu1.add_command(label='Leave', command=leave_server)
        menu1.add_command(label='Quit', command=closewin)

        menu2 = Menu(menu,tearoff=0)
        menu.add_cascade(label='Tools',menu=menu2)
        menu2.add_command(label='Text editor - Logs/', command=lambda: popen_text_editor('log/'))
        menu2.add_command(label='Text editor - Lib/', command=lambda: popen_text_editor('lib/'))

        menu3 = Menu(menu,tearoff=0)
        menu.add_cascade(label='Commands',menu=menu3)
        menu3.add_command(label='Command window', command=command_window)
        menu3.add_separator()
        menu3.add_command(label='Go afk', command=send_afk)
        menu3.add_command(label='Register', command=lambda: t_auth_window('register'))
        menu3.add_command(label='Auth', command=lambda: t_auth_window('auth'))
        menu3.add_separator()
        menu3.add_command(label='Help', command=T_ins_help)
        menu3.add_command(label='Clear chat', command=reset_textbox)
        menu3.add_command(label='Clear entry', command=lambda: textt.set(''))
        menu3.add_command(label='File list', command=lambda: enter_text('command_window','/fl'))
        menu3.add_command(label='Link list', command=T_ins_linklist)
        menu3.add_command(label='Log', command=T_ins_log)
        menu3.add_command(label='User list', command=T_ins_userlist)

        menu4 = Menu(menu,tearoff=0)
        menu.add_cascade(label='File',menu=menu4)
        menu4.add_command(label='File manager', command=file_manager)
        menu4.add_separator()
        menu4.add_command(label='Open folder', command=lambda: open_address_no_http(fdl_path))
        menu4.add_command(label='Share', command=share_file)

        menu5 = Menu(menu,tearoff=0)
        menu.add_cascade(label='Settings',menu=menu5)
        menu5.add_command(label='Set user', command=username_menu)
        menu5.add_command(label='Set font', command=font_menu)
        menu5.add_command(label='Set download path', command=download_menu)
        menu5.add_command(label='Color settings', command=color_menu)
        menu5.add_command(label='Update settings', command=update_menu)
        menu5.add_command(label='Sound settings', command=sound_menu)
        menu5.add_command(label='Other settings', command=other_menu)

        helpmenu = Menu(menu,tearoff=0)
        menu.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label='Changelog', command=Changelog)
        helpmenu.add_command(label='About..', command=About)
        return (menu1,menu2, menu3, menu4, menu5, helpmenu)

    if scroll_class_u == 'alternative':
        class Scrollbar:
            def __init__(self,widget,*arg):
                self.bg, self.troughcolor,self.highlightbackground, self.highlightcolor = '#DBD9D9','#9f9f9f','#DBD9D9','#606060'
                self.frame = Frame(widget,width=16, height=2, bg=self.bg, bd=0, highlightthickness= 0)
                self.windowY = float(self.frame.winfo_height())
                self.m_x, self.m_y, self.m_x_old, self.m_y_old = 0,0,0,0
                self.bar_color = self.troughcolor
                self.activated = False
                self.command = None
                self.izmers = float(0.5)
                self.kur = float(0.0)
                self.canva = Canvas(self.frame, width=16, height=Y_size, bg=self.bg, bd= 0,highlightthickness= 0, relief= SUNKEN)
                self.canva.bind('<Motion>',self.motion)
                self.bind("<Configure>", self.on_resize)
                self.canva.bind("<Enter>", self.on_enter)
                self.canva.bind("<Leave>", self.on_leave)
                self.canva.bind("<ButtonPress-1>", self.click_view)
                self.canva.bind("<ButtonRelease-1>", self.click_view_stop)
                

            def pack(self,**kwargs):
                for key in kwargs:
                    if str(key) == 'side':
                        sider = kwargs[key]
                self.frame.pack(side=sider,fill=Y)
                self.canva.pack(fill=Y)
                self.canva.create_rectangle(0, self.kur, 16, self.windowY*self.izmers, fill=self.bar_color)

            def on_resize(self,event):
                self.windowY = float(self.frame.winfo_height())
                self.canva.configure(height=self.windowY)
            def on_enter(self,event):
                self.bar_color = self.highlightcolor
                self.redraw_canva()
            def on_leave(self,event):
                self.bar_color = self.troughcolor
                self.redraw_canva()
                
            def configure(self,**kwargs):
                self.on_config(**kwargs)
                self.redraw_canva()

            def config(self,**kwargs):
                self.on_config(**kwargs)
                self.redraw_canva()

            def on_config(self,**kwargs):
                for key in kwargs:
                    if str(key) == 'bg':
                        self.bg = kwargs[key]
                        self.frame.config(bg=self.bg)
                        self.canva.config(bg=self.bg)
                    elif str(key) == 'command':
                        self.command = kwargs[key]
                        self.target_widget = kwargs[key].im_self
                    elif str(key) == 'troughcolor':
                        self.troughcolor = kwargs[key]
                        self.bar_color = self.troughcolor
                    elif str(key) == 'highlightbackground':
                        self.highlightbackground = kwargs[key]
                    elif str(key) == 'highlightcolor':
                        self.highlightcolor = kwargs[key]
                    elif str(key) == 'bd' or str(key) == 'border':
                        self.frame.config(bd=kwargs[key])
                    elif str(key) == 'highlightthickness':
                        self.frame.config(highlightthickness = kwargs[key])
                        
            def destroy(self,*arg):
                self.frame.destroy()

            def redraw_canva(self,*arg):
                izmers = self.izmers
                kur = self.kur
                if izmers > 0.96:
                    izmers = 0.96
                if kur - izmers < 0.04:
                    kur = izmers +0.04
                if self.activated == False:
                    self.canva.create_rectangle(0, self.windowY*kur, 18, self.windowY*izmers, fill=self.bar_color, outline=self.bar_color)
                else:
                    self.canva.create_rectangle(0, self.windowY*kur, 18, self.windowY*izmers, fill=self.highlightcolor, outline=self.highlightcolor)

            def click_view(self,*arg):
                self.activated = True
            def click_view_stop(self,*arg):
                self.activated = False
                self.mouse_click()

            def set(self,izmers,kur):
                self.izmers = float(izmers)
                self.kur = float(kur)
                self.canva.delete(ALL)
                self.redraw_canva()

            def bind(self,button, command):
                self.frame.bind(button, command)

            def motion(self,event,*arg):
                self.m_x, self.m_y = event.x, event.y
                self.m_y = self.m_y + self.windowY/2*(self.izmers - self.kur)
                if self.activated == True:
                    self.mouse_click()

            def mouse_click(self,*arg):
                try:
                    lncount = float(self.target_widget.index("end-1c"))
                except:
                    try:
                        lncount = float(self.target_widget.size())
                    except:
                        print 'Scrollbar: did not find any lines'
                try:
                    calc = 1.00/(self.windowY/self.m_y)
                except ZeroDivisionError:
                    calc = 0.00
                calc = lncount*calc
                self.command(int(calc))
                
            def get(self):
                return self.izmers, self.kur

    ### Window widgets
    def create_widgets():
        global T,E,User_area,S,S2, usra_len, default_os_color, E_borderlen, T_borderlen, S_borderlen, toolbar
        global show_toolbar, use_alternative_tlb
        if show_toolbar == 1:
            if use_alternative_tlb == 0:
                toolbar = toolbar_default()
            else:
                toolbar = toolbar_alternative()
        E = Entry(textvariable=textt)
        User_area = Text(root, height=44, width=usra_len)
        S = Scrollbar(root)
        S2 = Scrollbar(root)
        T = Text(root, height=46, width=114,wrap=WORD)
        configure_border_size(E,E_borderlen)
        configure_border_size(T,T_borderlen)
        try:
            configure_border_size(User_area,T_borderlen)
            configure_border_size(S2,S_borderlen)
        except:
            pass
        configure_border_size(S,S_borderlen)
        S.pack(side=RIGHT, fill=Y)
        if show_users == 1:
            User_area.pack(side=LEFT,fill=Y)
            S2.pack(side=LEFT, fill=Y)
        E.pack(side=BOTTOM,fill=X)
        T.pack(side=BOTTOM,fill=BOTH,expand=1)
        activated_widget = ('E',E)
        S.config(command=T.yview)
        S2.config(command=User_area.yview)
        User_area.config(yscrollcommand=S2.set,state="disabled",wrap='none')
        User_area.bind( '<Configure>', maxsize )
        T.config(yscrollcommand=S.set,state="disabled")
        E.focus_set()   
        default_os_color = root.cget('bg')
        tag_colors(preset='default')
        
        
        root.bind("<Control-a>", widget_sel_all)
        root.bind("<Tab>", focus_entry)
        root.bind("<Control-q>",lambda x: file_manager())
        root.bind("<Control-m>",lambda x: open_address_in_webbrowser(fdl_path))
        root.bind('<Control-j>', join_server_shortcut)
        root.bind('<Control-c>', copy_text)
        root.bind('<Control-g>', command_window)
        T.bind('<Control-f>',lambda x: search_text_dialog(T))
        User_area.bind('<Control-f>',lambda x: search_text_dialog(User_area))
        ##E.bind("<Key>", return_break)
        root.bind('<Return>', enter_text)
        root.bind('<KP_Enter>', enter_text)
        root.bind('<Escape>', reset_entry)
        root.bind('<FocusIn>', winf_is)
        root.bind('<FocusOut>', winf_isnt)
        root.bind('<Motion>', motion)
        root.bind('<Button-1>', deselect_widgets)
        if OS != 'Windows':
            root.bind('<Button-3>', copy_paste_buttons)
            E.bind("<Button-4>", focusT)
            E.bind("<Button-5>", focusT)
            root.bind('<Button-1>', copy_paste_buttons_del)
        if OS == 'Windows':
            root.bind('<Button-3>',rClicker, add='')
            E.bind("<MouseWheel>", focusT)

        E.bind('<Tab>', autocomplete_name)
        ## Entry log
        E.bind('<Up>', entrym_BACK)
        E.bind('<Down>', entrym_FORWARD)
        entry_mlist.append('/ljoin')
        ## Stores name of activated widget for rightclick menu position adjustments
        if OS != 'Windows':
            User_area.bind('<Enter>', set_activated_U)
            T.bind('<Enter>', set_activated_T)
            E.bind('<Enter>', set_activated_E)
            S.bind('<Enter>', set_activated_S)
            S2.bind('<Enter>', set_activated_S2)
            
        global hyperlink_obj, hyperlink_obj2
        hyperlink_obj = HyperlinkManager(T,'hyper')
        hyperlink_obj2 = HyperlinkManager(T,'hyper2')
    ##    def dictprint(*arg):
    ##        print S.__dict__.keys()
        
    def tag_colors(**kwargs):
        global text_font, show_users, chat_color_list, default_colors_list
        global toolbar,default_os_color, use_alternative_tlb, show_toolbar, hyperlink_obj, hyperlink_obj2
        preset = get_dict_item(kwargs,'preset','False')
        window_widget = get_dict_item(kwargs,'window',[])
        text_widgets = get_dict_item(kwargs,'text',[])
        entry_widgets = get_dict_item(kwargs,'entry',[])
        scrollbar_widgets = get_dict_item(kwargs,'scroll',[])
        listbox_widgets = get_dict_item(kwargs,'listbox',[])
        frame_widgets = get_dict_item(kwargs,'frame',[])
        label_widgets = get_dict_item(kwargs,'label',[])
        if preset == 'default':
            global T, E, S, S2, User_area, root
            if show_users == 1:
                text_widgets=[T,User_area]
                entry_widgets=[E]
                scrollbar_widgets=[S,S2]
                window_widget=[root]
            else:
                text_widgets=[T]
                entry_widgets=[E]
                scrollbar_widgets=[S]
                window_widget=[root]
    ##    T.tag_remove('bluecol',1.0,END)
         
        for x in chat_color_list:
            if x[0] == 'chat':
                # Text
                for dd in text_widgets:
                    try:
                        # Hyperlinks
                        if x[2] == 'blue_link':
                            dd.tag_configure('hyper', font=text_font, background=x[4], foreground=x[3])
                        if x[2] == 'privatlink':
                            dd.tag_configure('hyper2', font=text_font, background=x[4], foreground=x[3])
                        # Normal text
                        dd.tag_configure(x[2], font=text_font, background=x[4], foreground=x[3])
                    except Exception as e:
                        e = str(e)
                        scroller = S.get()
                        T_ins_warning(T, S, 'Text ERROR: loading color tags')
                        T_ins_warning(T, S, e)
                        if scroller[1] == 1.0:  
                            T.yview(END)
                # Listbox
                for dd in listbox_widgets:
                    if x[2] == 'blackcol':
                        dd.config(bg=x[4])
                        cnt = 0
                        while True:
                            try:
                                dd.itemconfig(cnt, bg=x[4], fg=x[3])
                                cnt += 1
                            except:
                                break
                # Label fg
                for dd in label_widgets:
                    if x[2] == 'blackcol':
                        dd.configure(foreground=x[3])
                        
            # Window
            elif x[0] == 'window':
                bgcol = x[4]
                if bgcol == 'default':
                    bgcol = default_os_color
                fgcol = x[3]
                if fgcol == 'default':
                    fgcol= 'black'
                try:# Root, Frames, Label bg
                    if x[2] == 'rootcolor':
                        if scroll_class_u != 'system':
                            for dd in scrollbar_widgets:
                                dd.config(bg=bgcol)
                        for dd in window_widget:
                            dd.configure(background=bgcol)
                        for dd in frame_widgets:
                            dd.configure(background=bgcol)
                        for dd in label_widgets:
                            dd.configure(background=x[4])
                    # Text and entry widgets
                    elif x[2] == 'text-widget':
                        for dd in text_widgets:
                            try:
                                dd.config(background=bgcol)
                            except:
                                print dd,' has no background color'
                    elif x[2] == 'entry-widget':
                        for dd in entry_widgets:
                            dd.config(fg=fgcol,insertbackground=fgcol,bg=bgcol)
                    # Borders
                    elif x[2] == 'border-text':
                        for dd in text_widgets:
                            dd.config(highlightbackground=bgcol)
                    elif x[2] == 'border-entry':
                        for dd in entry_widgets:
                            dd.config(highlightbackground=bgcol)
                    # Scrollbars
                    elif x[2] == 'troughcolor':
                        if scroll_class_u != 'system':
                            try:
                                for dd in scrollbar_widgets:
                                    dd.config(troughcolor=bgcol,highlightbackground=fgcol,highlightcolor=fgcol)
                            except Exception as e:
                                e = str(e)
                                scroller = S.get()
                                T_ins_warning(T, S, 'Scrollbar ERROR: loading color tags')
                                T_ins_warning(T, S, e)
                                if scroller[1] == 1.0:  
                                    T.yview(END)
                    # Select
                    elif x[2] == 'selectbg':
                        for dd in text_widgets:
                            dd.configure(inactiveselectbackground=fgcol, selectbackground=bgcol)
                        for dd in entry_widgets:
                            dd.configure(selectbackground=bgcol)
                    # Toolbar color
                    elif show_toolbar == 1:
                        if x[2] == 'toolbar':
                            tcol = bgcol
                            if use_alternative_tlb == 1:
                                toolbar.frame.config(bg=bgcol)
                                toolbar.menu_btn.config(fg=fgcol, bg=bgcol,highlightbackground=fgcol)
                            elif use_alternative_tlb == 0:
                                toolbar.menu.config(bg=bgcol,fg=fgcol)
                        elif x[2] == 'toolbar-selected':
                            if use_alternative_tlb == 1:
                                toolbar.menu_btn.config(activeforeground=fgcol,activebackground=bgcol)
                            toolbar.menu.config(selectcolor=fgcol,activeforeground=fgcol,activebackground=bgcol)
                            for dd in toolbar.submenus:
                                dd.config(activeforeground=fgcol,activebackground=bgcol)
                        elif x[2] == 'toolbar-menu':
                            for dd in toolbar.submenus:
                                dd.config(bg=bgcol,fg=fgcol,selectcolor=fgcol)
                            if use_alternative_tlb == 1:
                                toolbar.menu.config(bg=bgcol,fg=fgcol)
                except Exception as e:
                    e = str(e)
                    scroller = S.get()
                    T_ins_warning(T, S, 'ERROR: loading color tags')
                    T_ins_warning(T, S, e)
                    if scroller[1] == 1.0:  
                        T.yview(END)
    ##    selectbackground="red",highlightbackground="red"
        T.tag_raise("sel")
        User_area.tag_raise("sel")
        E.configure(font=text_font)


    def focusT(event):
        T.focus_set()
    ##    if event.delta == -120:
    ##        print event
    def focus_entry(*arg):
        E.focus_set()
        return "break"
    def return_break(*arg):
        ## Stops tkinter from tabbing
        return "break"
    def join_server_shortcut(*arg):
        join_server(False)
    def click1(*arg):
        pass
    def widget_sel_all(*arg):
    ##    global activated_widget
        activated_widget = root.focus_get() 
        try:
            if activated_widget == E:
                activated_widget.select_range(0, END)
            else:
                activated_widget.tag_add(SEL, "1.0", END)
                activated_widget.mark_set(INSERT, "1.0")
                activated_widget.see(INSERT)
                activated_widget.config(yscrollcommand=S.set,state="disabled")
        except:
            pass
        return "break"
    def deselect_widgets(*arg):
        T.tag_remove(SEL, "1.0", END)
        E.select_clear()
        User_area.tag_remove(SEL, "1.0", END)
    create_widgets()
        


    def task():
        global msg_recv,sound_interval,dsound_interval,username, task_loop_interval, leave_join, userlog_list
        global show_ttime,nadd_spaces,icon_was_switched,T,E,S,S2,User_area,hyperlink,connected_server, write_log
        global file_list, thread_message_list, msg_thrd
        for x in thread_message_list[msg_thrd:]:
            if x[0] == 'command':
                enter_text('command_window',x[1])
            msg_thrd+=1
    ##    getsize = 0
    ##    for x in data_list:
    ##        getsize += sys.getsizeof(x)
    ##    print getsize
        scroller = S.get()
        if sound_interval > 0:
            sound_interval-=float(task_loop_interval)/1000
        if msg_recv < len(data_list):
            for x in range(msg_recv,len(data_list)):
    ##            print data_list[x]
                ## Server messages
                if data_list[x][:9] == 'SSERVER::':
                    T.config(yscrollcommand=S.set,state="normal")
                    name = lenghten_name('SERVER: ',21)
                    T.insert(END, get_cur_time()+name+data_list[x][9:]+'\n','bluecol')
                    userlog_list.append(get_cur_time()+name+data_list[x][9:])
                    if write_log == 1:
                            write_logfile('log/',connected_server,get_cur_time_log()+'SERVER: '+data_list[x][9:]+'\n')
                    T.config(yscrollcommand=S.set,state="disabled")
                ## Private server messages
                elif data_list[x][:9] == 'WSERVER::':
                    T.config(yscrollcommand=S.set,state="normal")
                    name = lenghten_name('SERVER: ',21)
                    T.insert(END, get_cur_time()+name+data_list[x][9:]+'\n','browncol')
                    userlog_list.append(get_cur_time()+name+data_list[x][9:])
                    if write_log == 1:
                            write_logfile('log/',connected_server,get_cur_time_log()+'SERVER: '+data_list[x][9:]+'\n')
                    T.config(yscrollcommand=S.set,state="disabled")
                ## Server leave/join messages
                elif data_list[x][:9] == 'SERVELJ::':
                    if leave_join == 0:
                        doing = 'nothing'
                    else:
                        T.config(yscrollcommand=S.set,state="normal")
                        name = lenghten_name('SERVER: ',21)
                        T.insert(END, get_cur_time()+name+data_list[x][9:]+'\n','bluecol')
                        userlog_list.append(get_cur_time()+name+data_list[x][9:])
                        if write_log == 1:
                            write_logfile('log/',connected_server,get_cur_time_log()+'SERVER: '+data_list[x][9:]+'\n')
                        T.config(yscrollcommand=S.set,state="disabled")
                ## Server closing connection
                elif data_list[x][:9] == 'CLOSING::':
                    T.config(yscrollcommand=S.set,state="normal")
                    war = lenghten_name('WARNING: ',21)
                    T.insert(END, get_cur_time()+name+'Server shutting down\n', 'redcol')
                    leave_server()
                    T.config(yscrollcommand=S.set,state="disabled")
                ## File list
                elif data_list[x][:9] == 'FILLIST::':
                    data_list[x] = data_list[x].rstrip()
                    if data_list[x][9:] == 'EMPTY-LIST':
                        file_list = list(['EMPTY-LIST'])
                    else:
                        file_list = string_to_list(data_list[x][9:])
                ## New file shared
                elif data_list[x][:9] == 'NEWFILE::':
                    b = data_list[x].find(']')
                    T.config(yscrollcommand=S.set,state="normal")
                    name = lenghten_name('SERVER: ',21)
                    T.insert(END, get_cur_time()+name+data_list[x][9:b+0]+' shared a file, type "/dl '+data_list[x][b+1:]+'" or open file manager to download\n','bluecol')
                    userlog_list.append(get_cur_time()+name+data_list[x][9:])
                    T.config(yscrollcommand=S.set,state="disabled")
                ## User list update
                elif data_list[x][:9] == 'USRLIST::':
                    organise_USRLIST(data_list[x][9:])
                ## User name change
                elif data_list[x][:9] == 'DUPLICT::':
                    data_list[x] = data_list[x].rstrip()
                    root.title("iSPTC - "+data_list[x][9:]+' - '+connected_server)
                    username = data_list[x][9:]
                ## Messages from users
                else:
                    userlog_list.append(get_cur_time()+remove_spaces(data_list[x][4:23])+': '+data_list[x][23:])
                    beeped = False
                    mgreen = 'greencol'
                    mblack = 'blackcol'
                    mlink = 'bluecol'
                    T.config(yscrollcommand=S.set,state="normal")
                    usercol,uname = get_user_color(data_list[x][3],data_list[x][4:23],False)
                        
                    temp_list = []
                    dat = data_list[x][23:]
                    b = dat.find('@@')
                    c = dat.find(']')
                    ## Removes "]" from private message
                    if b is not -1 and c is not -1:
                        dat = dat[:c]+' '+dat[c+1:]

                    ## Separates words and append to temp_list
                    dat = dat+' '
                    while True:
                        b = dat.find(' ')
                        temp_list.append(dat[:b]+' ')
                        dat = dat[b+1:]
                        if b is -1:
                            break
                    temp_list[-1] = temp_list[-1][:-2]

                    ## Tags words
                    T.insert(END, get_cur_time(),'blackcol')
                    T.insert(END, uname+': ',usercol)
                    ## Detects private messages
                    if temp_list[0][0:2] == '@@':
                        mgreen = 'privatgreen'
                        mblack = 'privatecol'
                        mlink = 'privatlink'
                        del temp_list[0]
                    ## Username mentioned
                    for x in temp_list:
                        nfind, beeped = find_2name(x,username,uname,beeped)
                        if nfind is True:
                            T.insert(END, x,mgreen)
                        ## Hyperlinks
                        elif nfind is False:
                            linkk = find_link(x)
                            if linkk is not 'False':
                                if mlink == 'privatlink':
                                    T.insert(END, linkk,hyperlink_obj2.add(linkk))
                                else:
                                    T.insert(END, linkk, hyperlink_obj.add(linkk))
                                T.insert(END,' ')
                            if linkk is 'False' and nfind is False:
                                T.insert(END, x,mblack)       
                    T.insert(END,'\n')
                    ## Writes to logfile
                    if write_log == 1:
                        tstring= get_cur_time_log()
                        tstring+=remove_spaces(uname)+': '
                        for x in temp_list:
                            tstring+=x
                        write_logfile('log/',connected_server,tstring+'\n')
                        
                    nfind = False
                    T.config(yscrollcommand=S.set,state="disabled")
                    if windowfocus is False:
                        set_winicon(root,'icon2')
                        icon_was_switched = True
                msg_recv +=1
                if scroller[1] == 1.0:  
                    T.yview(END)
        root.after(task_loop_interval, task)  # reschedule event

    set_winicon(root,'icon')
    root.protocol('WM_DELETE_WINDOW', closewin)
    def startup_task():
        if update_enabled == 1:
            update_checker(update_link)
        else:
            autojoiner()
        load_lib_scripts(root)
        root.after(task_loop_interval, task)
    root.after(50, startup_task)
    root.mainloop()
