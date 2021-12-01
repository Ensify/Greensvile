from cx_Freeze import setup, Executable
import sys

build_exe_options = {'packages': ['pygame', 'sys', 'os', 'random','pytmx','sqlite3','tkinter','pickle','options','tilemap','objects','level'],
                     'include_files':['icon.ico','config.dat','controls.dat','levelmaps.dat','playerdata.db','controls.png','Controls_screen.png','Controls_selector.png','exit.png','launcher_screen.png','options.png','play.png','pointer.png','img','map','player']}

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

setup ( name = 'GreensVille',
        version = '1',
        description = 'SF GUI',
        options = {'build_exe': build_exe_options},
        executables = [Executable('Launcher.py', base=base,icon="icon.ico")])
