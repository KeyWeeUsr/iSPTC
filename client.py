#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from Tkinter import Button as tkButton
from Tkinter import Label as tkLabel
from ttk import Style as ttkStyle
from ttk import Button
from ttk import Scrollbar
from ttk import Checkbutton
from ttk import Radiobutton
from ttk import Combobox
from ttk import Menubutton
from ttk import Scale
from ttk import Separator
from ttk import Treeview
from ttk import Label
from ttk import Entry
##from ttk import Widget
from ttk import Frame as ttkFrame
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

ver = '1.05b'

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

class HyperlinkManager:
    def __init__(self, text,override_font):
        global font_size, text_font
        font = text_font
        fontlist=list(tkFont.families())
        fontlist.sort()
        self.text = text
        if override_font == 'False':
            self.text.tag_config("hyper", font=(fontlist[text_font[0]], font_size), foreground='blue', underline=1)
        else:
            self.text.tag_config("hyper", font=override_font, foreground='blue', underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, addr):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = addr
        linklist.append([tag,addr])
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
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
##        s.send('close::')
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
        bb2.destroy()
        bb3.destroy()
        bb4.destroy()
        bb5.destroy()
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

def copy_paste_buttons_del_thread(*arg):
    sleep(0.2)
##    try:
    cp_destroy()
##    except:
##        pass

def copy_paste_buttons_del(*arg):
    Thread(target=copy_paste_buttons_del_thread).start()

def copy_paste_buttons(*arg):
    global bb2, bb1, bb3, bb4, bb5, m_x, m_y, activated_widget, usra_len, X_size, Y_size, hide_users
    if activated_widget == 'T' and hide_users == 0:
        m_x += usra_len*8
    elif activated_widget == 'E':
        m_y += Y_size-130
        if hide_users == 0:
            m_x += usra_len*8
    elif activated_widget == 'S2' and hide_users == 0:
        m_x += usra_len*7
        
    if m_x > X_size-130:
        m_x = X_size-130
    if m_y > Y_size - 130:
        m_y = Y_size - 130
    try:
        cp_destroy()
    except:
        pass
    bb1 = tkButton(root, text='Open in browser', width=50,
                    command=lambda: {open_in_browser_btn(),cp_destroy()})
    bb1.place(x=m_x, y=m_y,width=120, height=26)
    bb2 = tkButton(root, text='Command window', width=50,
                    command=lambda: {command_window(),cp_destroy()})
    bb2.place(x=m_x, y=m_y+26,width=120, height=26)
    bb3 = tkButton(root, text='Clear', width=50,
                    command=lambda: {textt.set(''),cp_destroy()})
    bb3.place(x=m_x, y=m_y+52,width=120, height=26)   
    bb4 = tkButton(root, text='Copy', width=50,
                    command=lambda: {copy_text(),cp_destroy()})
    bb4.place(x=m_x, y=m_y+78,width=120, height=26)
    bb5 = tkButton(root, text='Paste', width=50,
                    command=lambda: {entry_paste(),cp_destroy()})
    bb5.place(x=m_x, y=m_y+104,width=120, height=26)
##    bb1.config(relief=SUNKEN,bd=1)
##    bb2.config(relief=SUNKEN,bd=1)
##    bb3.config(relief=SUNKEN,bd=1)
##    bb4.config(relief=SUNKEN,bd=1)
##    bb5.config(relief=SUNKEN,bd=1)

def sender_thread():
    global sender_thread_list, s, action_time
    tim = 0
    while True:
        if len(sender_thread_list) > 0:
            try:
                s.send(sender_thread_list[0])
                sender_thread_list.pop(0)
            except Exception as e:
                print str(e)
                action_time = False
        else:
            if action_time == False:
                break
        tim+=(0.07)
        if tim > 6:
            sender_thread_list.append('kpALIVE::')
            tim = 0
        sleep(0.07)
        
def recv_thread():
    global action_time, s, connected_server
    while action_time is True:
        try:
            data = s.recv(4096)
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
    global username, s, action_time, passwd, autoauth, offline_msg, kill_reconnect, connected_server, ver
    scroller = S.get()
    try:
        action_time = False
        s.send('close::')
        sleep(0.2)
        s.close()
    except:
        pass
    try:
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
        Thread(target=sender_thread).start()
        if passwd is '' or autoauth is 0:
            sender_thread_list.append('USRINFO::'+username)
##            s.send('USRINFO::'+username)
        else:
            sender_thread_list.append('USRINFO::'+username+']'+passwd)
##            s.send('USRINFO::'+username+']'+passwd)
        sender_thread_list.append('CONFIGR::offmsg='+str(offline_msg)+' ver=iSPTC-'+ver)
##        s.send('CONFIGR::offmsg='+str(offline_msg)+' ver=iSPTC-'+ver)
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

def open_address_in_webbrowser(address):
    a = address.find('http://')
    b = address.find('https://')
    c = address.find('www.')
    if a == -1 and b == -1 and c == -1:
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

def T_ins_help():
    global USRLIST
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, '[Help]\n', 'light-grey-bg')
    T.insert(END, 'Type:\n/help to see this message \n/u to show userlist\n/log to show chatlog\n'+
             '/afk to go afk\n/ll to see all links\n'+'/reg "password" to register\n'+
             '/auth "password" to authenticate\n/clear to clear textbox\n/share to share a file\n'+
             '/fm to open file manager\n/fl to show file list\n/files to open download folder\n', 'light-grey-bg')
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
        s.send('aAFKAFK::')
    except:
        pass

def attempt_registration(s,authps):
    if len(authps) < 4:
        T_ins_warning(T,S,'Too short')
    else:
        try:
            s.send('aUSRREG::'+authps)
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
        s.send('USRLOGI::'+authps)
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
            T.insert(END, str(x)+'\n', 'light-grey-bg')
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
    elif text == '/fm':
        file_manager()
    elif text == '/fl':
        T_ins_file_list()
    elif text == '/files':
        open_address_in_webbrowser(fdl_path)
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
##                    s.send(mesig)
                except Exception as ee:
                    T_ins_warning(T,S,str(ee))
    T.yview(END)

def clear_textbox(clt,disable):
    clt.config(yscrollcommand=S.set,state="normal")
    clt.delete(1.0,END)
    if disable == True:
        User_area.config(yscrollcommand=S.set,state="disabled")

def leave_server():
    global s,action_time
    war = lenghten_name('WARNING: ',21)
    try:
        sender_thread_list.append('close::')
##        s.send('close::')
        action_time = False
        sleep(0.2)
        s.close()
        s = ''
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, get_cur_time()+war+'Left server\n', 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")
        User_area.config(yscrollcommand=S.set,state="normal")
        User_area.delete(1.0,END)
        User_area.config(yscrollcommand=S.set,state="disabled")
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
    else:
        INPUT = 'python updater.py'
    Popen([INPUT], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    root.quit() 

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
        yes = True
    ## Creates dialogue window
    if yes == True:
        def update_updater():
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
    global ver
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
    global font_size, text_font, hide_users
    fontlist=list(tkFont.families())
    fontlist.sort()
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
    Tbox.tag_configure('blackcol', font=(fontlist[text_font[0]], font_size), foreground='black')
    Tbox.tag_configure('CL-bg', font=(fontlist[text_font[0]], font_size), background='#80ccff',foreground='black')
    Tbox.tag_configure('SE-bg', font=(fontlist[text_font[0]], font_size), background='#66cc66',foreground='black')
    Tbox.tag_configure('light-bg', font=(fontlist[text_font[0]], font_size), background='#f3f3f3',foreground='black')
    Tbox2.tag_configure('blackcol', font=(fontlist[text_font[0]], font_size), foreground='black')
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
                b = x.find('download,')
                if b is not -1:
                    downlist.append(x)
                b = x.find('move,')
                if b is not -1:
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
    global font_size, text_font
    font = text_font
    fontlist=list(tkFont.families())
    fontlist.sort()
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
    tEntry.configure(font=(fontlist[text_font[0]], font_size), foreground='black')
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
##                    s.send('USRINFO::'+username)
                else:
                    sender_thread_list.append('USRINFO::'+username+']'+passwd)
##                    s.send('USRINFO::'+username+']'+passwd)
            except:
                pass
        
    new_offline_msg = t_offline_msg.get()
    if new_offline_msg != offline_msg:
        offline_msg = new_offline_msg
        write_settings('offline_msg',offline_msg)
        try:
            sender_thread_list.append('CONFIGR::offmsg='+str(offline_msg))
##            s.send('CONFIGR::offmsg='+str(offline_msg))
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
    

def color_menu():
    global font_size, text_font
    colm = Toplevel()
    set_winicon(colm,'icon_grey')
    colm.title("Color settings")
    colm.minsize(700,400)
    colm.resizable(FALSE,FALSE)

##    frame = Frame(colm, height=380,width=300, relief=SUNKEN)
##    frame2 = Frame(colm, height=400,width=400, relief=SUNKEN)
##    frame.pack_propagate(0)
##    frame2.pack_propagate(0)
##    frame.pack(anchor=NE,side=LEFT)
##    frame2.pack(anchor=NE,side=LEFT)
    def callback(*arg):
        print arg
        gotcol = askcolor()
##        print gotcol
    colorbutton_list = []
    colorbutton_list2 = [['red','red','white'],['Blue','blue','white'],['Green','#009900','white'],
                         ['Purple','purple','white'],['Grey','#7F7F7F','white'],['Black','black','white'],
                         ['Pink','pink','white'],['Orange','orange','white'],['Link','blue','white'],
                         ['Time','black','white'],['Brown','#862d2d','white'],['Cyocol','#007f80','white'],
                         ['Private','white','#262626'],['Private green','#00cc00','#262626'],
                         ['Private link','#4d93ff','#262626'],['Dark background','black','#c8d9ea'],
                         ['Light background','black','#eaeefa']]
    for x in colorbutton_list2:
        colorbutton_list.append(x)
    cnt = 0
    col = 0
    for x in colorbutton_list:
        if x[2] is not '':
            tkButton(colm, text=x[0], fg=x[1], bg=x[2],width=11,
                   command=lambda: callback(str(x[1]),str(x[2]))).place(x=20+col*116,y=20+cnt*30)
        else:
            tkButton(colm, text=x[0], fg=x[1],width=11,
                   command=lambda: callback(x[1])).place(x=20+col*116,y=20+cnt*30)
        cnt += 1
        if cnt == 4:
            col += 1
            cnt = 0
            
    def close_func(*arg):
        colm.destroy()
    colm.bind('<Escape>', close_func)
    

def set_font(font,fontlist,t_font_size,t_usra_len):
    global T,E,User_area, text_font, font_size, usra_len
    if font is not ():
        text_font = font
        write_settings('tfont',text_font[0])
    try:
        font_size = t_font_size
    except:
        pass
    
    User_area.config(width=t_usra_len)
    tag_colors()
    hyperlink = HyperlinkManager(T,'False')
    usra_len = t_usra_len
    write_settings('font_size',font_size)
    write_settings('usra_len',usra_len)
    
def font_menu():
    global font_size, text_font, usra_len
    fom = Toplevel()
    set_winicon(fom,'icon_grey')
    fom.title("Font settings")
    fom.minsize(700,400)
    fom.resizable(FALSE,FALSE)

    frame = Frame(fom, height=380,width=300, relief=SUNKEN)
    frame2 = Frame(fom, height=400,width=400, relief=SUNKEN)
    frame.pack_propagate(0)
    frame2.pack_propagate(0)
    frame.pack(anchor=NE,side=LEFT)
    frame2.pack(anchor=NE,side=LEFT)

    t_font_size = IntVar()
    t_usra_len = IntVar()
    t_font_size.set(font_size)
    t_usra_len.set(usra_len)
    
    fonts=list(tkFont.families())
    fonts.sort()
    display = Listbox(frame)
    scroll = Scrollbar(frame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    display.pack(padx=10, fill=BOTH, expand=YES, side=LEFT)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)
    for item in fonts:
        display.insert(END, item)

    Label(frame2, text="Font size:",justify = LEFT).place(x=20,y=300)
    Efont_size = Entry(frame2,textvariable=t_font_size,width=3).place(x=100,y=300)
    Label(frame2, text="User_area length:",justify = LEFT).place(x=140,y=300)
    User_area_length = Entry(frame2,textvariable=t_usra_len,width=3).place(x=260,y=300)
    
    display_text = Text(frame2, height=12, width=50,wrap=WORD)
    display_text.place(x=20,y=80)
    display_text.insert(END, get_cur_time()+' SERVER: Hello human\n','bluecol')
    display_text.insert(END, get_cur_time()+' WARNING: Hello human\n','redcol')
    display_text.insert(END, get_cur_time()+' Human: Hello\n','greencol')
    display_text.insert(END, get_cur_time()+' SERVER: human is afk\n','greycol')
    display_text.insert(END, get_cur_time()+' Admin: /kick human\n','purplecol')
    display_text.insert(END, get_cur_time()+' Cat: hello\n','blackcol')
    display_text.insert(END, get_cur_time()+' Orange: the new color\n','orangecol')
    display_text.insert(END, get_cur_time()+' Mouse: hello cat\n','privatecol')
    display_text.insert(END, get_cur_time()+' Twitterbot: Falcon has landed\n','olfo-backgr')

    button2 = Button(frame2, text='Apply', command=lambda: {apply_display_font(display_text,display.curselection(),fonts,
                                                        t_font_size.get())})
    button = Button(frame2, text='Save', command=lambda: {set_font(display.curselection(),fonts,t_font_size.get(),
                                              t_usra_len.get()), fom.destroy()})
    button.place(x=200,y=360)
    button2.place(x=40,y=360)
    apply_display_font(display_text,text_font,fonts,font_size)
    def close_func(*arg):
        fom.destroy()
    def focusList(event):
        display.focus_set()
    fom.bind('<Escape>', close_func)
    if OS != 'Windows':
        fom.bind("<Button-4>", focusList)
        fom.bind("<Button-5>", focusList)
    if OS == 'Windows':
        fom.bind("<MouseWheel>", focusList)

def apply_display_font(display_text,font,fontlist,t_font_size):
    global font_size, text_font
    try: 
        if len(font) > 0:
            text_font = font
    except:
        pass
    try:
        font_size = t_font_size
    except:
        pass
    display_text.tag_configure('redcol', font=(fontlist[text_font[0]], font_size), foreground='red')
    display_text.tag_configure('bluecol', font=(fontlist[text_font[0]], font_size), foreground='blue')
    display_text.tag_configure('greencol', font=(fontlist[text_font[0]], font_size), foreground='#009900')
    display_text.tag_configure('purplecol', font=(fontlist[text_font[0]], font_size), foreground='purple')
    display_text.tag_configure('greycol', font=(fontlist[text_font[0]], font_size), foreground='#7F7F7F')
    display_text.tag_configure('blackcol', font=(fontlist[text_font[0]], font_size), foreground='black')
    display_text.tag_configure('privatecol', font=(fontlist[text_font[0]], font_size), background='#222222',foreground='white')
    display_text.tag_configure('olfo-backgr', font=(fontlist[text_font[0]], font_size), background='#c8d9ea',foreground='black')
    display_text.tag_configure('orangecol', font=(fontlist[text_font[0]], font_size), foreground='#e65b00')
    

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
                    tkMessageBox.showerror(title='File list', message='File list is empty')
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
        e = str(e)
        if e == "global name 's' is not defined" or e == "'str' object has no attribute 'send'":
            e = 'Not connected!'
        tkMessageBox.showerror(title='Error', message=str(e))

def change_other_settings(a,c,e,f,g,h,i,j):
    global X_size,Y_size ,autojoin, leave_join, nadd_spaces, show_ttime, hide_users, autoauth
    global User_area, S2, T, S, E, s, username, write_log, show_logtime
    autojoin = a
    leave_join = c
    nadd_spaces = e
    autoauth = h
    write_log = i
    show_logtime = j

    if hide_users is not g:
        hide_users = g
        if g == 1:
            User_area.destroy()
            S2.destroy()
        else:
            T.destroy()
            E.destroy()
            S.destroy()
            create_widgets()
            user_area_insert()
    show_ttime = f
    write_settings('show_ttime',f)
    write_settings('autojoin',a)
    write_settings('leave_join',c)
    write_settings('nadd_spaces',e)
    write_settings('hide_users',g)
    write_settings('autoauth',h)
    write_settings('chlog',i)
    write_settings('show_logtime',j)
##    root.geometry('%sx%s' % (X_size,Y_size))
    
def other_menu():
    global autojoin, leave_join, nadd_spaces, show_ttime, hide_users, autoauth, write_log, show_logtime
    sm = Toplevel()
    set_winicon(sm,'icon_grey')
    sm.title("Other settings")
    sm.minsize(500,250)
    sm.resizable(FALSE,FALSE)
    frame = Frame(sm, height=160,width=210, relief=SUNKEN)
    frame.pack_propagate(0)
    frame.pack(anchor=NE,side=LEFT,padx=10,pady=10)
    frame2 = Frame(sm, height=160,width=210, relief=SUNKEN)
    frame2.pack_propagate(0)
    frame2.pack(anchor=NE,side=LEFT,padx=10,pady=10)
    frame3 = Frame(sm, height=40,width=500, relief=SUNKEN)
    frame3.pack_propagate(0)
    frame3.place(x=180,y=200)
    
    t_leave_join = IntVar()
    t_autoauth = IntVar()
    t_autojoin = IntVar()
    t_write_log = IntVar()
    t_lenghten = IntVar()
    t_hide_users = IntVar()
    t_box_time = IntVar()
    t_log_time = IntVar()
    t_leave_join.set(leave_join)
    t_autoauth.set(autoauth)
    t_autojoin.set(autojoin)
    t_write_log.set(write_log)
    t_lenghten.set(nadd_spaces)
    t_hide_users.set(hide_users)
    t_box_time.set(show_ttime)
    t_log_time.set(show_logtime)
    
    Checkbutton(frame, text="Show leave and join", variable=t_leave_join).pack(anchor=NW)
    Checkbutton(frame, text="Enable autoauthentication", variable=t_autoauth).pack(anchor=NW)
    Checkbutton(frame, text="Enable autojoin", variable=t_autojoin).pack(anchor=NW)
    Label(frame, text="\nLog file time:",justify = LEFT).pack(anchor=NW)
    Radiobutton(frame,text="Show full",variable=t_log_time,value=3).pack(anchor=NW)
    Radiobutton(frame,text="Without seconds",variable=t_log_time,value=2).pack(anchor=NW)
    Radiobutton(frame,text="Hide",variable=t_log_time,value=1).pack(anchor=NW)

    Checkbutton(frame2, text="Enable log writing", variable=t_write_log).pack(anchor=NW)
    Checkbutton(frame2, text="Force 19chr length usernames", variable=t_lenghten).pack(anchor=NW)
    Checkbutton(frame2, text="Hide userbox", variable=t_hide_users).pack(anchor=NW)
    Label(frame2, text="\nTextbox time:",justify = LEFT).pack(anchor=NW)
    Radiobutton(frame2,text="Show full",variable=t_box_time,value=3).pack(anchor=NW)
    Radiobutton(frame2,text="Without seconds",variable=t_box_time,value=2).pack(anchor=NW)
    Radiobutton(frame2,text="Hide",variable=t_box_time,value=1).pack(anchor=NW)

    button = Button(frame3, text='Save', command=lambda: {change_other_settings(t_autojoin.get(),
                    t_leave_join.get(),t_lenghten.get(),t_box_time.get(),t_hide_users.get(),
                    t_autoauth.get(),t_write_log.get(),t_log_time.get()),
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
    global USRLIST, hide_users
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

    if hide_users == 0:
        user_area_insert()

def user_area_insert():
    global USRLIST
    User_area.config(yscrollcommand=S2.set,state="normal")
    User_area.delete(1.0,END)
    for x in USRLIST:
        try:
            if x == []:
                User_area.insert(END,'\n')
            else:
                usercol = get_user_color(x[2],x[0],False)
                ## Offline color
                if x[1] == 'Offline':
                    User_area.insert(END, x[0]+'\n','greycol')
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
    User_area.config(yscrollcommand=S2.set,state="disabled")

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
    for x in TLDS:
        begn = data.find('.'+x)
        if begn is not -1 and len(data) > begn:
            return data
    return 'False'

def copy_text(*arg):
    try:
        try:
            T.config(state="normal")
            T.clipboard_clear()
            text = T.get("sel.first", "sel.last")
            T.clipboard_append(text)
            T.config(state="disabled")
        except:
            try:
                User_area.config(state="normal")
                User_area.clipboard_clear()
                text = User_area.get("sel.first", "sel.last")
                User_area.clipboard_append(text)
                User_area.config(state="disabled")
            except:
                E.clipboard_clear()
                text = E.selection_get()
                E.clipboard_append(text)
    except:
        pass

def entry_paste(*arg):
    try:
        text = root.selection_get(selection='CLIPBOARD')
        E.insert('insert', text)
    except:
        print 'Nothing in clipboard'

def autocomplete_name(*arg):
    is_private = False
    try:
        ## Finds the last word in entry widget
        if len(USRLIST) > 0:
            text = textt.get()
            text = text[::-1]
            cnt = 0
            for x in text:
                if x == ' ':
                    text = text[:cnt]
                    break
                cnt += 1
            text = text[::-1]
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
                print "ERROR: loading module"
                print e

def Changelog():
    global font_size, text_font, window_sizes
    def closethis():
        write_settings('win_changelog_x',topwin.winfo_width())
        write_settings('win_changelog_y',topwin.winfo_height())
        window_sizes[0][0], window_sizes[0][1] = str(topwin.winfo_width()),str(topwin.winfo_height())
        topwin.destroy()
    font = text_font
    fontlist=list(tkFont.families())
    fontlist.sort()
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
    Tbox.tag_configure('blackcol', font=(fontlist[text_font[0]], font_size+2, 'normal'), foreground='black')
    Tbox.tag_configure('CL-bg', font=(fontlist[text_font[0]], font_size+2), background='#80ccff',foreground='black')
    Tbox.tag_configure('SE-bg', font=(fontlist[text_font[0]], font_size+2), background='#66cc66',foreground='black')
    Tbox.tag_configure('UP-bg', font=(fontlist[text_font[0]], font_size+2), background='#FF7373',foreground='black')
    Tbox.tag_configure('dark-bg', font=(fontlist[text_font[0]], font_size+2), background='#cccccc',foreground='black')
    Tbox.tag_configure('light-bg', font=(fontlist[text_font[0]], font_size+2), background='#f3f3f3',foreground='black')
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
    def close_func(*arg):
        topwin.destroy()
    topwin.bind('<Escape>', close_func)

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
    activated_widget = 'T'
def set_activated_U(*arg):
    global activated_widget
    activated_widget = 'U'
def set_activated_E(*arg):
    global activated_widget
    activated_widget = 'E'
def set_activated_S(*arg):
    global activated_widget
    activated_widget = 'S'
def set_activated_S2(*arg):
    global activated_widget
    activated_widget = 'S2'

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
hide_users = int(read_settings('hide_users=',0))
X_size = int(read_settings('X_size=',800))
Y_size = int(read_settings('Y_size=',600))
font_size = int(read_settings('font_size=',10))
text_font = (int(read_settings('tfont=',10)),)
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

## Setting global vars
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
activated_widget = 'E'
## Tkinter below
root = Tk()
root.title("iSPTC - "+username)
root.minsize(300,300)
root.geometry('%sx%s' % (X_size,Y_size))
maxsize = "5x5"
textt = StringVar()
textt.set("")
###Toolbar
menu = Menu(root,tearoff=0,borderwidth=0)
root.config(menu=menu)
menu1 = Menu(menu,tearoff=0)
menu.add_cascade(label='Server',menu=menu1)
menu1.add_command(label='Join', command=join_typing)
menu1.add_command(label='Join last', command=lambda: join_server(False))
menu1.add_separator()
menu1.add_command(label='Leave', command=leave_server)
menu1.add_command(label='Quit', command=closewin)

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
menu4.add_command(label='Download manager', command=file_manager)
menu4.add_separator()
menu4.add_command(label='Open folder', command=lambda: open_address_in_webbrowser(fdl_path))
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

### Window widgets
def create_widgets():
    global T,E,User_area,S,S2,hyperlink, usra_len
    E = Entry(textvariable=textt)
    User_area = Text(root, height=44, width=usra_len)
    S = Scrollbar(root)
    S2 = Scrollbar(root)
    T = Text(root, height=46, width=114,wrap=WORD)
    ## bordercolors
##    root.configure(background='red')
##    widliste = [T,E,User_area, S, S2]
##    widliste = [S,S2]
##    for x in widliste:
##        x.config(background='black')
##    for x in widliste:
##        x.config(highlightthickness=0)
##    for x in widliste:
##        x.config(highlightbackground='black')
##    for x in widliste:
##        x.config(bd=0)
##    for x in widliste:
##        x.config(troughcolor='black')

    S.pack(side=RIGHT, fill=Y)
    if hide_users == 0:
        User_area.pack(side=LEFT,fill=Y)
        S2.pack(side=LEFT, fill=Y)
    E.pack(side=BOTTOM,fill=X)
    T.pack(side=BOTTOM,fill=BOTH,expand=1)
    S.config(command=T.yview)
    S2.config(command=User_area.yview)
    User_area.config(yscrollcommand=S2.set,state="disabled",wrap='none')
    User_area.bind( '<Configure>', maxsize )
    T.config(yscrollcommand=S.set,state="disabled")
    E.focus_set()
    hyperlink = HyperlinkManager(T,'False')
    tag_colors()
def tag_colors():
    global font_size, text_font, hide_users
    fontlist=list(tkFont.families())
    fontlist.sort()
    T.tag_configure('redcol', font=(fontlist[text_font[0]], font_size), foreground='red')
    T.tag_configure('bluecol', font=(fontlist[text_font[0]], font_size), foreground='blue')
    T.tag_configure('greencol', font=(fontlist[text_font[0]], font_size), foreground='#009900')
    T.tag_configure('purplecol', font=(fontlist[text_font[0]], font_size), foreground='purple')
    T.tag_configure('greycol', font=(fontlist[text_font[0]], font_size), foreground='#7F7F7F')
    T.tag_configure('blackcol', font=(fontlist[text_font[0]], font_size), foreground='black')
    T.tag_configure('pinkcol', font=(fontlist[text_font[0]], font_size), foreground='pink')
    T.tag_configure('orangecol', font=(fontlist[text_font[0]], font_size), foreground='#e65b00')
    T.tag_configure('blue_link', font=(fontlist[text_font[0]], font_size), foreground='blue')
    T.tag_configure('timecol', font=(fontlist[text_font[0]], font_size), foreground='black')
    T.tag_configure('browncol', font=(fontlist[text_font[0]], font_size), foreground='#862d2d')
    T.tag_configure('cycol', font=(fontlist[text_font[0]], font_size), foreground='#007f80')
    T.tag_configure('privatecol', font=(fontlist[text_font[0]], font_size), background='#262626',foreground='white')
    T.tag_configure('privatgreen', font=(fontlist[text_font[0]], font_size), background='#262626',foreground='#00cc00')
    T.tag_configure('privatlink', font=(fontlist[text_font[0]], font_size), background='#4d93ff',foreground='blue')
    T.tag_configure('olfo-backgr', font=(fontlist[text_font[0]], font_size), background='#c8d9ea',foreground='black')
    T.tag_configure('light-grey-bg', font=(fontlist[text_font[0]], font_size), background='#eaeefa',foreground='black')
##    T.configure(selectbackground="red", inactiveselectbackground="green")
    if hide_users is not 1:
        User_area.tag_configure('olfo-backgr', font=(fontlist[text_font[0]], font_size), background='#c8d9ea',foreground='black')
        User_area.tag_configure('cycol', font=(fontlist[text_font[0]], font_size), foreground='#007f80')
        User_area.tag_configure('orangecol', font=(fontlist[text_font[0]], font_size), foreground='#e65b00')
        User_area.tag_configure('blackcol', font=(fontlist[text_font[0]], font_size), foreground='black')
        User_area.tag_configure('pinkcol', font=(fontlist[text_font[0]], font_size), foreground='pink')
        User_area.tag_configure('purplecol', font=(fontlist[text_font[0]], font_size), foreground='purple')
        User_area.tag_configure('greycol', font=(fontlist[text_font[0]], font_size), foreground='#7F7F7F')
        User_area.tag_configure('redcol', font=(fontlist[text_font[0]], font_size), foreground='red')
        User_area.tag_configure('offcol', font=(fontlist[text_font[0]], font_size), foreground='#66CCFF')
    E.configure(font=(fontlist[text_font[0]], font_size), foreground='black')

create_widgets()
    
def focusT(event):
    T.focus_set()
##    if event.delta == -120:
##        print event
def focus_entry(*arg):
    E.focus_set()
def return_break(*arg):
    ## Stops tkinter from tabbing
    return "break"
def join_server_shortcut(*arg):
    join_server(False)
def click1(*arg):
    pass

root.bind("<Tab>", return_break)
root.bind("<Control-q>",lambda x: file_manager())
root.bind("<Control-m>",lambda x: open_address_in_webbrowser(fdl_path))
root.bind('<Control-j>', join_server_shortcut)
root.bind('<Control-c>', copy_text)
root.bind('<Control-g>', command_window)
##E.bind("<Key>", return_break)
root.bind('<Return>', enter_text)
root.bind('<KP_Enter>', enter_text)
root.bind('<Escape>', reset_entry)
root.bind('<FocusIn>', winf_is)
root.bind('<FocusOut>', winf_isnt)
root.bind('<Motion>', motion)
if OS != 'Windows':
    root.bind('<Button-3>', copy_paste_buttons)
    root.bind("<Button-4>", focusT)
    root.bind("<Button-5>", focusT)
    root.bind('<Button-1>', copy_paste_buttons_del)
if OS == 'Windows':
    root.bind('<Button-3>',rClicker, add='')
    root.bind("<MouseWheel>", focusT)

E.bind('<Tab>', autocomplete_name)
## Entry log
E.bind('<Up>', entrym_BACK)
E.bind('<Down>', entrym_FORWARD)
## Stores name of activated widget for rightclick menu position adjustments
if OS != 'Windows':
    User_area.bind('<Enter>', set_activated_U)
    T.bind('<Enter>', set_activated_T)
    E.bind('<Enter>', set_activated_E)
    S.bind('<Enter>', set_activated_S)
    S2.bind('<Enter>', set_activated_S2)


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
                            T.insert(END, linkk, hyperlink.add(linkk))
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
