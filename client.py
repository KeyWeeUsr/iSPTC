#!/usr/bin/env python
from Tkinter import *
from threading import Thread
from random import randrange
from time import strftime,gmtime,sleep
import socket,os,platform
OS = platform.system()
sys_path = os.getcwd()
print sys_path
if OS is 'Windows':
    import winsound
    
ver = '1.12.15'

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

def read_settings(text_find):
    a = readf('load/settings')
    a = get_settings(a,text_find)
    return a

def get_settings(text,text_find):
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = lines[len(text_find):]
    return c

def write_settings(text_find,new_value):
    a = readf('load/settings')
    a = edit_settings(a,text_find,new_value)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,'load/settings')

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

class Test(Text):
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


def closewin():
    global s, action_time
    print 'Goodbye'
    action_time = False
    try:
        s.send('close::')
        sleep(1)
        s.close()
        root.destroy()
    except:
        sleep(1)
        root.destroy()

def get_cur_time():
    return strftime("%H:%M:%S")

def recv_thread(s):
    global action_time
    while action_time is True:
        data = s.recv(2048)
        if not data:
            break
        data_list.append(data+'\n')
        
def join_typing():
    joinaddr = str(read_settings('joinaddr='))
    jaddr = StringVar()
    jaddr.set(joinaddr)
    jsrv = Toplevel()
    set_winicon(jsrv,'icon')
    jsrv.title("Server address")
    jsrv.minsize(250,100)
    jsrv.resizable(FALSE,FALSE)
    usrEntry = Entry(jsrv,textvariable=jaddr)
    usrEntry.pack(pady=25)
    button = Button(jsrv, text='Done', width=20,pady=10, command=lambda: {join_server(jaddr.get()),
                                                                jsrv.destroy()})
    button.pack()
    
def join_server(typing):
    global username, s, action_time
    try:
        action_time = False
        s.send('close::')
        sleep(2)
        s.close()
    except:
        pass
    try:
        if typing is not False:
            TCP_IP = typing
            TCP_PORT = 8001
            write_settings('joinaddr',TCP_IP) 
        else:
            joinaddr = str(read_settings('joinaddr='))
            TCP_IP = joinaddr
            TCP_PORT = 8001
        BUFFER_SIZE = 2048
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'joining',TCP_IP, TCP_PORT
        s.connect((TCP_IP, TCP_PORT))
        action_time = True
        Thread(target=recv_thread,args=(s,)).start()
        sleep(1)
        s.send('USRINFO::'+username)
    except:
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, get_cur_time()+"         WARNING: Can't join\n", 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")
        
def enter_text(event):
    global s
##    T.config(yscrollcommand=S.set,state="normal")
##    T.config(yscrollcommand=S.set,state="disabled")
    text = textt.get()
    textt.set('')
    if len(text) > 0:
        if sound_settings[1] == True:
            play_sound('beep1.wav',True)
        try:
            s.send('MESSAGE::'+text)
        except:
            T.config(yscrollcommand=S.set,state="normal")
            T.insert(END, get_cur_time()+'         WARNING: Not connected\n', 'redcol')
            T.config(yscrollcommand=S.set,state="disabled")

def leave_server():
    global s
    try:
        s.send('close::')
        action_time = False
        sleep(0.5)
        s.close()
        s = ''
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, get_cur_time()+'         WARNING: Left server\n', 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")
        User_area.config(yscrollcommand=S.set,state="normal")
        User_area.delete(1.0,END)
        User_area.config(yscrollcommand=S.set,state="disabled")
    except:
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, get_cur_time()+'         WARNING: Not connected\n', 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")

def change_name(new_name):
    global username, s
    new_name = new_name.get()
    username = new_name
    root.title("iSPTC - "+new_name)
    write_settings('username',username)
    try:
        s.send('USRINFO::'+username)
    except:
        pass
    
def set_username():
    new_name = StringVar()
    new_name.set("")
    uw = Toplevel()
    set_winicon(uw,'icon')
    uw.title("New name")
    uw.minsize(250,100)
    uw.resizable(FALSE,FALSE)
    usrEntry = Entry(uw,textvariable=new_name)
    usrEntry.pack(pady=25)
    button = Button(uw, text='Done', width=20, command=lambda: {change_name(new_name),
                                                                uw.destroy()})
    button.pack()
    
def change_sound_set(a,b,c):
    sound_settings[0] = a
    sound_settings[1] = b
    sound_settings[2] = c
    write_settings('enable_sound',a)
    write_settings('entry_enabled',b)
    write_settings('user_textbox',c)

def sound_menu():
    sw = Toplevel()
    set_winicon(sw,'icon')
    sw.title("Sound options")
    sw.minsize(280,140)
    sw.resizable(FALSE,FALSE)
    ### 0all_sound, 1entry, 2user textbox
    sound_enabled = IntVar()
    entry_enabled = IntVar()
    user_textbox = IntVar()
    sound_enabled.set(sound_settings[0])
    entry_enabled.set(sound_settings[1])
    user_textbox.set(sound_settings[2])
    Checkbutton(sw, text="Enable sound", variable=sound_enabled).grid(row=1, sticky=W,padx=20)
    Checkbutton(sw, text="Entry sound", variable=entry_enabled).grid(row=2, sticky=W,padx=20)
    Checkbutton(sw, text="Textbox sound", variable=user_textbox).grid(row=3, sticky=W,padx=20)
    button = Button(sw, text='Done', width=20,
                    command=lambda: {change_sound_set(sound_enabled.get(),entry_enabled.get(),
                                                      user_textbox.get()),sw.destroy()})
    button.grid(row=4, padx=60,pady=10)

def change_other_settings(a):
    global autojoin
    autojoin = a
    write_settings('autojoin',a)
    
def other_menu():
    sm = Toplevel()
    set_winicon(sm,'icon')
    sm.title("Other options")
    sm.minsize(280,140)
    sm.resizable(FALSE,FALSE)
    global autojoin
    autojoin_enabled = IntVar()
    autojoin_enabled.set(autojoin)
    Checkbutton(sm, text="Enable autojoin", variable=autojoin_enabled).grid(row=1, sticky=W,padx=20)
    button = Button(sm, text='Done', width=20,
                    command=lambda: {change_other_settings(autojoin_enabled.get()),
                                                           sm.destroy()})
    button.grid(row=4, padx=60,pady=10)

    
def find_2name(text,name):
    text2 = text[:15]
    b = text2.find(name)
    if b is not -1:
        return False
    name = name[:-1]
    text = text[15:]
    text = text.lower()
    b = text.find(name.lower())
    if b is not -1:
        if sound_settings[2] == 1:
            play_sound('beep1.wav',False)
        return True
    else:
        return False
    
    
def About():
    print 'about'



## Loading from settings file
### 0all_sound, 1entry, 2user textbox
sound_settings = [1,1,1]
sound_settings[0] = int(read_settings('enable_sound='))
sound_settings[1] = int(read_settings('entry_enabled='))
sound_settings[2] = int(read_settings('user_textbox='))
dsound_interval = float(6.0)
dsound_interval=float(read_settings('sound_interval='))
try:
    username = str(read_settings('username='))
    if username == 'default':
        username = 'User'+str(randrange(1,999,1))
except:
    print "Couldn't load username"
    username = 'User'+str(randrange(1,999,1))
autojoin = 0
autojoin = int(read_settings('autojoin='))
## Setting global vars
sound_interval = 0
action_time = True
data_list = []
msg_recv = 0

## Tkinter below
root = Tk()
root.title("iSPTC - "+username)
root.minsize(300,300)
root.geometry("1000x700")
maxsize = "5x5"
textt = StringVar()
textt.set("")
###Toolbar
menu = Menu(root,tearoff=0)
root.config(menu=menu)
menu1 = Menu(menu,tearoff=0)
menu.add_cascade(label='Main',menu=menu1)
menu1.add_command(label='Join', command=join_typing)
menu1.add_command(label='Join last', command=lambda: join_server(False))
menu1.add_command(label='Leave', command=leave_server)
menu1.add_command(label='Quit', command=closewin)

menu2 = Menu(menu,tearoff=0)
menu.add_cascade(label='Settings',menu=menu2)
menu2.add_command(label='Set username', command=set_username)
menu2.add_command(label='Sound options', command=sound_menu)
menu2.add_command(label='Other options', command=other_menu)

helpmenu = Menu(menu,tearoff=0)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About..', command=About)

### Window widgets
E = Entry(textvariable=textt)
User_area = Text(root, height=44, width=20)
S = Scrollbar(root, width=15)
S2 = Scrollbar(root, width=15)
T = Text(root, height=46, width=114)
S.pack(side=RIGHT, fill=Y)
User_area.pack(side=LEFT,fill=Y)
S2.pack(side=LEFT, fill=Y)
E.pack(side=BOTTOM,fill=BOTH)
T.pack(side=BOTTOM,fill=BOTH,expand=1)
S.config(command=T.yview)
S2.config(command=User_area.yview)
User_area.config(yscrollcommand=S2.set,state="normal")
User_area.bind( '<Configure>', maxsize )
T.config(yscrollcommand=S.set,state="disabled")
##T.bind( '<Configure>', maxsize )
T.tag_configure('redcol', foreground='red')
T.tag_configure('bluecol', foreground='blue')
T.tag_configure('greencol', foreground='green')
T.tag_configure('purplecol', foreground='purple')
User_area.tag_configure('purplecol', foreground='purple')

def prindata(aa):
    print data_list
root.bind('<Return>', enter_text)
root.bind('<Escape>',prindata)

def task():
    global msg_recv,sound_interval,dsound_interval,username
    dtime = get_cur_time()
    if sound_interval > 0:
        sound_interval-=0.25
        

    if msg_recv < len(data_list):
        for x in range(msg_recv,len(data_list)):
            if data_list[x][:9] == 'SSERVER::':
                T.config(yscrollcommand=S.set,state="normal")
                T.insert(END, dtime+'          SERVER: '+data_list[x][9:],'bluecol')
                scroller = S.get()
                if scroller[1] == 1.0:  
                    T.yview(END)
                T.config(yscrollcommand=S.set,state="disabled")
            elif data_list[x][:9] == 'CLOSING::':
                T.config(yscrollcommand=S.set,state="normal")
                T.insert(END, get_cur_time()+'         WARNING: Server shutting down\n', 'redcol')
                leave_server()
                T.config(yscrollcommand=S.set,state="disabled")
            elif data_list[x][:9] == 'USRLIST::':
                User_area.config(yscrollcommand=S.set,state="normal")
                User_area.delete(1.0,END)
                User_area.insert(END, data_list[x][9:])
                User_area.config(yscrollcommand=S.set,state="disabled")
            else:
                T.config(yscrollcommand=S.set,state="normal")
                nfind = find_2name(data_list[x],username)
                if nfind is True:
                    T.insert(END, dtime+' '+data_list[x],'greencol')
                else:
                    T.insert(END, dtime+' '+data_list[x],)
                nfind = False
                scroller = S.get()
                if scroller[1] == 1.0:  
                    T.yview(END)
                T.config(yscrollcommand=S.set,state="disabled")
            msg_recv +=1
    root.after(250, task)  # reschedule event in 0.5 second



te = Test(root)
set_winicon(root,'icon')

root.protocol('WM_DELETE_WINDOW', closewin)
root.after(250, task)
if autojoin == 1:
    join_server(False)
root.mainloop()

