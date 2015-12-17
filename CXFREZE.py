import cx_Freeze, sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("client.py", base = base)]

cx_Freeze.setup(
    name="iSPTC",
    version="0.81",
    options={"build_exe": {"packages":["os","platform","socket","threading","Tkinter","time","random"],
                           "include_files":["load/icon.ico","load/beep1.wav","load/icon.png","load/settings","load/server"]}},
    executables = executables
    )

##os.rename("fileslater","fileslater")
