from distutils.core import setup
import py2exe
import sys
import matplotlib
from glob import glob
data_files = matplotlib.get_py2exe_datafiles()

setup(windows=[{"script": "main.py","icon_resources": [(1,"py.ico")]}],
      name = "Inventory Manager", version = "2.4.3", description = "Das Enterprise pvt. Lt.",
      data_files = data_files,
      options = {'py2exe':{'includes':['lxml.etree','lxml._elementpath','gzip'],
                          'packages':['anydbm','reportlab','matplotlib','pytz','Tkinter','FileDialog','PIL'],
                          'dll_excludes':['libgdk-win32-2.0-0.dll']}}, requires=['reportlab', 'PIL'])
