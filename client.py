#!/usr/bin/env python
from Tkinter import *
from threading import Thread
from random import randrange
from time import strftime,gmtime,sleep
import socket,os,platform,webbrowser
import tkFont
ver = '0.95'

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
        a = readf(sys_path+'load/settings.cfg')
    else:
        a = readf('load/settings.cfg')
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
        a = readf(sys_path+'load/settings.cfg')
        a = edit_settings(a,text_find,new_value)
        text = a = '\n'.join(str(e) for e in a)
        savef(text,sys_path+'load/settings.cfg')
    else:
        a = readf('load/settings.cfg')
        a = edit_settings(a,text_find,new_value)
        text = a = '\n'.join(str(e) for e in a)
        savef(text,'load/settings.cfg')

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

linkk = 'aa'
linklist = []

class HyperlinkManager:
    def __init__(self, text):
        global linkk, font_size, text_font
        font = text_font
        fontlist=list(tkFont.families())
        fontlist.sort()
        self.text = text
        self.text.tag_config("hyper", font=(fontlist[text_font[0]], font_size), foreground='blue', underline=1)
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
        self.linksss = linkk
        linklist.append([tag,linkk])
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                for x in linklist:
                    if x[0] == tag:
                        print x[1]
                        webbrowser.open(x[1])
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

def lenghten_name(name,symbols):
    global nadd_spaces
    if nadd_spaces is 1:
        while len(name) < symbols:
            name = " " + name
    return name
    
def closewin():
    global s, action_time
    print 'Goodbye'
    action_time = False
    try:
        s.send('close::')
        sleep(0.3)
        s.close()
        root.destroy()
    except:
        sleep(0.3)
        root.destroy()

def get_cur_time():
    global show_ttime
    if show_ttime is 1:
        return ''
    if show_ttime is 2:
        return strftime("%H:%M")
    if show_ttime is 3:
        return strftime("%H:%M:%S")

def cp_destroy(*arg):
    global cp_is
    bb1.destroy()
    bb2.destroy()
    bb3.destroy()
    bb4.destroy()
    cp_is = False

def open_in_browser_btn():
    try:
        clipboardData = root.selection_get(selection="CLIPBOARD")
        done = True
    except:
        done = False
    try:
        copy_text()
        webbrowser.open(str(root.selection_get(selection="CLIPBOARD")))
    except:
        print 'Nothing in clipboard'
    if done == True:
        E.clipboard_clear()
        E.clipboard_append(clipboardData)    
    
def copy_paste_buttons(*arg):
    global bb2, bb1, bb3, bb4, cp_is, m_x, m_y
    if cp_is == False:
        bb1 = Button(root, text='Open in browser', width=50,
                        command=lambda: {open_in_browser_btn(),cp_destroy()})
        bb1.place(x=m_x, y=m_y,width=120, height=26)
        bb2 = Button(root, text='Clear entry', width=50,
                        command=lambda: {textt.set(''),cp_destroy()})
        bb2.place(x=m_x, y=m_y+26,width=120, height=26)   
        bb3 = Button(root, text='Copy', width=50,
                        command=lambda: {copy_text(),cp_destroy()})
        bb3.place(x=m_x, y=m_y+52,width=120, height=26)
        bb4 = Button(root, text='Paste', width=50,
                        command=lambda: {entry_paste(),cp_destroy()})
        bb4.place(x=m_x, y=m_y+78,width=120, height=26)
        cp_is = True
    else:
        cp_destroy()

def recv_thread():
    global action_time, s
    while action_time is True:
        data = s.recv(2048)
        if not data:
            if action_time is True:
                T.config(yscrollcommand=S.set,state="normal")
                war = lenghten_name('WARNING: ',21)
                T.insert(END, get_cur_time()+war+'Connection lost\n', 'redcol')
                T.config(yscrollcommand=S.set,state="disabled")
            break
        data_list.append(data+'\n')
        
def join_typing():
    global server_list
    server_list = []
    temp_text = readf('load/serverlist')
    for x in temp_text:
        server_list.append(x)
    joinaddr = str(read_settings('joinaddr='))
    jaddr = StringVar()
    jaddr.set(joinaddr)
    jsrv = Toplevel()
    set_winicon(jsrv,'icon')
    jsrv.title("Server address")
    jsrv.minsize(320,360)
    jsrv.resizable(FALSE,FALSE)

    frame = Frame(jsrv, height=260,width=300, relief=SUNKEN)
    frame.pack_propagate(0)
    frame.pack(padx=10,pady=10,anchor=NE,side=TOP)

    Label(frame, text="Select from list:").pack(anchor=NW)
    display = Listbox(frame)
    scroll = Scrollbar(frame)
    scroll.pack(side=RIGHT, fill=Y, expand=NO)
    display.pack(fill=BOTH, expand=YES, side=TOP)
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)
    for item in server_list:
        display.insert(END, item)

    Label(jsrv, text="Or type manually:").pack(side=TOP)
    usrEntry = Entry(jsrv,textvariable=jaddr)
    usrEntry.pack(side=TOP,pady=10,)
    usrEntry.focus_set()
    button = Button(jsrv, text='Join',pady=10, width=10,height=1, command=lambda: {join_srv_check(display.curselection(),jaddr.get()),
                                                                jsrv.destroy()})
    button.pack(side=TOP)
    def cmdbind(*arg):
        join_srv_check(display.curselection(),jaddr.get())
        jsrv.destroy()
    jsrv.bind('<Return>', cmdbind)

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
    global username, s, action_time, passwd, autoauth, offline_msg
    try:
        action_time = False
        s.send('close::')
        sleep(0.3)
        s.close()
    except:
        pass
    try:
        if typing is not False:
            TCP_IP = typing
            TCP_PORT = 44671
            write_settings('joinaddr',TCP_IP) 
        else:
            joinaddr = str(read_settings('joinaddr='))
            TCP_IP = joinaddr
            TCP_PORT = 44671
        BUFFER_SIZE = 2048
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'joining',TCP_IP, TCP_PORT
        s.connect((TCP_IP, TCP_PORT))
        action_time = True
        Thread(target=recv_thread).start()
        sleep(0.3)
        if passwd is '' or autoauth is 0:
            s.send('USRINFO::'+username)
        else:
            s.send('USRINFO::'+username+']'+passwd)
        sleep(0.2)
        s.send('CONFIGR::offmsg='+str(offline_msg))
    except:
        T.config(yscrollcommand=S.set,state="normal")
        war = lenghten_name('WARNING: ',21)
        T.insert(END, get_cur_time()+war+"Can't join\n", 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")

def scroller_to_end():
    scroller = S.get()
    if scroller[1] == 1.0:  
        T.yview(END)

def T_ins_userlist():
    global USRLIST
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, '[Userlist]\n', 'browncol')
    T.insert(END, '[Name] [IP] [Level] [AFK]\n', 'browncol')
    for x in USRLIST:
        T.insert(END, x[0]+', '+x[1]+', '+x[2]+', '+x[3]+'\n', 'black')
    T.config(yscrollcommand=S.set,state="disabled")
    scroller_to_end()

def T_ins_help():
    global USRLIST
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, '[Help]\n', 'browncol')
    T.insert(END, 'Type:\n/users for userlist\n/log for chatlog\n/afk to go afk\n/ll to see all links\n'+
             '/register [passwd] to register\n/auth [passwd] to authenticate\n', 'blackcol')
    T.config(yscrollcommand=S.set,state="disabled")
    scroller_to_end()

def T_ins_log():
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, '[Log]\n', 'browncol')
    for x in data_list:
        T.insert(END, x,'blackcol')
    T.config(yscrollcommand=S.set,state="disabled")
    scroller_to_end()
    
def T_ins_linklist():
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, '[Link list]\n', 'browncol')
    for x in linklist:
        T.insert(END, x[1]+'\n','bluecol')
    T.config(yscrollcommand=S.set,state="disabled")
    scroller_to_end()

def send_afk():
    try:
        s.send('aAFKAFK::')
    except:
        pass

def attempt_registration(s,authps):
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
    
def t_auth_window(auth_or_register):
    global passwd
    try:
        hhw.destroy()
    except:
        pass
    t_passwd = StringVar()
    t_passwd.set(passwd)
    hhw = Toplevel()
    set_winicon(hhw,'icon')
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
    
    button = Button(hhw, text='Auth', width=20, command=lambda: {auth_register(auth_or_register,t_passwd),
                                                                hhw.destroy()})
    button.pack(side=BOTTOM,pady=10)
    def cmdbind(*arg):
        auth_register(auth_or_register,t_passwd)
        hhw.destroy()
    hhw.bind('<Return>', cmdbind)

def enter_text(event):
    global s, USRLIST
##    T.config(yscrollcommand=S.set,state="normal")
##    T.config(yscrollcommand=S.set,state="disabled")
    text = textt.get()
    if len(text) > 0:
        if text[0] == '/':
            if text == '/users':
                T_ins_userlist()
            elif text == '/help':
                T_ins_help()
            elif text == '/log':
                T_ins_log()
            elif text == '/afk':
                send_afk()
            elif text == '/ll':
                T_ins_linklist()
            elif text[:10] == '/register ' and len(text) > 11:
                attempt_registration(s,text[10:])
            elif text[:6] == '/auth ' and len(text) > 7:
                attempt_auth(s,text[6:])
            textt.set('')
        else:
            if text[0] is '@':
                b = text.find(' ')
                if text[1] is '@':
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
            try:
                s.send('MESSAGE::'+text)
            except Exception as ee:
                T.config(yscrollcommand=S.set,state="normal")
                war = lenghten_name('WARNING: ',21)
                T.insert(END, get_cur_time()+war+str(ee)+'\n', 'redcol')
                T.config(yscrollcommand=S.set,state="disabled")
    T.yview(END)

def leave_server():
    global s,action_time
    war = lenghten_name('WARNING: ',21)
    try:
        s.send('close::')
        action_time = False
        sleep(0.4)
        s.close()
        s = ''
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, get_cur_time()+war+'Left server\n', 'redcol')
        T.config(yscrollcommand=S.set,state="disabled")
        User_area.config(yscrollcommand=S.set,state="normal")
        User_area.delete(1.0,END)
        User_area.config(yscrollcommand=S.set,state="disabled")
    except:
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, get_cur_time()+war+'\n', 'redcol')
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
                    s.send('USRINFO::'+username)
                else:
                    s.send('USRINFO::'+username+']'+passwd)
            except:
                pass
        
    new_offline_msg = t_offline_msg.get()
    if new_offline_msg != offline_msg:
        offline_msg = new_offline_msg
        write_settings('offline_msg',offline_msg)
        sleep(0.2)
        try:
            s.send('CONFIGR::offmsg='+str(offline_msg))
        except:
            pass

def set_username():
    global username, passwd, offline_msg
    uw = Toplevel()
    t_new_name = StringVar()
    t_new_name.set(username)
    t_passwd = StringVar()
    t_passwd.set(passwd)
    t_offline_msg = IntVar()
    t_offline_msg.set(offline_msg)
    set_winicon(uw,'icon')
    uw.title("User")
    uw.minsize(250,170)
    uw.resizable(FALSE,FALSE)
    
    Label(uw, text="Username:").pack(anchor=NW,padx=35,pady=5)
    usrEntry = Entry(uw,textvariable=t_new_name)
    usrEntry.pack(pady=5)
    usrEntry.focus_set()

    Label(uw, text="Pass (leave blank, if unused):").pack(anchor=NW,padx=35)
    usrEntry = Entry(uw,textvariable=t_passwd)
    usrEntry.pack(pady=5)
    usrEntry.focus_set()
    Checkbutton(uw, text="Enable offline messages", variable=t_offline_msg).pack(anchor=NW,padx=35)
    button = Button(uw, text='Save', width=20, command=lambda: {change_name(t_new_name,t_passwd,
                                                                            t_offline_msg),
                                                                uw.destroy()})
    button.pack(side=BOTTOM,pady=10)
    def cmdbind(*arg):
        change_name(t_new_name,t_passwd,t_offline_msg)
        uw.destroy()
    uw.bind('<Return>', cmdbind)
    
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
    button = Button(sw, text='Save', width=20,command=lambda: {change_sound_set(sound_enabled.get(),entry_enabled.get(),user_textbox.get(),snd_interval.get()),sw.destroy()})
    button.grid(row=6, padx=60,pady=30)

def set_font(font,fontlist,t_font_size):
    global T,E,User_area, text_font, font_size
    global font_size, text_font
    if font is not ():
        text_font = font
        write_settings('tfont',text_font[0])
    try:
        font_size = t_font_size
    except:
        pass
    tag_colors()
    hyperlink = HyperlinkManager(T)
    write_settings('font_size',font_size)
    
def font_menu():
    global font_size, text_font
    fom = Toplevel()
    set_winicon(fom,'icon')
    fom.title("Font options")
    fom.minsize(700,400)
    fom.resizable(FALSE,FALSE)

    frame = Frame(fom, height=380,width=300, relief=SUNKEN)
    frame2 = Frame(fom, height=400,width=400, relief=SUNKEN)
    frame.pack_propagate(0)
    frame2.pack_propagate(0)
    frame.pack(anchor=NE,side=LEFT)
    frame2.pack(anchor=NE,side=LEFT)
    
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

    t_font_size = IntVar()
    t_font_size.set(font_size)
    Label(frame2, text="Font size:",justify = LEFT).place(x=20,y=300)
    Efont_size = Entry(frame2,textvariable=t_font_size,width=3).place(x=100,y=300)
    display_text = Text(frame2, height=12, width=50,wrap=WORD)
    display_text.place(x=20,y=80)
    display_text.insert(END, get_cur_time()+' SERVER: Hello human\n','bluecol')
    display_text.insert(END, get_cur_time()+' WARNING: Hello human\n','redcol')
    display_text.insert(END, get_cur_time()+' Human: Hello\n','greencol')
    display_text.insert(END, get_cur_time()+' SERVER: human is afk\n','greycol')
    display_text.insert(END, get_cur_time()+' Admin: /kick human\n','purplecol')
    display_text.insert(END, get_cur_time()+' Cat: hello ','blackcol')       

    button2 = Button(frame2, text='Apply', width=12,
                    command=lambda: {apply_display_font(display_text,display.curselection(),fonts,
                                                        t_font_size.get())})
    button = Button(frame2, text='Save', width=12,
                    command=lambda: {set_font(display.curselection(),fonts,
                                                        t_font_size.get()),
                                     fom.destroy()})
    button.place(x=200,y=360)
    button2.place(x=40,y=360)
    apply_display_font(display_text,text_font,fonts,font_size)

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
    display_text.tag_configure('greencol', font=(fontlist[text_font[0]], font_size), foreground='green')
    display_text.tag_configure('purplecol', font=(fontlist[text_font[0]], font_size), foreground='purple')
    display_text.tag_configure('greycol', font=(fontlist[text_font[0]], font_size), foreground='grey')
    display_text.tag_configure('blackcol', font=(fontlist[text_font[0]], font_size), foreground='black')

def change_other_settings(a,b,c,d,e,f,g,h):
    global X_size,Y_size ,autojoin, leave_join, nadd_spaces, show_ttime, hide_users
    global User_area, S2, T, S, E, s, username
    autojoin = a
    X_size = b
    leave_join = c
    Y_size = d
    nadd_spaces = e
    autoauth = h

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
    if f is not 0:
        show_ttime = f
        write_settings('show_ttime',f)
    write_settings('autojoin',a)
    write_settings('X_size',b)
    write_settings('leave_join',c)
    write_settings('Y_size',d)
    write_settings('nadd_spaces',e)
    write_settings('hide_users',g)
    write_settings('autoauth',h)
    root.geometry('%sx%s' % (X_size,Y_size))
    
    
def other_menu():
    global X_size,Y_size , autojoin, leave_join, nadd_spaces, show_ttime, hide_users, autoauth
    sm = Toplevel()
    set_winicon(sm,'icon')
    sm.title("Other options")
    sm.minsize(500,200)
    sm.resizable(FALSE,FALSE)
    frame = Frame(sm, height=210,width=210, relief=SUNKEN)
    frame2 = Frame(sm, height=180,width=220, relief=SUNKEN)
    frame.pack_propagate(0)
    frame2.pack_propagate(0)
    frame.pack(anchor=NE,side=LEFT)
    frame2.pack(anchor=NE,side=LEFT)
    
    leave_join_enabled = IntVar()
    autoauth_enabled = IntVar()
    autojoin_enabled = IntVar()
    t_X_size = IntVar()
    t_Y_size = IntVar()
    autojoin_enabled.set(autojoin)
    autoauth_enabled.set(autoauth)
    leave_join_enabled.set(leave_join)
    Checkbutton(frame, text="Show leave and join", variable=leave_join_enabled).pack(anchor=NW)
    Checkbutton(frame, text="Enable autoauthentication", variable=autoauth_enabled).pack(anchor=NW)
    Checkbutton(frame, text="Enable autojoin", variable=autojoin_enabled).pack(anchor=NW)
    t_X_size = Scale(frame, from_=300, to=2000,length=160, orient=HORIZONTAL)
    t_Y_size = Scale(frame, from_=300, to=1600,length=160, orient=HORIZONTAL)
    Label(frame, text="X_size").pack(side=TOP)
    t_X_size.pack(side=TOP)
    Label(frame, text="Y_size").pack(side=TOP)
    t_X_size.set(X_size)
    t_Y_size.set(Y_size)
    t_Y_size.pack(side=TOP)
    
    lenchspaces = IntVar()
    t_hide_users = IntVar()
    lenchspaces.set(nadd_spaces)
    t_hide_users.set(hide_users)
    Checkbutton(frame2, text="Hide userbox", variable=t_hide_users).pack(anchor=NW)
    Checkbutton(frame2, text="Lenghten usernames to 15", variable=lenchspaces).pack(anchor=NW)
    t_box_time = IntVar()
    t_box_time.set = (show_ttime)
    Label(frame2, text="Textbox time:",justify = LEFT).pack(anchor=NW)
    Radiobutton(frame2,text="Show full",variable=t_box_time,value=3).pack(anchor=NW)
    Radiobutton(frame2,text="Without seconds",variable=t_box_time,value=2).pack(anchor=NW)
    Radiobutton(frame2,text="Hide",variable=t_box_time,value=1).pack(anchor=NW)
    t_box_time.set = (show_ttime)
    button = Button(frame2, text='Save', width=20,
                    command=lambda: {change_other_settings(autojoin_enabled.get(),t_X_size.get(),
                                                           leave_join_enabled.get(),t_Y_size.get(),
                                                           lenchspaces.get(),t_box_time.get(),
                                                           t_hide_users.get(),autoauth_enabled.get())
                                                           ,sm.destroy()})
    button.pack(side=BOTTOM)

    
def find_2name(text,name):
    global username
    text = text.lower()
    name = name.lower()
    b = text.find(name)
    if b is not -1:
        if sound_settings[2] == 1:
            play_sound('beep1.wav',False)
        return True
    else:
        return False

def reset_entry(var):
    global cp_is, bb1, bb2
    if cp_is == True:
        bb1.destroy()
        bb2.destroy()
        cp_is = False
    else:
        textt.set('')

def reset_textbox():
    T.config(yscrollcommand=S.set,state="normal")
    T.delete(1.0,END)
    T.config(yscrollcommand=S.set,state="disabled")

def organise_USRLIST(data):
    global USRLIST, hide_users
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
    cnt = 0
    for x in USRLIST:
        if x[0][:6] == 'Users:' and x[1] == '':
            usercount = x
            USRLIST.pop(cnt)
            break
        cnt+=1
    USRLIST.sort()
    templist = [usercount]
    for x in USRLIST:
        templist.append(x)
    USRLIST = list(templist)
    print 'USRLIST received'
    if hide_users == 0:
        user_area_insert()

def user_area_insert():
    global USRLIST
    User_area.config(yscrollcommand=S2.set,state="normal")
    User_area.delete(1.0,END)
    for x in USRLIST:
        try:
            usercol = get_user_color(x[2],x[0],False)
            ##AFK color
            if x[1] == 'Offline':
                User_area.insert(END, x[0]+'\n','offcol')               
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
        return 'pinkcol',name
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
    data = data + ' '
    begn = data.find('http://')
    linktext = ''
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
    if begn is not -1:
        while True:
            if data[begn] is not ' ':
                linktext = linktext+data[begn]
                begn+=1
            else:
                return 'http://'+linktext
    return False

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

def motion(event):
    global m_x,m_y
    m_x, m_y = event.x, event.y

def Changelog():
    global font_size, text_font
    font = text_font
    fontlist=list(tkFont.families())
    fontlist.sort()
    topwin = Toplevel()
    set_winicon(topwin,'icon')
    topwin.title("Changelog")
    topwin.minsize(750,550)
    topwin.resizable(FALSE,FALSE)
    frame = Frame(topwin, height=510,width=730, relief=SUNKEN,bg='grey')
    frame.pack_propagate(0)
    frame.pack(side=TOP,padx=10,pady=10)
    
    Tbox = Text(frame, height=12, width=50,wrap=WORD)
    Tbox.tag_configure('blackcol', font=(fontlist[text_font[0]], font_size), foreground='black')
    S1 = Scrollbar(frame, width=15)
    S1.pack(side=RIGHT, fill=Y)
    Tbox.pack(side=BOTTOM,fill=BOTH,expand=1)
    Tbox.focus_set()
    Tbox.config(yscrollcommand=S1.set,state="normal")
    S1.config(command=Tbox.yview)

    bb1 = Button(topwin, text='Close', width=26,
                        command=lambda: {topwin.destroy()})
    
    bb1.pack(side=BOTTOM,pady=10)
    changelogfile = readf('load/changelog.txt')
    for x in changelogfile:
        Tbox.insert(END, x+'\n','blackcol')
    Tbox.config(yscrollcommand=S1.set,state="normal")
     
def About():
    global ver
    winwi = 350
    aboutwin = Toplevel()
    aboutwin.resizable(FALSE,FALSE)
    set_winicon(aboutwin,'icon')
    aboutwin.title("About..")
    aboutwin.config()
    frame = Frame(aboutwin, height=280,width=winwi, relief=SUNKEN,bg='grey')
    frame.pack_propagate(0)
    frame.pack(side=TOP)
    
    Text = ("iSPTC ver%s" % (ver))
    msg = Message(frame, text = Text,width=winwi)
    msg.config(bg='grey',fg='white',width=winwi,font=('system', 26))
    msg.pack(anchor=NW)

    Text = ("inSecure Plain Text Chat")
    msg = Message(frame, text = Text,width=winwi)
    msg.config(bg='grey',fg='white',width=winwi,font=('system', 14))
    msg.pack(anchor=NW)

    Text = (" ")
    msg = Message(frame, text = Text,width=winwi)
    msg.config(bg='grey',width=winwi,font=('system', 54))
    msg.pack(anchor=NW)

    Text = ("Github page: github.com/Bakterija")
    msg = Message(frame, text = Text,width=winwi)
    msg.config(bg='grey',fg='white',width=winwi,font=('system', 9))
    msg.pack(anchor=NW)



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
show_ttime= int(read_settings('show_ttime='))
nadd_spaces= int(read_settings('nadd_spaces='))
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
hide_users = int(read_settings('hide_users='))
X_size = int(read_settings('X_size='))
Y_size = int(read_settings('Y_size='))
font_size = int(read_settings('font_size='))
text_font = (int(read_settings('tfont=')),)
server_list = []
passwd = str(read_settings('usrauth='))
autoauth = int(read_settings('autoauth='))
offline_msg = int(read_settings('offline_msg='))

## Setting global vars
sound_interval = 0
action_time = True
data_list = []
msg_recv = 0
windowfocus = True
icon_was_switched = False
cp_is = False
cp_focus = False
## Tkinter below
root = Tk()
root.title("iSPTC - "+username)
root.minsize(300,300)
root.geometry('%sx%s' % (X_size,Y_size))
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
menu1.add_separator()
menu1.add_command(label='Leave', command=leave_server)
menu1.add_command(label='Quit', command=closewin)

menu2 = Menu(menu,tearoff=0)
menu.add_cascade(label='Edit',menu=menu2)
menu2.add_command(label='Copy', command=copy_text)
menu2.add_command(label='Paste', command=entry_paste)
menu2.add_separator()
menu2.add_command(label='Clear Text box', command=reset_textbox)
menu2.add_command(label='Clear Entry box', command=lambda: textt.set(''))


menu3 = Menu(menu,tearoff=0)
menu.add_cascade(label='Commands',menu=menu3)
menu3.add_command(label='Register', command=lambda: t_auth_window('register'))
menu3.add_command(label='Auth', command=lambda: t_auth_window('auth'))
menu3.add_separator()              
menu3.add_command(label='Go afk', command=send_afk)
menu3.add_command(label='Print userlist', command=T_ins_userlist)
menu3.add_command(label='Print log', command=T_ins_log)
menu3.add_command(label='Print link list', command=T_ins_linklist)

menu4 = Menu(menu,tearoff=0)
menu.add_cascade(label='Settings',menu=menu4)
menu4.add_command(label='Set user', command=set_username)
menu4.add_command(label='Set font', command=font_menu)
menu4.add_command(label='Sound options', command=sound_menu)
menu4.add_command(label='Other options', command=other_menu)

helpmenu = Menu(menu,tearoff=0)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='Changelog', command=Changelog)
helpmenu.add_command(label='About..', command=About)

### Window widgets
def create_widgets():
    global T,E,User_area,S,S2,hyperlink
    E = Entry(textvariable=textt)
    User_area = Text(root, height=44, width=20)
    S = Scrollbar(root, width=15)
    S2 = Scrollbar(root, width=15)
    T = Text(root, height=46, width=114,wrap=WORD)
    ## bordercolors
##root.configure(background='red')
##    widliste = [T,E,User_area, S, S2]
##    for x in widliste:
##        x.config(background='black')
##    for x in widliste:
##        x.config(highlightthickness=0)
##    for x in widliste:
##        x.config(highlightbackground='black')
##    for x in widliste:
##        x.config(bd=0)
        
    S.pack(side=RIGHT, fill=Y)
    if hide_users == 0:
        User_area.pack(side=LEFT,fill=Y)
        S2.pack(side=LEFT, fill=Y)
    E.pack(side=BOTTOM,fill=BOTH)
    T.pack(side=BOTTOM,fill=BOTH,expand=1)
    S.config(command=T.yview)
    S2.config(command=User_area.yview)
    User_area.config(yscrollcommand=S2.set,state="disabled")
    User_area.bind( '<Configure>', maxsize )
    T.config(yscrollcommand=S.set,state="disabled")
    E.focus_set()
    hyperlink = HyperlinkManager(T)
    tag_colors()

def tag_colors():
    global font_size, text_font, hide_users
    fontlist=list(tkFont.families())
    fontlist.sort()
    T.tag_configure('redcol', font=(fontlist[text_font[0]], font_size), foreground='red')
    T.tag_configure('bluecol', font=(fontlist[text_font[0]], font_size), foreground='blue')
    T.tag_configure('greencol', font=(fontlist[text_font[0]], font_size), foreground='#009900')
    T.tag_configure('purplecol', font=(fontlist[text_font[0]], font_size), foreground='purple')
    T.tag_configure('greycol', font=(fontlist[text_font[0]], font_size), foreground='grey')
    T.tag_configure('blackcol', font=(fontlist[text_font[0]], font_size), foreground='black')
    T.tag_configure('pinkcol', font=(fontlist[text_font[0]], font_size), foreground='pink')
    T.tag_configure('blue_link', font=(fontlist[text_font[0]], font_size), foreground='blue')
    T.tag_configure('timecol', font=(fontlist[text_font[0]], font_size), foreground='black')
    T.tag_configure('browncol', font=(fontlist[text_font[0]], font_size), foreground='brown')
    T.tag_configure('privatecol', font=(fontlist[text_font[0]], font_size), background='#222222',foreground='white')
    T.tag_configure('privatgreen', font=(fontlist[text_font[0]], font_size), background='#222222',foreground='#009900')
    T.tag_configure('privatlink', font=(fontlist[text_font[0]], font_size), background='#222222',foreground='blue')

    if hide_users is not 1:
        User_area.tag_configure('blackcol', font=(fontlist[text_font[0]], font_size), foreground='black')
        User_area.tag_configure('pinkcol', font=(fontlist[text_font[0]], font_size), foreground='pink')
        User_area.tag_configure('purplecol', font=(fontlist[text_font[0]], font_size), foreground='purple')
        User_area.tag_configure('greycol', font=(fontlist[text_font[0]], font_size), foreground='grey')
        User_area.tag_configure('redcol', font=(fontlist[text_font[0]], font_size), foreground='red')
        User_area.tag_configure('offcol', font=(fontlist[text_font[0]], font_size), foreground='#66CCFF')
    E.configure(font=(fontlist[text_font[0]], font_size), foreground='black')

create_widgets()

def click1():
    print "nothing"
    
root.bind('<Return>', enter_text)
root.bind('<Escape>', reset_entry)
root.bind('<FocusIn>', winf_is)
root.bind('<FocusOut>', winf_isnt)
root.bind('<Control-c>', copy_text)
root.bind('<Motion>', motion)
root.bind('<Button-3>', copy_paste_buttons)


def task():
    global msg_recv,sound_interval,dsound_interval,username, task_loop_interval, leave_join
    global show_ttime,nadd_spaces,icon_was_switched,T,E,S,S2,User_area,hyperlink
    if sound_interval > 0:
        sound_interval-=float(task_loop_interval)/1000
    if msg_recv < len(data_list):
        for x in range(msg_recv,len(data_list)):
##            print data_list[x]
            if data_list[x][:9] == 'SSERVER::':
                T.config(yscrollcommand=S.set,state="normal")
                name = lenghten_name('SERVER: ',21)
                T.insert(END, get_cur_time()+name+data_list[x][9:],'bluecol')
                scroller = S.get()
                if scroller[1] == 1.0:  
                    T.yview(END)
                T.config(yscrollcommand=S.set,state="disabled")
            elif data_list[x][:9] == 'SERVELJ::':
                if leave_join == 0:
                    doing = 'nothing'
                else:
                    T.config(yscrollcommand=S.set,state="normal")
                    name = lenghten_name('SERVER: ',21)
                    T.insert(END, get_cur_time()+name+data_list[x][9:],'bluecol')
                    scroller = S.get()
                    if scroller[1] == 1.0:  
                        T.yview(END)
                    T.config(yscrollcommand=S.set,state="disabled")
            elif data_list[x][:9] == 'CLOSING::':
                T.config(yscrollcommand=S.set,state="normal")
                war = lenghten_name('WARNING: ',21)
                T.insert(END, get_cur_time()+name+'Server shutting down\n', 'redcol')
                leave_server()
                T.config(yscrollcommand=S.set,state="disabled")
            elif data_list[x][:9] == 'USRLIST::':
                organise_USRLIST(data_list[x][9:])
            elif data_list[x][:9] == 'DUPLICT::':
                root.title("iSPTC - "+data_list[x][9:])
            else:
                global linkk
                mgreen = 'greencol'
                mblack = 'blackcol'
                mlink = 'bluecol'
                T.config(yscrollcommand=S.set,state="normal")
                nfind = find_2name(data_list[x][23:],username)
                usercol,uname = get_user_color(data_list[x][3],data_list[x][4:23],False)

                ##Separates words
                temp_list = []
                dat = data_list[x][23:]
                b = dat.find('@@')
                c = dat.find(']')
                if b is not -1 and c is not -1:
                    dat = dat[:c]+' '+dat[c+1:]
                while True:
                    b = dat.find(' ')
                    temp_list.append(dat[:b]+' ')
                    dat = dat[b+1:]
                    if b is -1:
                        break

                ## Tags words
                T.insert(END, get_cur_time(),'blackcol')
                T.insert(END, uname+': ',usercol)
                if temp_list[0][0:2] == '@@':
                    mgreen = 'privatgreen'
                    mblack = 'privatecol'
                    mlink = 'privatlink'
                for x in temp_list:
                    nfind = find_2name(x,username)
                    if nfind is True:
                        T.insert(END, x,mgreen)
                    elif nfind is False:
                        global linkk
                        linkk = find_link(x)
                        if linkk is not False:
                            T.insert(END, linkk, hyperlink.add(click1))
                            T.insert(END,' ')
                    if linkk is False and nfind is False:
                        T.insert(END, x,mblack)       
                T.insert(END,'\n')
                    
                      
                nfind = False
                scroller = S.get()
                if scroller[1] == 1.0:  
                    T.yview(END)
                T.config(yscrollcommand=S.set,state="disabled")
                if windowfocus is False:
                    set_winicon(root,'icon2')
                    icon_was_switched = True
            msg_recv +=1
    root.after(task_loop_interval, task)  # reschedule event


##te = Test(root)
set_winicon(root,'icon')

root.protocol('WM_DELETE_WINDOW', closewin)
root.after(task_loop_interval, task)
if autojoin == 1:
    join_server(False)
root.mainloop()

