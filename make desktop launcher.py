#!/usr/bin/env python
import os
import getpass

user = getpass.getuser()
path = os.getcwd()+'/'

def editf():
    a = []
    a.append('[Desktop Entry]')
    a.append('Comment=')
    a.append('Terminal=false')
    a.append('Name=iSPTC')
    a.append('Exec='+ path + 'client.py')
    a.append('Path='+ path)
    a.append('Type=Application')
    a.append('Icon=' + path + 'load/icon.png')
    return a

def savef(text):
    f = open('/home/'+ user + '/Desktop/iSPTC.desktop', 'w')
    print ('/home/'+ user + '/Desktop/iSPTC.desktop')
    f.write(text)
    f.close()

def main():
    file = editf()
    text = file = '\n'.join(str(e) for e in file)
    savef(text)
    print('------->')
    print('Done!')


main()
