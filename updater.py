#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from time import strftime,gmtime,sleep
from shutil import move as move_file
from subprocess import *
import platform, urllib, urllib2, os
from threading import Thread
from ttk import Button
from ttk import Scrollbar
v = '2'

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

def write_settings(text_find,new_value):
    global sys_path
    a = readf('load/settings.ini')
    a = edit_settings(a,text_find,new_value)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,'load/settings.ini')  

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
    a = readf('load/settings.ini')
    a = get_settings(a,arg[0],arg[1])
    return a

def get_settings(text,text_find,default_value):
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = lines[len(text_find):]
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

def set_winicon(window,name):
    global OS
    if OS is 'Windows':
        try:
            window.iconbitmap("load\\"+name+".ico")
        except:
            print "Couldn't load windows icon"
    else:
        try:
            img = PhotoImage(file='load/'+name+'.png')
            window.tk.call('wm', 'iconphoto', window._w, img)
        except:
            print "Couldn't load Linux icon"

def restart_client():
    global OS
    INPUT = 'python client.py'
    if OS == 'Windows':
        if os.path.exists('client.exe') == True:
            INPUT = 'client.exe'
    Popen([INPUT], shell=True,
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
root.title("Updater ver: "+str(v))
root.minsize(280,300)

frame = Frame(root, height=210,width=600, relief=SUNKEN)
frame.pack_propagate(0)
frame.pack(anchor=NE,side=TOP,padx=20,pady=20)

S = Scrollbar(frame)
T = Text(frame, height=46, width=80,wrap=WORD)
        
S.pack(side=RIGHT, fill=Y)
T.pack(side=BOTTOM,fill=BOTH,expand=1)
S.config(command=T.yview)
T.tag_configure('redcol', foreground='red')
T.tag_configure('blackcol', foreground='black')
T.tag_configure('greencol', background='#c8d9ea',foreground='#009900')
T.tag_configure('failed', background='#c8d9ea',foreground='red')

button = Button(root, text='Reopen client', command=lambda: {restart_client(),root.destroy()})
button.place(x=180,y=250)
button2 = Button(root, text='Close', command=lambda: {root.destroy()})
button2.place(x=360,y=250)

## Create download link list 
tlist = []
tfile = readf('load/upd_filelist')

def worker_thread():
    global T, tlist
    cnt = 0
    try:
        for x in tlist:
            T.config(yscrollcommand=S.set,state="normal")
            if x[:8] == 'download':
                T.insert(END, 'Downloading '+x[len('download,'):]+'\n','blackcol')
                download(x[len('download,'):])
            elif x[:8] == 'movefile':
                b = x[9:].find(',')
                source = x[9:b+9]
                target = x[b+10:]
                templist = [[source],[target]]
                T.insert(END, 'Moving '+source+' to '+target+'\n','blackcol')
                move_file(source,target)
            elif x[:8] == 'mkfolder':
                try:
                    os.stat(x[9:])
                except:
                    os.mkdir(x[9:])
                    T.insert(END, 'Making folder - '+x[9:]+'\n','blackcol')
                    
        savef('','load/upd_filelist')
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, 'Erased file list\n','blackcol')
        T.insert(END, '#Done\n','greencol')
        T.config(yscrollcommand=S.set,state="disabled")
    except Exception as e:
        e = str(e)
        T.config(yscrollcommand=S.set,state="normal")
        T.insert(END, 'Update failed, worker thread has crashed\n','redcol')
        T.insert(END, e+'\n','redcol')
        T.insert(END, '#Failed\n','failed')
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
            T.insert(END, 'No list, closing in 15 seconds\n','redcol')
            root.after(15000, kill_root)
    except Exception as e:
        T.insert(END, str(e)+'\n','redcol')
        T.insert(END, 'Updater has stopped\n','redcol')
        T.insert(END, '#Failed\n','failed')
    T.config(yscrollcommand=S.set,state="disabled")

def task2():
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, 'Worker thread started\n','blackcol')
    T.config(yscrollcommand=S.set,state="disabled")
    Thread(target=worker_thread).start()

file_updater_ver = str(read_settings('updater_ver=','1'))
can_update = True
if v != file_updater_ver:
    T.config(yscrollcommand=S.set,state="normal")
    T.insert(END, 'Updater version does not match the stored value\nTry updating again\n','redcol')
    T.insert(END, '#Failed\n','failed')
    T.config(yscrollcommand=S.set,state="disabled")
    write_settings('updater_ver',v)
    can_update = False

set_winicon(root,'icon')
if can_update == True:
    root.after(100, task1)
root.mainloop()

