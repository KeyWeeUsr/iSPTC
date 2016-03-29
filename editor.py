#!/usr/bin/env python
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
from threading import Thread
from PIL import Image as Pillow_image
from PIL import ImageTk
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
import os,platform,tkFont, tkMessageBox, importlib
from client import read_settings, savef, readf
from sys import argv
OS = platform.system()

def widget_sel_all(widget):
        widget.tag_add(SEL, "1.0", END)
        widget.mark_set(INSERT, "1.0")
        widget.see(INSERT)
        return "break"

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

class File_editor:       
    def __init__(self,topwin,argv,**kwargs):
        global text_font
        self.topwin = topwin
        self.filefolder = 'log/'
        if len(argv) > 1: self.filefolder = argv[1]
        self.thread_status = 'Ready:'
        set_winicon(self.topwin,'icon_grey')

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
        self.topwin.bind("<Control-a>", lambda x: widget_sel_all(self.Tbox))
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
        pass
##        Themes are disabled
##        tag_colors(text=[self.Tbox],scroll=[self.Tscroll,self.Fscroll],listbox=[self.listbox],window=[self.topwin],
##                   frame=[self.frame1,self.frame2,self.frame3,self.frame4],label=[self.label1,self.loadLabel])

    def widget_sel_all(self,*arg):
        self.Tbox.tag_add(SEL, "1.0", END)
        self.Tbox.mark_set(INSERT, "1.0")
        self.Tbox.see(INSERT)
    def close_func(self,*arg):
        self.topwin.destroy()

def startup_task():
    File_editor(topwin, argv)

if __name__ == '__main__':
    font1 = str(read_settings('font1=','Arial'))
    font2 = int(read_settings('font2=',10))
    font3 = str(read_settings('font3=','normal'))
    text_font = (font1,font2,font3)
    
    topwin = Tk()
    topwin.title('Text editor')
    topwin.minsize(700,500)
    topwin.after(50, startup_task)
    topwin.mainloop()
