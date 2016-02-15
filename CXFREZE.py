import cx_Freeze, sys, shutil

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("client.py", base = base,icon="load/icon.ico"),
               cx_Freeze.Executable("updater.py", base = base,icon="load/icon.ico")]

cx_Freeze.setup(
    name="iSPTC",
    version="1.07",
    options={"build_exe": {"packages":["os","platform","socket","threading","Tkinter","time","random"],
                           "include_files":["load/icon.ico","load/beep1.wav","load/icon.png","load/settings.ini",
                                            "load/server.ini","load/icon2.png","load/icon2.ico","load/serverlist.ini",
                                            "changelog.txt","lib/top_domains.py","load/icon_grey.ico",
                                            "load/icon3.png","lib/loadscripts.ini","lib/__init__.py",
                                            "load/themes/Default","load/themes/Default_dark"]}},
    executables = executables
    )

##os.rename("fileslater","fileslater")
if sys.platform == "win32":
    shutil.rmtree('build/exe.win32-2.7/tk/demos')
    shutil.rmtree('build/exe.win32-2.7/tk/images')
