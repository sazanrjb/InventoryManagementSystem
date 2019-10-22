from Tkinter import *
from TableTree import MultiListbox
from ttk import *
from tkMessageBox import showinfo
from tkMessageBox import askokcancel
from proWrd import Filter,InvoiceSplit
import time as t

from buttoncalender import CalendarButton




class ModifyInvoice(Frame):
    def __init__(self,master,db):
        Frame.__init__(self,master)
        self.db = db
        self.master = master
        
