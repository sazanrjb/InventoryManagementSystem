from GraphList import *
from ChoiceButton import ChoiceButton

from Tkinter import *
from ttk import *

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.lines as mlines
from numpy import arange
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class Graph(Frame):

    def __init__(self,master,currency,db,**kwrgs):
        Frame.__init__(self,**kwrgs)
        self.db =db
        self.app71 = Frame(self)
        self.app71.grid(row = 0,column = 0,sticky = N+S+E+W)
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.grid(True)
        self.c = currency
        self.a.set_ylabel("Currency.(%s)"%(currency))
        self.a.set_xlabel("Days")
        self.nm = ("January","February","March","April","May","June","July","August","September","October","November","December")
        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.f, master=self.app71)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=YES)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.app71)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.cbtn71 = ChoiceButton(self,12,"Months",self.nm)
        self.cbtn71.grid(row =0,column=1,sticky='nsew')

        self.app73 = Frame(self)
        self.app73.grid(row=1,column=0,sticky = N+S+E+W)

        btn71 = Button(master=self.app73, text='Product Earning', command=lambda:self.Proearn())
        btn71.pack(side = LEFT,fill = BOTH,expand = YES)

        btn72 = Button(master=self.app73, text='Product Cost', command=lambda:self.procostd())
        btn72.pack(side = LEFT,fill = BOTH,expand = YES)

        button = Button(master=self.app73, text='Profit PerDay', command=lambda:self._quit())
        button.pack(side = LEFT,fill = BOTH,expand = YES)

    def y2y1(self,obj):
        return obj + 0.1

    def procostd(self):
        self.a.cla()
        self.a.set_title('Product Cost/Price PerProduct')
        x = getprocostd(self.db)
        x1 = getpropriced(self.db)
        y = arange(1.0,len(x)+1,1.0)
        try :
            maxi = max(x)+1
            mini = min(x)
        except(ValueError):
            return 0
        y1 = map(self.y2y1,y)
        self.a.bar(y,x,label = "cost")
        self.a.plot(y1,x1,'ro')
        l1 = mlines.Line2D([], [], color='blue', marker='|',markersize=15, label='Price')
        l2 = mlines.Line2D([], [], color='red', marker='.',markersize=15, label='Cost')
        c = self.c
        self.a.set_ylabel("Currency(%s)"%(c))
        self.a.set_xlabel("Products")
        self.a.legend([l1,l2])
        self.a.grid(True)
        self.f.tight_layout()
        self.canvas.show()
        
    def Proearn(self):
        self.a.cla()
        self.a.set_title('Profits Earned PerProduct')
        x = getparear(self.db)
        y = arange(1.0,len(x)+1,1.0)
        try :
            maxi = max(x)+1
            mini = min(x)
        except(ValueError):
            return 0
        self.a.bar(y,x)
        c = self.c
        self.a.set_ylabel("Currency(%s)"%(c))
        self.a.set_xlabel("Products")
        self.a.grid(True)
        self.f.tight_layout()
        self.canvas.show()
        

    def _quit(self):
        self.a.cla()
        month= self.cbtn71.active['text']
        self.a.set_title('Profits Earned PerDay')
        x = getxlist(self.db,month)
        y = arange(1.0,len(x)+1,1.0)
        try :
            maxi = max(x)+1
            mini = min(x)
        except(ValueError):
            return 0
        self.a.bar(y,x)
        c = self.c
        self.a.set_ylabel("Currency(%s)"%(c))
        self.a.set_xlabel("No of Days")
        self.a.text(0.1,maxi-0.1,month,horizontalalignment='left',verticalalignment='top',transform=self.a.transAxes)
        self.a.grid(True)
        self.f.tight_layout()
        self.canvas.show()
