#!/usr/bin/env python
from Tkinter import *
from threading import Thread
from random import randrange
from time import strftime,gmtime,sleep
import socket,os,platform
sys_path = os.getcwd()
bat_file = False
try:
    argv = sys.argv[1]
    b = argv.find('bat_file')
    if b is not -1:
        sys_path+="\\iSPTC\\"
        sys_path = str(sys_path)
        bat_file=True
except:
    pass
OS = platform.system()
print sys_path
if OS is 'Windows':
    import winsound
    
ver = '0.81'

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
    global bat_file, sys_path
    if bat_file is True:
        a = readf(sys_path+'load/settings')
    else:
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
    global bat_file, sys_path
    if bat_file is True:
        a = readf(sys_path+'load/settings')
        a = edit_settings(a,text_find,new_value)
        text = a = '\n'.join(str(e) for e in a)
        savef(text,sys_path+'load/settings')
    else:
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

class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

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
    if len(text) > 0:
        if text[0] is '@':
            b = text.find(' ')
            if b is not -1:
                textt.set(text[:b]+" ")
            else:
                textt.set(text+" ")
        else:
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
    if len(new_name) <3:
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, get_cur_time()+'         WARNING: Name is too short\n', 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")
    else:
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
    
def change_sound_set(a,b,c,d):
    global dsound_interval
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
    set_winicon(sw,'icon')
    sw.title("Sound options")
    sw.minsize(280,180)
    sw.resizable(FALSE,FALSE)
    ### 0all_sound, 1entry, 2user textbox
    sound_enabled = IntVar()
    entry_enabled = IntVar()
    user_textbox = IntVar()
    snd_interval = IntVar()
    sound_enabled.set(sound_settings[0])
    entry_enabled.set(sound_settings[1])
    user_textbox.set(sound_settings[2])
    Checkbutton(sw, text="Enable sound", variable=sound_enabled).grid(row=1, sticky=W,padx=20)
    Checkbutton(sw, text="Entry sound", variable=entry_enabled).grid(row=2, sticky=W,padx=20)
    Checkbutton(sw, text="Textbox sound", variable=user_textbox).grid(row=3, sticky=W,padx=20)
    snd_interval = Scale(sw, from_=0, to=30,length=120, orient=HORIZONTAL)
    Label(sw, text="Sound min interval").grid(row=1,padx=160)
    snd_interval.grid(row=2,padx=160)
    snd_interval.set(int(dsound_interval))
    button = Button(sw, text='Done', width=20,command=lambda: {change_sound_set(sound_enabled.get(),entry_enabled.get(),user_textbox.get(),snd_interval.get()),sw.destroy()})
    button.grid(row=6, padx=60,pady=30)

def change_other_settings(a,b,c,d):
    global task_loop_interval,autojoin, leave_join, usr_symbolmatch
    autojoin = a
    task_loop_interval = b
    leave_join = c
    usr_symbolmatch = d
    write_settings('autojoin',a)
    write_settings('chat_interval',b)
    write_settings('leave_join',c)
    write_settings('symbol_match',d)
    
def other_menu():
    global task_loop_interval, autojoin, leave_join, usr_symbolmatch
    sm = Toplevel()
    set_winicon(sm,'icon')
    sm.title("Other options")
    sm.minsize(280,140)
    sm.resizable(FALSE,FALSE)
    leave_join_enabled = IntVar()
    autojoin_enabled = IntVar()
    task_int = IntVar()
    symbolmatch = IntVar()
    autojoin_enabled.set(autojoin)
    leave_join_enabled.set(leave_join)
    Checkbutton(sm, text="Show leave and join", variable=leave_join_enabled).pack(side=TOP)
    Checkbutton(sm, text="Enable autojoin", variable=autojoin_enabled).pack(side=TOP)
    task_int = Scale(sm, from_=0, to=800,length=160, orient=HORIZONTAL)
    symbolmatch = Scale(sm, from_=-3, to=0,length=160, orient=HORIZONTAL)
    Label(sm, text="Chat refresh ms").pack(side=TOP)
    task_int.pack(side=TOP)
    Label(sm, text="Textbox match user name 0=all").pack(side=TOP)
    task_int.set(task_loop_interval)
    symbolmatch.set(usr_symbolmatch)
    symbolmatch.pack(side=TOP)
    button = Button(sm, text='Done', width=20,
                    command=lambda: {change_other_settings(autojoin_enabled.get(),task_int.get(),
                                                           leave_join_enabled.get(),symbolmatch.get())
                                                           ,sm.destroy()})
    button.pack(side=BOTTOM)

    
def find_2name(text,name):
    global usr_symbolmatch
    text2 = text[:15]
    b = text2.find(name)
    if b is not -1:
        return False
    name = name[:usr_symbolmatch]
    text = text[15:]
    text = text.lower()
    b = text.find(name.lower())
    if b is not -1:
        if sound_settings[2] == 1:
            play_sound('beep1.wav',False)
        return True
    else:
        return False

def reset_entry(var):
    textt.set('')

def reset_textbox(var):
    T.set('')

def organise_USRLIST(data):
    USRLIST = []
    temp_list = []
    while True:
        begn = data.find('[[')
        end = data.find(']]')
        if begn is -1 or end is -1:
            break
        temp_list.append(data[begn+2:end+1])
        data = data[end+2:]
    cnt = 0
    for x in temp_list:
        USRLIST.append([])
    for x in temp_list:
        while True:
            begn = x.find('[')+1
            end = x.find(']')
            if begn is -1 or end is -1:
                break
            USRLIST[cnt].append(x[begn:end])
            x = x[end+1:]
        cnt+=1
    print 'USRLISTE:',USRLIST

    User_area.config(yscrollcommand=S.set,state="normal")
    User_area.delete(1.0,END)
    for x in USRLIST:
        if x[1] == '2':
            User_area.insert(END, x[0]+'\n','purplecol')
        elif x[1] == '999':
            User_area.insert(END, x[0]+'\n','pinkcol')
        elif x[1] == '-1':
            User_area.insert(END, x[0]+'\n','greycol')
        else:
            User_area.insert(END, x[0]+'\n')
    User_area.config(yscrollcommand=S.set,state="disabled")

def add_spaces(name):
    for x in name:
        while len(name) < 15:
            name = ' '+name
    return name

def get_user_color(col,name):
    dtime = get_cur_time()
    name = add_spaces(name)
    if col == '1':
        return 'black',name
    elif col == '2':
        return 'purplecol',name
    elif col == '9':
        return 'pinkcol', name
    return '0','0'

      
def About():
    print 'about'



## Loading from settings file
### 0all_sound, 1entry, 2user textbox
sound_settings = [1,1,1]
task_loop_interval = int(500)
task_loop_interval = int(read_settings('chat_interval='))
sound_settings[0] = int(read_settings('enable_sound='))
sound_settings[1] = int(read_settings('entry_enabled='))
sound_settings[2] = int(read_settings('user_textbox='))
dsound_interval = float(6.0)
dsound_interval=float(read_settings('sound_interval='))
leave_join = 1
leave_join = int(read_settings('leave_join='))
usr_symbolmatch = 0
usr_symbolmatch = int(read_settings('symbol_match='))
try:
    username = str(read_settings('username='))
    if username == 'default':
        username = 'User'+str(randrange(1,999,1))
    elif len(username) < 3:
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
##menu1.add_command(label='Test', command=lambda: s.send('USRINFO::user'))

menu2 = Menu(menu,tearoff=0)
menu.add_cascade(label='Edit',menu=menu2)
menu2.add_command(label='Clear textbox', command=reset_textbox)
menu2.add_command(label='Clear Entry box', command=reset_entry)

menu3 = Menu(menu,tearoff=0)
menu.add_cascade(label='Settings',menu=menu3)
menu3.add_command(label='Set username', command=set_username)
menu3.add_command(label='Sound options', command=sound_menu)
menu3.add_command(label='Other options', command=other_menu)


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
T.tag_configure('pinkcol', foreground='pink')
User_area.tag_configure('purplecol', foreground='purple')
User_area.tag_configure('greycol', foreground='grey')
User_area.tag_configure('pinkcol', foreground='pink')



root.bind('<Return>', enter_text)
root.bind('<Escape>', reset_entry)

def task():
    global msg_recv,sound_interval,dsound_interval,username, task_loop_interval, leave_join
    dtime = get_cur_time()
    if sound_interval > 0:
        sound_interval-=float(task_loop_interval)/1000
        

    if msg_recv < len(data_list):
        for x in range(msg_recv,len(data_list)):
            print data_list[x]
            if data_list[x][:9] == 'SSERVER::':
                T.config(yscrollcommand=S.set,state="normal")
                T.insert(END, dtime+'          SERVER: '+data_list[x][9:],'bluecol')
                scroller = S.get()
                if scroller[1] == 1.0:  
                    T.yview(END)
                T.config(yscrollcommand=S.set,state="disabled")
            elif data_list[x][:9] == 'SERVELJ::':
                if leave_join == 0:
                    doing = 'nothing'
                else:
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
                organise_USRLIST(data_list[x][9:])
            else:
                T.config(yscrollcommand=S.set,state="normal")
                nfind = find_2name(data_list[x][4:],username)
                usercol,uname = get_user_color(data_list[x][3],data_list[x][4:19])
                if nfind is True:
                    T.insert(END, dtime+' '+uname+': ',usercol)
                    T.insert(END, dtime+' '+data_list[x][19:],'greencol')
                else:
                    T.insert(END, dtime+' '+uname+': ',usercol)
                    T.insert(END, data_list[x][19:])                        
                nfind = False
                scroller = S.get()
                if scroller[1] == 1.0:  
                    T.yview(END)
                T.config(yscrollcommand=S.set,state="disabled")
            msg_recv +=1
    root.after(task_loop_interval, task)  # reschedule event in 0.5 second

hyperlink = HyperlinkManager(T)

te = Test(root)
set_winicon(root,'icon')

root.protocol('WM_DELETE_WINDOW', closewin)
root.after(task_loop_interval, task)
if autojoin == 1:
    join_server(False)
root.mainloop()

