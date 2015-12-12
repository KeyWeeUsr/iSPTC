#!/usr/bin/env python
from Tkinter import *
from threading import Thread
import socket,time, random

class Test(Text):
    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)
        
    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)
    
    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)


def closewin():
    global s, action_time
    print 'Good bye'
    action_time = False
    try:
        s.send('close::')
        time.sleep(1)
        s.close()
        time.sleep(1)
        root.destroy()
    except:
        time.sleep(1)
        root.destroy()

def get_cur_time():
    return time.strftime("%H:%M:%S", time.gmtime())

def recv_thread(s):
    global action_time
    while action_time is True:
        data = s.recv(1024)
        if not data:
            break
        data_list.append(data+'\n')

def connect_srv():
    global username
    TCP_IP = '127.0.0.1'
    TCP_PORT = 8001
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    Thread(target=recv_thread,args=(s,)).start()
    return s
        
def enter_text(event):
    global s
##    T.config(yscrollcommand=S.set,state="normal")
##    T.config(yscrollcommand=S.set,state="disabled")
    text = textt.get()
    textt.set('')
    if len(text) > 0:
        s.send(text)

def sclose(val):
    global s
    s.close()

def join_server():
    global s
    s = connect_srv()
    time.sleep(1)
    s.send('USRINFO::'+username)

def change_name(new_name):
    global username, s
    print username,new_name
    new_name = new_name.get()
    username = new_name
    root.title("OSOM - "+new_name)
    s.send('USRINFO::'+username)
    uw.destroy()
    
def set_username():
    new_name = StringVar()
    new_name.set("")
    uw = Toplevel()
    uw.title("New name")
    uw.minsize(250,100)
    usrEntry = Entry(uw,textvariable=new_name)
    usrEntry.pack(pady=25)
    button = Button(uw, text='Done', width=20, command=lambda: change_name(new_name))
    button.pack()
    
    
def About():
    print 'about'

action_time = True
data_list = []
msg_recv = 0
username = 'User'+str(random.randrange(1,999,1))
print 'username is: ',username
root = Tk()
root.title("iSPTC - "+username)
root.minsize(300,300)
root.geometry("1000x700")
maxsize = "5x5"
textt = StringVar()
textt.set("")

menu = Menu(root)
root.config(menu=menu)
menu1 = Menu(menu)
menu.add_cascade(label='Menu',menu=menu1)
menu1.add_command(label='Join', command=join_server)
menu1.add_command(label='Set username', command=set_username)
menu1.add_command(label='Quit', command=closewin)

helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About..', command=About)

E = Entry(textvariable=textt)
E.pack(side=BOTTOM,fill=BOTH)
User_area = Text(root, height=44, width=20)
S = Scrollbar(root, width=15)
S2 = Scrollbar(root, width=15)
T = Text(root, height=46, width=114)
S.pack(side=RIGHT, fill=Y)
User_area.pack(side=LEFT,fill=Y)
S2.pack(side=LEFT, fill=Y)
T.pack(side=BOTTOM,fill=BOTH,expand=1)
S.config(command=T.yview)
S2.config(command=User_area.yview)
User_area.config(yscrollcommand=S2.set,state="normal")
User_area.bind( '<Configure>', maxsize )
T.config(yscrollcommand=S.set,state="normal")
##T.bind( '<Configure>', maxsize )
T.tag_configure('redcol', foreground='red')

root.bind('<Return>', enter_text)
##root.bind('<Escape>', sclose)

def task():
    global msg_recv
    dtime = get_cur_time()
    if msg_recv < len(data_list):
        for x in range(msg_recv,len(data_list)):
            if data_list[x][:9] == 'SSERVER::':
                T.config(yscrollcommand=S.set,state="normal")
                T.insert(END, dtime+'          SERVER: '+data_list[x][9:],'redcol')
                scroller = S.get()
                if scroller[1] == 1.0:  
                    T.yview(END)
                T.config(yscrollcommand=S.set,state="normal")
            elif data_list[x][:9] == 'USRLIST::':
                User_area.config(yscrollcommand=S.set,state="normal")
                User_area.delete(1.0,END)
                User_area.insert(END, data_list[x][9:])
                User_area.config(yscrollcommand=S.set,state="disabled")
            else:
                T.config(yscrollcommand=S.set,state="normal")
                T.insert(END, dtime+' '+data_list[x])
                scroller = S.get()
                if scroller[1] == 1.0:  
                    T.yview(END)
                T.config(yscrollcommand=S.set,state="normal")
            msg_recv +=1
    root.after(500, task)  # reschedule event in 0.5 second

te = Test(root)
##te.pack(fill='both', expand=1)

root.protocol('WM_DELETE_WINDOW', closewin)
root.after(500, task)
root.mainloop()

