from Tkinter import *
from ColumnListbox import MultiListbox
from ttk import *
from tkMessageBox import showinfo
from tkMessageBox import askokcancel
from proWrd import Filter
import time as t
import shelve

df = shelve.open("g.ic")
invn = df['invn']
nam = df['nam']

class ADDInvoice():
    def __init__(self,master,invn,nam):
        self.value = []
        self.lis = invn.keys()
        self.lis.sort()
        self.invn = invn
        self.nam = nam
        self.master = master
        self.f = Frame(master)
        self.f.grid(row = 0,column = 0,sticky = N+W+S+E)
        self.f.columnconfigure(0,weight = 1)
        self.f.rowconfigure(0,weight = 1)
        self.mlb1 = MultiListbox(self.f, (('No', 5), ('Invoice Number', 15), ('Invoice Date', 40),('Customer Attach',40)))
        self.mlb1.grid(row = 0,column = 0,columnspan = 4,sticky = N+W+S+E)
        self.Del = Button(self.f,text = "Delete",command = lambda: self.Delete())
        self.Del.grid(row = 1,column = 3)
        self.Add = Button(self.f,text = "ADD",command = lambda: self.Add_Invoice())
        self.Add.grid(row = 1,column = 1)
        self.Edit = Button(self.f,text = "Edit",command = lambda:self.Add_Invoice(edit = True))
        self.Edit.grid(row = 1,column =2)
        self.Insert(self.lis,self.invn)

    def Delete(self):
        index = self.mlb1.Select_index
        if index == None or index > self.mlb1.size():
            return showinfo('Select Error','Noting Is Selected',parent  = self.master)
        tup = self.mlb1.get(index)
        s = askokcancel('Confirm','Are You Sure You Want To Delete Invoice Number %s ?'%tup[1],parent = self.master)
        if s == True :
            s = self.invn.pop(tup[1])
            r = self.nam[s.keys()[0]]['Invoice Nos'].split(",")
            delindex = r.index(str(tup[1]))
            del r[delindex]
            self.nam[s.keys()[0]]['Invoice Nos'] = ",".join(r)
        return self.Refresh()

    def Insert(self,lists,dictionary):
        r= 0
        lists = map(int,lists)
        lists.sort()
        self.mlb1.delete(0,END)
        for i in lists :
            i = str(i)
            r= r + 1
            self.mlb1.insert(END,(r,i, dictionary[i][dictionary[i].keys()[0]]["Invoice Date"],dictionary[i].keys()[0]))
        return 1
  
    def Get_Month(self,num):
        Months = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
        M = Months[num]
        return M

    def Get_Date(self,Month,Year,Day):
        rep = str(self.Get_Month(Month))+ " " + str(Day) +", "+ str(Year)
        return rep

    def Date(self):
        Year = t.localtime().tm_year
        Month = t.localtime().tm_mon
        Day = t.localtime().tm_mday
        Date = self.Get_Date(Month,Year,Day)
        return Date

    def Add_Invoice(self,edit = False):
        tup = []
        cor = 'white'
        fg = '#9558fb'
        if edit == True :
            index = self.mlb1.Select_index
            if index == None or index > self.mlb1.size():
                return showinfo('Select Error','Noting Is Selected',parent =self.master )
            tup = self.mlb1.get(index)
        self.t = Toplevel(self.master)
        self.t.title('Add Invoice')
        self.t['bg'] = cor
        self.li = []
        maxrow = 15
        maxcol = 3
        for row in xrange(maxrow):
            for column in xrange(maxcol):
                if row == 1 and column == 0 :
                    lbl = Label(self.t,text = " Invoice No",background = cor,foreground = fg)
                    lbl.grid(row = row ,column =column,sticky = N+W+S+E)
                elif row == 1 and column == 1 or row == 3 and column == 1 or row == 9 and column == 1:
                    lbl = Entry(self.t,width = 30)
                    lbl.grid(row = row ,column =column,sticky = N+W+S+E)
                    self.li.append(lbl)
                elif row == 5 and column == 1:
                    lbl = Combobox(self.t,width = 30,value = self.nam.keys())
                    lbl.grid(row = row ,column =column,sticky = N+W+S+E)
                    self.li.append(lbl)
                elif row == 7 and column == 1:
                    lbl = Text(self.t,width = 5,height = 5,wrap = WORD,borderwidth = 2,relief = GROOVE)
                    lbl.grid(row = row ,column =column,sticky = N+W+S+E)
                    self.li.append(lbl)
                elif row == 3 and column == 0 :
                    lbl = Label(self.t,text = " Invoice Date",background = cor,foreground = fg)
                    lbl.grid(row = row ,column =column,sticky = N+W+S+E)
                elif row == 5 and column ==0:
                    lbl = Label(self.t,text = " Customer Name",background = cor,foreground = fg)
                    lbl.grid(row = row ,column =column,sticky = N+W+S+E)
                elif row == 7 and column == 0 :
                    lbl = Label(self.t,text = " Customer Address  ",background = cor,foreground = fg)
                    lbl.grid(row = row ,column =column,sticky = N+W+E)
                elif row == 9 and column == 0 :
                    lbl = Label(self.t,text = " Customer Phone",background = cor,foreground = fg)
                    lbl.grid(row = row ,column =column,sticky = N+W+S+E)
                elif row == 11 and column == 1:
                    btn = Button(self.t,text ="Save Invoice",command = lambda:self.Ainv(edit,tup))
                    btn.grid(row = row ,column =column,sticky = N+W+S+E)
                else :
                    lbl = Label(self.t,background = cor,foreground = fg)
                    lbl.grid(row = row ,column =column,sticky = N+W+S+E)
                    
        self.li[2].bind('<<ComboboxSelected>>',self.autofill)
        self.li[1].delete(0,END)
        self.li[1].insert(0,self.Date())
        if edit == True :
            self.li[0].delete(0,END)
            self.li[0].insert(0,tup[1])
            self.li[1].delete(0,END)
            self.li[1].insert(0,tup[2])
            self.li[2].delete(0,END)
            self.li[2].insert(0,tup[3])
            self.autofill(1)
        self.t.mainloop()
        return 1

    def autofill(self,event):
        st = str(self.li[2].get())
        d = self.nam[st]
        add = d['Address']
        phn= d['Phone No']
        self.li[3].delete(0.0,END)
        self.li[3].insert(0.0,add)
        self.li[4].delete(0,END)
        self.li[4].insert(0,phn)
    
    def Ainv(self,edit,tup):
        d = {}
        inv_no = Filter(self.li[0].get())
        if  str(inv_no).isdigit() == False :
            return showinfo('Input Error','Invoice Number Should Be Numbers',parent  = self.t)
        sd = str(inv_no) in invn.keys()
        if sd == True :
            return showinfo('Input Error','Invoice Number Already Exists',parent  = self.t)
        inv_date = Filter(self.li[1].get())
        if len(inv_date.split()) == 0 :
            return showinfo('Input Error','Invoioce Date Should Be specified',parent  = self.t)
        Cname = Filter(self.li[2].get()).title()
        if len(Cname.split()) == 0 :
            return showinfo('Input Error','Customer Name Should Be specified',parent  = self.t)
        Cadd = Filter(self.li[3].get(0.0,END)).title()
        Cphn = Filter(self.li[4].get()).title()
        if edit == True :
            s = self.invn.pop(tup[1])
            r = self.nam[s.keys()[0]]['Invoice Nos'].split(",")
            delindex = r.index(str(tup[1]))
            del r[delindex]
            self.nam[s.keys()[0]]['Invoice Nos'] = ",".join(r)
        d['Name'] = Cname
        d['Address'] = Cadd
        d['Phone No'] = Cphn
        gh = Cname in self.nam.keys()
        if gh == True :
            d['ID No'] = self.nam[Cname]['ID No']
            d['Invoice Nos'] = str(inv_no)+"," + self.nam[Cname]['Invoice Nos']
        else :
            d['ID No'] = len(self.nam.keys()) + 1
            d['Invoice Nos'] = str(inv_no)
        d['Invoice Date'] = str(inv_date)
        d['Due']= 0
        d['Email'] = ""
        self.nam[Cname] = d
        self.invn[str(inv_no)] = {}
        self.invn[str(inv_no)][Cname] = d
        self.t.destroy()
        return self.Refresh()

    def Refresh(self):
        return self.Insert(self.invn.keys(),self.invn)



root = Tk()
root.columnconfigure(0,weight = 1)
root.rowconfigure(0,weight = 1)
app = ADDInvoice(root,invn,nam)

root.mainloop()

