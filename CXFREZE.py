import cx_Freeze, sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("client.py", base = base,icon="load/icon.ico"),
               cx_Freeze.Executable("updater.py", base = base,icon="load/icon.ico")]

cx_Freeze.setup(
    name="iSPTC",
    version="0.96",
    options={"build_exe": {"packages":["os","platform","socket","threading","Tkinter","time","random"],
                           "include_files":["load/icon.ico","load/beep1.wav","load/icon.png","load/settings.cfg","load/server.cfg","load/icon2.png","load/icon2.ico","load/serverlist","load/changelog.txt"]}},
    executables = executables
    )

##os.rename("fileslater","fileslater")
