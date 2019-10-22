from Tkinter import *
from TableTree import MultiListbox
from ttk import *
from tkMessageBox import showinfo
from tkMessageBox import askokcancel
from proWrd import Filter,InvoiceSplit
import time as t
import UniqueIdGenerator as uig
from buttoncalender import CalendarButton

class ADDInvoice():
    def __init__(self,master,db):
        self.value = []
        self.db = db
        self.master = master
        self.f = Frame(master)
        self.f.grid(row = 0,column = 0,sticky = N+W+S+E)
        self.f.columnconfigure(0,weight = 1)
        self.f.rowconfigure(1,weight = 1)
        Label(self.f,text= "Invoice List",font= ('Berlin Sans FB Demi',21),foreground="#3496ff").grid(row=0,column=0,sticky=N+S+E+W,columnspan=2,padx=10,pady=5)
        self.mlb1 = MultiListbox(self.f, (("Invoice ID",40),('Invoice No', 17), ('Invoice Date', 40),('Customer Attached',40)),height = 15)
        self.mlb1.grid(row = 1,column = 0,columnspan = 4,sticky = N+W+S+E)
        self.Del = Button(self.f,text = "Delete",command = lambda: self.Delete())
        self.Del.grid(row = 2,column = 3)
        self.Add = Button(self.f,text = "ADD",command = lambda: self.Add_Invoice())
        self.Add.grid(row = 2,column = 1)
        self.Edit = Button(self.f,text = "Edit",command = lambda:self.Add_Invoice(edit = True))
        self.Edit.grid(row = 2,column =2)
        self.Insert()

    def Delete(self):
        index = self.mlb1.Select_index
        if index == None or index > self.mlb1.size():
            return showinfo('Select Error','Noting Is Selected',parent  = self.master)
        tup = self.mlb1.get(index)
        s = askokcancel('Confirm','Are You Sure You Want To Delete Invoice Number %s ?'%tup[0],parent = self.master)
        if s == True :
            self.db.deleteinvoice(tup[0])
        self.Refresh()
        return showinfo("Info","Invoice delete successfully",parent = self.master)

    def Insert(self):
        lists = self.db.sqldb.execute(""" SELECT invoice_id,invoice_no,invoice_date,customer_name FROM invoices JOIN customers USING (customer_id)
                                            ORDER BY invoice_date """).fetchall()
        self.mlb1.delete(0,END)
        for i in lists :
            self.mlb1.insert(END,i)
        return 1

    def Add_Invoice(self,edit = False):
        tup = []
        cor = 'white'
        fg = 'black'
        title = 'Add Invoice'
        heading = "New Invoice"
        if edit == True :
            title = "Modify Invoice"
            index = self.mlb1.Select_index
            if index == None or index > self.mlb1.size():
                return showinfo('Select Error','Noting Is Selected',parent = self.master )
            tup = self.mlb1.get(index)
            heading = "Invoice ID : %s "%(tup[0])
        def productsearch():
            inp = Filter(entry7.get())
            l = self.db.searchproduct(inp.title())
            entry7["value"]= l
            return 1
        def pAssdd():
            name = Filter(entry7.get()).title()
            amount = Filter(entry4.get())
            qty = Filter(entry8.get())
            PID = self.db.sqldb.getproductID(name)
            if PID == None :
                return showinfo("Error","No Product Name %s is in Product List"%(name),parent= self.app)
            try :
                amount = float(amount)
                qty = float(qty)
            except(ValueError):
                return showinfo("Error","Amount,Qty Should be in Numbers",parent= self.app)
            price  = self.db.sqldb.getcell("costs","product_id","price",PID)
            if price == None :
                return showinfo("Error","No Purchse has been made on %s "%(name),parent= self.app)
            costid = self.db.getanycostid(PID,price)
            boo = False
            for i in xrange(lb.size()):
                r = lb.get(i)
                if costid == r[3] :
                    newqty = float(r[1])+float(qty)
                    lb.setvalue(i,"Qty",newqty)
                    boo = True
            amount += float(price)*qty
            if boo == False :
                lb.insert(END,(name,qty,price,costid))
            entry7.delete(0,END)
            entry4.delete(0,END)
            entry4.insert(END,str(round(amount,2)))
            return 1
        def pDssdd():
            index = lb.Select_index
            if index == None or index > lb.size():
                return 0
            tmtup = lb.get(index)
            amount = float(Filter(entry4.get()))
            amount -=  float(tmtup[2])*float(tmtup[1])
            entry4.delete(0,END)
            entry4.insert(END,str(round(amount,2)))
            lb.delete(index)
            return 1
        self.app = Toplevel(self.master)
        self.app.title(title)
        self.app['bg'] = cor
        Label(self.app,text= heading,font= ('Berlin Sans FB Demi',21),foreground="#3496ff").grid(row=0,column=0,sticky=N+S+E+W,padx=10,pady=5)
        self.t= Frame(self.app)
        self.t.grid(row =1,column=0,sticky =N+S+E+W)
        Label(self.t,text = "Invoice No",background = cor,foreground = fg).grid(row = 0 ,column = 0,sticky = N+W+S+E,padx=10,pady=10)
        entry0 = Spinbox(self.t,from_ = 0,to =9999)
        entry0.grid(row = 0 ,column =1,sticky = N+W+S+E,padx=10,pady=10)
        
        Label(self.t,text = "Invoice Date",background = cor,foreground = fg).grid(row = 1 ,column =0,sticky = N+W+S+E,padx=10,pady=10)
        cb0 = CalendarButton(self.t)
        cb0.grid(row = 1 ,column =1,sticky = N+W+S+E,padx=10,pady=10)
        Label(self.t,text = "Customer Name",background = cor,foreground = fg).grid(row = 2 ,column =0,sticky = N+W+S+E,padx=10,pady=10)
        drop = map(lambda x : x[0] ,self.db.sqldb.execute(""" SELECT customer_name FROM customers """).fetchall())
        
        entry1 = Combobox(self.t,width = 30,value = drop )
        entry1.grid(row = 2 ,column = 1,sticky = N+W+S+E,padx=10,pady=10)
        Label(self.t,text = " Customer Address  ",background = cor,foreground = fg).grid(row = 3 ,column =0,sticky = N+W+E,padx=10,pady=10)
        entry2 = Text(self.t,width = 5,height = 5,wrap = WORD,borderwidth = 2,relief = GROOVE)
        entry2.grid(row = 3 ,column =1,sticky = N+W+S+E,padx=10,pady=10)
        Label(self.t,text = " Customer Phone",background = cor,foreground = fg).grid(row = 4 ,column =0,sticky = N+W+S+E,padx=10,pady=10)
        entry3 = Entry(self.t,width = 30)
        entry3.grid(row = 4 ,column =1,sticky = N+W+S+E,padx=10,pady=10)
        btn = Button(self.t,text ="Save Invoice",command = lambda:self.Ainv(edit,tup))
        btn.grid(row = 5 ,column =1,sticky = N+W+S+E,padx=10,pady=10)
        Label(self.t,text = "Amount",background = cor,foreground = fg).grid(row = 0 ,column =2,sticky = N+W+S+E,padx=10,pady=10)
        entry4 = Entry(self.t,width = 30)
        entry4.grid(row = 0 ,column =3,sticky = N+W+S+E,padx=10,pady=10)
        Label(self.t,text = "Paid",background = cor,foreground = fg).grid(row = 1 ,column =2,sticky = N+W+S+E,padx=10,pady=10)
        entry5 = Entry(self.t,width = 30)
        entry5.grid(row = 1 ,column =3,sticky = N+W+S+E,padx=10,pady=10)
        Label(self.t,text = "Discount",background = cor,foreground = fg).grid(row = 2 ,column =2,sticky = N+W+S+E,padx=10,pady=10)
        drop = map(lambda x : x[0] ,self.db.sqldb.execute(""" SELECT product_name FROM products ORDER BY product_name """).fetchall())
        
        entry6 = Entry(self.t,width = 30)
        entry6.grid(row = 2 ,column =3,sticky = N+W+S+E,padx=10,pady=10)
        frm = Frame(self.t)
        frm.grid(row = 3 ,column =2,sticky = N+W+E+S,padx=10,pady=10)
        btnA1 = Button(frm,text = ">>" ,command = lambda:pAssdd())
        btnA1.grid(row = 0,column=0)
        btnA2 = Button(frm,text = "<<" ,command = lambda:pDssdd())
        btnA2.grid(row = 1,column=0)
        lb = MultiListbox(self.t,[("Product Name",35),("Qty",15),("Unit Price",23),("Cost ID",30)],5)
        lb.firstcolumn("",width = 0)
        lb.grid(row = 3 ,column =3,sticky = N+W+S+E,padx=10,pady=10)

        Label(self.t,text = "Products",background = cor,foreground = fg).grid(row = 4 ,column =2,sticky = N+W+S+E,padx=10,pady=10)
        
        tmpff = Frame(self.t)
        tmpff.grid(row = 4 ,column =3,sticky = N+W+S+E,padx=0,pady=0)
        tmpff.rowconfigure(0,weight = 1)
        tmpff.columnconfigure(0,weight = 5)
        tmpff.columnconfigure(2,weight = 1)
        
        entry7 = Combobox(tmpff,width = 30,value = drop,postcommand = lambda:productsearch())
        entry7.grid(row = 0,column =0,sticky = N+W+S+E,padx=10,pady=10)
        Label(tmpff,text = "QTY",background = cor,foreground = fg).grid(row = 0 ,column =1,sticky = N+W+S+E,padx=10,pady=10)
        entry8 = Entry(tmpff,width = 10)
        entry8.grid(row = 0 ,column =2,sticky = N+W+S+E,padx=10,pady=10)
        def autofill(event):
            st = Filter(entry1.get())
            l = self.db.sqldb.execute("""SELECT customer_address,phone_no FROM customers JOIN contacts USING (customer_id)
                 WHERE customer_name =  "%s" """%(st)).fetchone()
            if l == None :
                return None
            add = l[0]
            phn= l[1]
            entry2.delete(0.0,END)
            entry2.insert(0.0,add)
            entry3.delete(0,END)
            entry3.insert(0,phn)
        def adddis(event):
            amt = Filter(entry4.get())
            paid = Filter(entry5.get())
            try :
                amt = float(amt)
                paid = float(paid)
            except(ValueError):
                return None
            dis = amt-paid
            entry6.delete(0,END)
            entry6.insert(0,str(dis))
            return None
        entry1.bind('<<ComboboxSelected>>',autofill)
        entry4.delete(0,END)
        entry4.insert(0,str(0))
        entry5.delete(0,END)
        entry5.insert(0,str(0))
        entry6.delete(0,END)
        entry6.insert(0,str(0))
        entry7.bind('<<ComboboxSelected>>',lambda event :(entry8.delete(0,END),entry8.insert(0,1.0)))
        entry5.bind('<Any-KeyRelease>',adddis)
        if edit == True :
            entry0.delete(0,END)
            entry0.insert(0,tup[1])
            entry0['state'] = "readonly"
            try:
                cb0.insert(tup[2])
            except :
                cb0.insert(cb0.getTimeStamp())
            entry1.delete(0,END)
            entry1.insert(0,tup[3])
            autofill(1)
            amount =0.0
            paid = self.db.sqldb.getcell("invoices","invoice_id","paid",tup[0])
            row = self.db.sqldb.execute("""SELECT product_name,QTY,price,cost_id FROM sells JOIN costs USING (cost_id) JOIN products USING(product_id)
                 WHERE invoice_id =  "%s" """%(tup[0])).fetchall()
            for i in row :
                amount += i[2]
                lb.insert(END,i)
            discount = float(amount) - float(paid)
            entry4.delete(0,END)
            entry4.insert(0,str(amount))
            entry5.delete(0,END)
            entry5.insert(0,str(paid))
            entry6.delete(0,END)
            entry6.insert(0,str(discount))
        self.entry0 = entry0
        self.entry1 = entry1
        self.entry2 = entry2
        self.entry3 = entry3
        self.entry4 = entry4
        self.entry5 = entry5
        self.entry6 = entry6
        self.entry7 = entry7
        self.entry8 = entry8
        self.cb0 = cb0
        self.lb = lb
        self.t.mainloop()
        return 1
    
    def Ainv(self,edit,tup):
        """tup = [invoice number,invoice date,customer name]
        """
        inv_no = Filter(self.entry0.get())
        if edit == True :
            invid = tup[0]
        else :
            invid = self.db.sqldb.getinvoiceID(inv_no)
        if invid != None and edit == False :
            return showinfo('Input Error','Invoice Number Already Exists',parent  = self.t)
        inv_date = self.cb0.get()
        if self.lb.size() == 0 :
            return showinfo('Input Error','At Least One Product must be Added',parent  = self.t)
        Cname = Filter(self.entry1.get()).title()
        if len(Cname) == 0 :
            return showinfo('Input Error','Customer Name Should Be specified',parent  = self.t)
        Cadd = Filter(self.entry2.get(0.0,END)).title()
        Cphn = Filter(self.entry3.get()).title()
        try :
            amount = float(Filter(self.entry4.get()))
            paid = float(Filter(self.entry5.get()))
            discount = float(Filter(self.entry6.get()))
        except(ValueError):
            return showinfo('Input Error','Amount, Paid and Discount Have To Be numbers',parent  = self.t)
        ctmid = self.db.sqldb.getcustomerID(Cphn)
        if ctmid == None :
            ans = askokcancel("New Customer","The Customer %s is not in customer list!\nAdd It?",parent  = self.t)
            if ans == False :
                return 0
            ctmid = self.db.addcustomer(Cname,Cadd,Cphn,"")
        else:
            dbcmname = self.db.sqldb.getcell("customers","customer_id","customer_name",ctmid)
            if dbcmname != Cname :
                showinfo('Input Error','Phone Number Already Registered in Another Name',parent  = self.t)
        if edit == True :
            self.db.editinvoice_withpaid(invid,ctmid,paid,inv_no,inv_date)
        else :
            invid = self.db.addinvoice(ctmid,inv_no,paid,inv_date)
        selids = self.db.getallsellID(invid)
        for i in selids :
            self.db.deletesells(i)
        tnoofproduct = 0
        for i in xrange(self.lb.size()) :
            r = self.lb.get(i)
            tnoofproduct+=float(tup[1])
        discountperproduct = discount/tnoofproduct
        for i in xrange(self.lb.size()) :
            tup = self.lb.get(i)
            product_price = float(tup[2])
            product_qty = float(tup[1])
            costid = tup[3]
            selID = self.db.sqldb.getsellID(invid,costid)
            sold_price = product_price - discountperproduct
            self.db.addsells(costid,sold_price,invid,product_qty)
        self.lb.delete(0,END)
        self.app.destroy()
        return self.Refresh()

    def Refresh(self):
        self.Insert()
        return showinfo('Saved','All Changes Successfully Saved',parent  = self.f)





