import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os", "time", "subprocess", "sys", "win32gui"],
"excludes": ["tkinter"], "optimize": 2, "include_files": ["config.ini", "README.md"]}

base = None

setup(  name = "udkbr",
        version = "0.1",
        description = "UDK Build & Run",
        options = {"build_exe": build_exe_options},
        executables = [Executable("udkbr.py", base=base, icon = r"icon.ico")])