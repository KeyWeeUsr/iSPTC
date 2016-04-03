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
from client import read_settings, savef, readf, T_ins_warning
from sys import argv
OS = platform.system()
sys_path = os.getcwd()

def widget_sel_all(widget):
        widget.tag_add(SEL, "1.0", END)
        widget.mark_set(INSERT, "1.0")
        widget.see(INSERT)
        return "break"

def set_winicon(window,name):
    global sys_path
    OS = platform.system()
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

def search_text_dialog(widget,widget_scroll):
    widget.tag_configure("search", background="green")
    def color_tagger_thread(name, back, case):
        start = 1.0
        while start != widget.index(CURRENT):
             pos = widget.search(name, start, stopindex=END, nocase=case)
             b = pos.find('.')
             pos2 = pos[b+1:]
             if not pos:
                 break
             pos2 = pos[:b]+'.'+str(int(pos2)+int(countVar.get()))
             widget.tag_add("search", pos, pos2)
             start = pos + "+1c"
    def text_finder(*arg):
        if t_findtext_old.get() != t_findtext.get() or t_match_case_old != t_match_case:
            widget.tag_remove("search",1.0,END)
        widget.tag_remove("sel",1.0,END)
        ftext = t_findtext.get()
        t_findtext_old.set(ftext)
        t_match_case_old.set(t_match_case)
        if t_match_case.get() == 1: nocase = 0
        else: nocase = 1
        if t_search_backward.get() == 1: startVar,stopindex, back = start.get(),'1.0', True
        else: startVar,stopindex, back = start.get(), 'END', False
        if t_wrap_around.get() == 0:
            pos = widget.search(ftext, startVar, stopindex=stopindex, count=countVar, backwards=back, nocase=nocase)
        else:
            pos = widget.search(ftext, startVar, count=countVar, backwards=back, nocase=nocase)
        if pos != '':
            widget.see(pos)
            b = pos.find('.')
            pos2 = pos[b+1:]
            pos2 = pos[:b]+'.'+str(int(pos2)+int(countVar.get()))
            widget.tag_add(SEL, pos, pos2)
            widget.tag_raise("sel")
            if back == True: start.set(pos)
            else: start.set(pos2)
            color_tagger_thread(ftext,back,nocase)
        else:
            T_ins_warning(widget, widget_scroll, 'Nothing found')
    topwin = Toplevel()
    set_winicon(topwin,'icon_grey')
    topwin.title("Search dialog")
    topwin.minsize(600,80)
    topwin.resizable(FALSE,FALSE)

    frame4 = Frame(topwin, height=100,width=120, relief=SUNKEN,bg='')
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
    t_match_case_old = IntVar()
    t_wrap_around = IntVar()
    t_findtext = StringVar()
    t_findtext_old = StringVar()
    t_search_backward = IntVar()
    t_findtext.set('')
    t_findtext_old.set('')
    t_match_case.set(0)
    t_match_case_old.set(0)
    t_wrap_around.set(1)
    t_search_backward.set(0)
    
    start.set("1.0")
    Label(frame1, text="Find text: ").pack(side=LEFT)
    tEntry = Entry(frame1,textvariable=t_findtext,width=50)
    tEntry.pack(side=LEFT)
    tEntry.focus_set()

    Label(frame2, text="Options: ").pack(side=LEFT)
    Checkbutton(frame2, text="Match case", variable=t_match_case).pack(side=LEFT,padx=5)
    Checkbutton(frame2, text="Wrap around", variable=t_wrap_around).pack(side=LEFT,padx=5)
    Checkbutton(frame2, text="Search backwards", variable=t_search_backward).pack(side=LEFT,padx=5)

    def close_func(*arg):
        widget.tag_remove("search",1.0,END)
        topwin.destroy()
    button = Button(frame4, text='Find', command=text_finder).pack(side=TOP,pady=15, padx=10)
    button = Button(frame4, text='Close', command=close_func).pack(side=TOP, padx=10)
    
    topwin.protocol('WM_DELETE_WINDOW', close_func)
    topwin.bind('<Escape>', close_func)
    topwin.bind('<Return>', text_finder)

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
        self.Tbox.bind('<Control-f>',lambda x: search_text_dialog(self.Tbox,self.Tscroll))
        self.listbox.bind('<Button-1>', lambda x: self.topwin.after(20,self.file_loader))
        self.topwin.protocol('WM_DELETE_WINDOW', self.close_func)
        self.topwin.after(200,self.after_task)
        self.colortag()

    def after_task(self):
        self.topwin.bind('<Configure>', self.on_resize)
        
    def reload_file_list(self):
        try:
            self.listbox.delete(0, END)
##            file_list = os.listdir(self.filefolder)
            file_list =  next(os.walk(self.filefolder))[2]
            can_insert = True
            ignored_files = ['.lnk','.exe','.jpg','.jpeg','.mp3','.ogg','.avi','.mkv','.flv','.iso','.apk','.mp4',
                             '.wav','.doc','.docx','.zip','.sys']
            for x in file_list:
                for extension in ignored_files:
                    if x[-len(extension):] == extension:
                        can_insert = False
                        break
                if can_insert == True: self.listbox.insert("end", x)
                can_insert = True
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
        global OS
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
                if OS == 'Linux': Thread(target=self.file_loader_thread,args=(text,)).start()
                else: self.file_loader_thread(text)
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
