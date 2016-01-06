#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from time import strftime,gmtime,sleep
from subprocess import *
import platform, urllib, urllib2
from threading import Thread
v = 1.00

OS = platform.system()

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

def restart_client():
    cmd_str = 'python /home/atis/Desktop/Pitoni_Bash/sokets/client.py'
    Popen([cmd_str], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)

def download(filelink):
    global T
    filelink = filelink.rstrip()
    try:
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
                    
    except Exception as e:
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, str(e)+'\n','redcol')
        T.config(yscrollcommand=S.set,state="disabled")

## Tkinter below
root = Tk()
root.title("Updater")
root.minsize(280,300)

frame = Frame(root, height=210,width=600, relief=SUNKEN)
frame.pack_propagate(0)
frame.pack(anchor=NE,side=TOP,padx=20)

S = Scrollbar(frame, width=15)
T = Text(frame, height=46, width=80,wrap=WORD)
        
S.pack(side=RIGHT, fill=Y)
T.pack(side=BOTTOM,fill=BOTH,expand=1)
S.config(command=T.yview)
T.tag_configure('redcol', foreground='red')
T.tag_configure('blackcol', foreground='black')

button = Button(root, text='Reopen client', height=2, width=18,command=lambda: {restart_client(),root.destroy()})
button.place(x=180,y=250)
button2 = Button(root, text='Close', height=2, width=18,command=lambda: {root.destroy()})
button2.place(x=360,y=250)

## Create download link list 
tlist = []
tfile = readf('load/upd_filelist')

def downloader_thread():
    global T, tlist
    for x in tlist:
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, 'Downloading '+x[len('download,'):]+'\n','blackcol')
        download(x[len('download,'):])
    savef('','load/upd_filelist')
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, 'Erased file list\n','blackcol')
    T.insert(END, 'Done\n','blackcol')
    T.config(yscrollcommand=S.set,state="disabled")

def kill_root():
    root.destroy()

def task1():
    sleep(1)
    global T, tfile, tlist
    T.config(yscrollcommand=S.set,state="normal") 
    try:
        if len(tfile) > 0:
            for x in tfile:
                tlist.append(x)
            T.insert(END, 'List loaded\n','blackcol')
            root.after(100, task2)
        else:
            T.insert(END, 'No list, closing automatically in 15 seconds\n','redcol')
            root.after(15000, kill_root)
    except Exception as e:
        T.insert(END, str(e)+'\n','redcol')
        T.insert(END, 'Updater has stopped\n','redcol')
    T.config(yscrollcommand=S.set,state="disabled")

def task2():
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, 'Downloader thread started\n','blackcol')
    T.config(yscrollcommand=S.set,state="disabled")
    Thread(target=downloader_thread).start()

set_winicon(root,'icon')
root.after(100, task1)
root.mainloop()

