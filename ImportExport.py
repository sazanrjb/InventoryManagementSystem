import csv as c
import copy
from Tkinter import *
from ttk import *
from tkMessageBox import showinfo
from proWrd import Filter,InvoiceSplit
import tkFont as F


class DataBaseTypeError(Exception):
    pass



class ImportCsv(object):

    def __init__(self,importfile,databaseType,db):
        self.db = db
        self.returns = False
        if databaseType == "Product" :
            self.ProductImport(importfile)
        elif databaseType == "Customer" :
            self.CustomerImport(importfile)
        else :
            raise DataBaseTypeError("Wrong Type Provided ,Instead use Product or Customer")

    def ProductImport(self,importfile):
        try :
            wri = open(str(importfile),'rb')
        except(IOError):
            return showinfo('I\O Error','File Specified For Product List Does Not Exists')
        writer = c.DictReader(wri)
        new_writer = []
        for row in writer :
            n = copy.deepcopy(row)
            new_writer.append(n)
        if len(new_writer) == 0 :
            return showinfo("Message","No Products To Import")
        self.ProductImportGui(new_writer[0].keys())
        if self.isdonme == True :
            self.Im_Validate(new_writer)
        else :
            return None
        return showinfo("Successfull","All producs Have been Imported!!\nBetter Save it! if you want to keep the change.")

    def Im_Validate(self,writer):
        for row in writer:
            try:
                name = Filter(row[self.d["Name"]]).title()
            except(KeyError,IndexError):
                return showinfo('Import Error','Cannot Import Current Csv File Try Again')
            try:
                category = Filter(row[self.d['Category']]).title()
            except(KeyError):
                return showinfo('Import Error','Cannot Import Current Csv File Try Again')
            try :
                description = Filter(row[self.d['Description']]).title()
            except(KeyError):
                description = ""

            PID = self.db.sqldb.getproductID(name)
            if PID != None :
                self.db.editproduct(PID,name,category,description)
            else :
                self.db.addproduct(name,category,description)
        self.returns = True
        return 0

    def Im_Assign(self):
        if len(self.entry.get()) == 0 :
            return showinfo("Warning","Name cannot be empty",parent = self.root2)
        if len(self.entry1.get()) == 0 :
            return showinfo("Warning","Category cannot be empty",parent = self.root2)
        d = {}
        d["Name"] = Filter(self.entry.get())
        d['Category'] = Filter(self.entry1.get())
        d['Description'] = Filter(self.entry2.get())
        self.d = d
        self.isdonme = True
        return self.root2.destroy()

    def ProductImportGui(self,C_value):
        colour = 'orange'
        self.isdonme = False
        self.root2 = Toplevel()
        self.root2.title('Product Import Option')
        self.root2['bg'] = colour
        self.root2.grid()
        self.root2.columnconfigure(0,weight = 1)
        self.root2.rowconfigure(0,weight = 1)
        app = Frame(self.root2)
        app.grid(row = 0,column = 0,padx=10,pady =10)
        for i in range(9):
            app.rowconfigure(i,weight = 1)
        app.columnconfigure(0,weight = 1)
        app.columnconfigure(1,weight = 1)
        Combo_Width = 50
        fg = 'White'
        ############################################################################################
        Label(app,text = "Name",background = colour,foreground = fg,font = F.Font(family = 'Times',size = 15)).grid(row = 0,column = 0,sticky = N+W+E+S,padx=10,pady =10)
        self.entry = Combobox(app,width = Combo_Width,value = C_value,state = 'readonly')
        self.entry.grid(row = 0,column = 1,sticky = N+W+E+S,padx=10,pady =10)
        Label(app,text = 'Category',background = colour,foreground = fg,font = F.Font(family = 'Times',size = 15)).grid(row = 1,column = 0,sticky = N+W+E+S,padx=10,pady =10)
        self.entry1 = Combobox(app,width = Combo_Width,value = C_value)
        self.entry1.grid(row = 1,column = 1,sticky = N+W+E+S,padx=10,pady =10)
        Label(app,text = 'Description',background = colour,foreground = fg,font = F.Font(family = 'Times',size = 15)).grid(row = 2,column = 0,sticky = N+W+E+S,padx=10,pady =10)
        self.entry2 = Combobox(app,width = Combo_Width,value = C_value)
        self.entry2.grid(row = 2,column = 1,sticky = N+W+E+S,padx=10,pady =10)
        
        self.btn = Button(app,text = 'Assign',padding = -1,command = lambda:self.Im_Assign())
        self.btn.grid(row = 3,column = 1,sticky = N+E+W+S,padx=10,pady =10)
        ############################################################################################
        self.root2.wait_window()
        return 1

    def CustomerImport(self,importfile):
        try :
            wri = open(str(importfile),'rb')
        except(IOError):
            return showinfo('I\O Error','File Specified For Customer List Does Not Exists')
        writer = c.DictReader(wri)
        new_writer = []
        for row in writer :
            n = copy.deepcopy(row)
            new_writer.append(n)
        if len(new_writer) == 0 :
            return showinfo("Message","No Customers To Import")
        self.CustomerImportGui(new_writer[0].keys())
        if self.iscdonme == True :
            self.Im_CValidate(new_writer)
        else :
            return 1
        return showinfo("Successfull","All Customers Have been Imported!!\nBetter Save it! if you want to keep the change.")

    def Im_CValidate(self,writer):
        for row in writer:
            try:
                name= Filter(row[self.d["Customer Name"]]).title()
            except(KeyError):
                return showinfo('Import Error','Cannot Import Current Csv File Try Again')
            try :
                phone = Filter(row[self.d["Customer Phone"]]).title()
            except(KeyError):
                return showinfo('Import Error','Cannot Import Current Csv File Try Again')
            try:
                address = Filter(row[self.d["Customer Address"]]).title()
            except(KeyError):
                address = ""
            try:
                email = Filter(row[self.d["Customer Email"]]).title()
            except(KeyError):
                email = ""
            if len(phone) == 10 :
                phnid = self.db.sqldb.getphoneID(phone)
                print (phnid,phone,name,address,email),len(phone)
                if phnid != None :
                    self.db.editcustomer(phnid,phone,name,address,email)
                else :
                    self.db.addcustomer(name,address,phone,email)
        self.returns = True
        return 1

    def Im_CAssign(self):
        if len(self.el[1].get()) == 0 :
            return showinfo("Warning","Customer Name cannot be empty",parent = self.root2)
        d ={}
        d["Customer Name"] = Filter(self.el[0].get())
        d["Customer Phone"] = Filter(self.el[1].get())
        d["Customer Address"] = Filter(self.el[2].get())
        d["Customer Email"] = Filter(self.el[3].get())
        self.d = d
        self.iscdonme = True
        return self.root2.destroy()

    def CustomerImportGui(self,C_value):
        colour = 'orange'
        self.iscdonme = False
        self.root2 = Toplevel()
        self.root2.title('Customer Import Option')
        self.root2['bg'] = colour
        self.root2.grid()
        self.root2.columnconfigure(0,weight = 1)
        self.root2.rowconfigure(0,weight = 1)
        app = Frame(self.root2)
        app.grid(row = 0,column = 0)
        Combo_Width = 50
        fg = 'White'
        self.el = range(4)
        maxrow = xrange(5)
        maxcolumn = xrange(3)
        ################################################
        for row in maxrow :
            app.columnconfigure(row,weight = 1)
            for column in maxcolumn :
                app.rowconfigure(column,weight = 1)
                if (row == 0 and column == 1) or (row == 1 and column == 1) or (row == 2 and column == 1 )or (row == 3 and column == 1):
                    entry = Combobox(app,width = Combo_Width,value = C_value)
                    entry.grid(row = row,column = column,sticky = N+W+E+S,padx =10,pady=10)
                    self.el[row] = entry
                elif row == 0 and column == 0 :
                    Label(app,background = colour,foreground = fg ,text = "Customer Name",font = F.Font(family = 'Times',size = 15)).grid(row = row,column = column,sticky = N+W+E+S,padx =10,pady=10)
                elif row == 1 and column == 0 :
                    Label(app,background = colour,foreground = fg ,text = "Customer Phone",font = F.Font(family = 'Times',size = 15)).grid(row = row,column = column,sticky = N+W+E+S,padx =10,pady=10)
                elif row == 2 and column == 0 :
                    Label(app,background = colour,foreground = fg ,text = "Customer Address  ",font = F.Font(family = 'Times',size = 15)).grid(row = row,column = column,sticky = N+W+E+S,padx =10,pady=10)
                elif row == 3 and column == 0 :
                    Label(app,background = colour,foreground = fg ,text = "Customer Email",font = F.Font(family = 'Times',size = 15)).grid(row = row,column = column,sticky = N+W+E+S,padx =10,pady=10)
                elif row == 4 and column == 1:
                    self.btn = Button(app,text = 'Assign',padding = -1,command = lambda:self.Im_CAssign())
                    self.btn.grid(row = row,column = column,sticky = N+E+W+S,padx =10,pady=10)
        #################################################
        self.root2.wait_window()
        return 1
        



class ExportCsv(object):

    def __init__(self,exportfile,db):
        self.db = db
        self.returns = False
        self.Export(exportfile)

    def Export(self,exportfile):
        self.writeproducts(exportfile)
        self.writecustomer(exportfile)
        self.returns = True
        return None

    def writecustomer(self,exportfile):
        fields = ("customer_name","customer_address","customer_email","phone_no")
        wri = open(str(exportfile+"customers")+".csv",'wb')
        writer = c.writer(wri)
        writer.writerow(fields)
        rows = self.db.sqldb.execute(""" SELECT customer_name,customer_address,customer_email,phone_no FROM customers JOIN contacts USING (customer_id) """).fetchall()
        for row in rows :
            writer.writerow(row)
        wri.close()
        return None

    def writeproducts(self,exportfile):
        fields = ("product_name","product_description","product_category")
        wri = open(str(exportfile+"products")+".csv",'wb')
        writer = c.writer(wri)
        writer.writerow(fields)
        rows = self.db.sqldb.execute(""" SELECT product_name,product_description,category_name FROM products JOIN category USING (category_id) """).fetchall()
        for row in rows :
            writer.writerow(row)
        wri.close()
        return 1





