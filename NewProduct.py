from Tkinter import *
from ttk import *
import tkFont as F
from PIL import ImageTk, Image
from proWrd import Filter
from tkMessageBox import showinfo
from tkMessageBox import askokcancel, askyesno
from TableTree import MultiListbox
from buttoncalender import CalendarButton

sty = N + W + S + E


def selectfirst(item):
    return item[0]


class NewProduct(Frame):
    def __init__(self, master, tup, modify, db):
        Frame.__init__(self, master)
        self.db = db
        self.tup = tup
        self.modify = modify
        bg = 'White'
        fg = "#3496ff"
        self.master = master
        self.f = Frame(self, style='me.TFrame')
        self.f.grid(row=0, column=0, sticky=sty)
        self.f.rowconfigure(1, weight=3)
        self.f.columnconfigure(0, weight=1)
        if modify == True:
            value = tup[1]
        else:
            value = "Product Name"
        self.name = Label(self.f, text=value, font=('Berlin Sans FB Demi', 40), foreground=fg)
        self.name.grid(row=0, column=0, sticky=sty)
        note = Notebook(self.f)
        note.grid(row=1, column=0, sticky=sty)
        note.rowconfigure(0, weight=1)
        note.columnconfigure(0, weight=1)
        self.notepage1(note, modify, tup)
        if modify == True:
            self.notepage15(note)
            self.notepage2(note)
            self.notepage3(note)

    def update_name(self, event):
        name = Filter(self.entry5.get()).title()
        if len(name) == 0:
            name = "Product Name"
        self.name.configure(text=name)

    def Load_Percent(self, cost, price):
        if float(cost) == 0.0:
            return 0
        profit = float(price) - float(cost)
        percent = (100 * profit) / float(cost)
        return round(percent, 2)

    def notepage1(self, note, modify, tup):
        app = Frame(note)
        app.grid(row=0, column=0)
        self.f.rowconfigure(0, weight=1)
        self.f.columnconfigure(0, weight=1)
        note.add(app, text='Detail')
        for i in range(17):
            app.rowconfigure(i, weight=1)
        for i in range(8):
            app.columnconfigure(i, weight=1)
        Label(app, text='Product Detail', font=('Berlin Sans FB Demi', 23), foreground="#3496ff").grid(row=0, column=0,
                                                                                                       columnspan=2,
                                                                                                       sticky=sty)
        Label(app, text='Product Name').grid(row=1, column=0, sticky=E, padx=10, pady=4)
        self.entry5 = Entry(app, width=65)
        self.entry5.grid(row=1, column=1, columnspan=2, sticky=sty, padx=10, pady=10)
        self.entry5.bind('<Any-KeyRelease>', self.update_name)
        Label(app, text="Product Category").grid(row=2, column=0, sticky=E, padx=10, pady=10)
        self.entry = Combobox(app, width=35)
        self.entry.grid(row=2, column=1, columnspan=2, sticky=sty, padx=10, pady=10)
        Label(app, text="Product Description").grid(row=3, column=0, sticky=N + E, padx=10, pady=10)
        self.text = Text(app, width=26, height=5, wrap=WORD, relief=FLAT)
        self.text.grid(row=3, column=1, columnspan=2, sticky=sty, padx=10, pady=10)
        self.text.configure(highlightthickness=1, highlightbackground="Grey")
        self.df = self.text.configure()
        Label(app, text="Product QTY").grid(row=4, column=0, sticky=E, padx=10, pady=10)
        self.qty = StringVar()
        self.entry3 = Entry(app, width=35, textvariable=self.qty)
        self.entry3.grid(row=4, column=1, columnspan=2, sticky=E + W, padx=10, pady=10)

        Label(app, text=" Product ID ").grid(row=5, column=0, sticky=E)
        self.entry6 = Entry(app, width=35)
        self.entry6.grid(row=5, column=1, columnspan=2, sticky=sty, padx=10, pady=10)
        btn = Button(app, text='Save', width=12, command=lambda: self.Save(modify, self.tup), style='new.TButton')
        btn.grid(row=6, column=1, sticky=sty, padx=10, pady=10)
        copy = Button(app, text='Save As Copy', command=lambda: self.Save(False, self.tup), style='new.TButton')
        copy.grid(row=6, column=2, sticky=sty, padx=10, pady=10)
        keys = self.db.sqldb.execute("SELECT category_name FROM category").fetchall()
        keys = map(selectfirst, keys)
        keys.sort()
        self.entry['value'] = keys
        del keys
        if modify == False:
            copy['state'] = DISABLED
        if modify == True:
            d = self.db.sqldb.execute(""" SELECT product_name,category_name,product_description FROM  products 
                        JOIN category USING (category_id) WHERE product_id = "%s" """ % (tup[0])).fetchone()
            name = d[0]
            category = d[1]
            Des = d[2]
            no = tup[0]
            qty = self.db.sqldb.getquantity(tup[0])
            self.entry5.delete(0, END)
            self.entry5.insert(0, name)
            self.entry.delete(0, END)
            self.entry.insert(0, category)
            self.text.delete(0.0, END)
            self.text.insert(0.0, Des)
            self.entry3.delete(0, END)
            self.qty.set(qty)
            self.entry6.delete(0, END)
            self.entry6.insert(0, no)
        self.entry6['state'] = "readonly"
        self.entry3['state'] = "readonly"

    def Percent(self, event):
        cost = Filter(self.entry4.get())
        if len(cost) == 0:
            return showinfo(title="Error", message='Product Cost Must Be Specified Before Product % ',
                            parent=self.master)
        else:
            try:
                cost = float(cost)
            except(AttributeError, ValueError):
                return showinfo(title="Error", message='Numbers Must be Written in Cost Entry', parent=self.master)
        percent = Filter(self.entry7.get())
        if len(percent) == 0:
            percent = 0
        else:
            try:
                percent = float(percent)
            except(AttributeError, ValueError):
                return showinfo(title="Error", message='Numbers Must be Written in Profit % Entry', parent=self.master)
        s = cost / 100.0
        s = s * percent
        price = float(cost) + s
        price = round(price, 2)
        self.entry2.delete(0, END)
        self.entry2.insert(0, price)
        return 1

    def Save(self, modify, tup):
        """Objects of Tup
           tup[0] ->  ID No
           tup[1] ->  Product name
           tup[2] ->  category
           tup[3] ->  description
           tup[4] ->  quantity
        """

        name = Filter(self.entry5.get()).title()
        category = Filter(self.entry.get()).title()
        description = Filter(self.text.get(0.0, END)).title()
        if len(name.split()) == 0:
            return showinfo(title="Error", message='Product Name Must Be Specified', parent=self.master)
        if len(category.split()) == 0:
            return showinfo(title="Error", message='Product Category Must Be Specified', parent=self.master)
        vre = self.db.sqldb.getproductID(name)
        if modify == False:
            if vre != None:
                return showinfo(title="Error", message='Product Name is Already Listed Change Name To Save As Copy',
                                parent=self.master)
            PID = self.db.addproduct(name, category, description)
        elif modify == True:
            PID = tup[0]
            previousname = tup[1]
            previouscategory = tup[2]
            pdescription = tup[3]
            if previousname != name:
                if vre != None:
                    return showinfo(title="Error", message='Product Name is Already Listed', parent=self.master)
                s = askokcancel("Name Mismatch",
                                "Are You Sure You Want to Change\n\n%s to %s\n\n%s to %s\n\n%s to %s" % (
                                    previousname, name, previouscategory,
                                    category, pdescription, description), parent=self.master)
                if s == False:
                    return False
            self.db.editproduct(PID, name, category, description)
        self.master.destroy()
        return showinfo("ADDED", 'Saved Successfully')

    def Add2Mlb15(self):
        self.mlb11.delete(0, END)
        ins = self.mlb11.insert
        if self.modify == True:
            row = self.db.sqldb.execute(""" SELECT cost_id,cost,price FROM costs
                                          JOIN products USING (product_id)  WHERE product_id = "%s"  """ % (
                self.tup[0])).fetchall()
            for i in row:
                i = list(i)
                price = i[2]
                cost = i[1]
                costid = i[0]
                qty = self.db.sqldb.getcostquantity(costid)
                i.append(qty)
                ins(END, i)

    def dummy(self):
        pass

    def addcost(self, edit=False):
        try:
            PID = self.tup[0]
        except(IndexError):
            return showinfo(title="ERROR", message='Product Not Yet Saved', parent=self.master)
        try:
            newcost = float(Filter(self.ncost.get()))
            newprice = float(Filter(self.nprice.get()))
        except:
            return showinfo(title="ERROR", message='costs and price must be numbers', parent=self.master)
        costid = self.db.sqldb.getcostID(PID, newcost, newprice)
        if costid != None:
            return showinfo("Message", "Cost and Price Already Listed", parent=self.master)
        if edit == False:
            self.db.sqldb.addnewcost(PID, newcost, newprice)
        else:
            i = self.mlb11.Select_index
            if i == None:
                return showinfo("Message", "Select a Cost Or Price To Edit", parent=self.master)
            r = self.mlb11.get(i)
            pcostid = r[0]
            self.db.editcosts(pcostid, PID, newcost, newprice)
        self.Add2Mlb15()
        self.ncost.delete(0, END)
        self.nprice.delete(0, END)

    def deletecost(self):
        PID = self.tup[0]
        costid = self.pcostid
        if costid == None:
            return showinfo("Message", "Select a Cost Or Price To Delete", parent=self.master)
        ans = self.db.sqldb.deletecost(costid)
        if ans == True:
            return showinfo("Message", "%s Has Been Successfully Deleted" % (costid),
                            parent=self.master), self.Add2Mlb15()
        else:
            return showinfo("Message", "Cannot Delete %s It Is Associated With Purchase And Sells" % (costid),
                            parent=self.master)

    def setcostid(self, event):
        i = self.mlb11.Select_index
        r = self.mlb11.get(i)
        pcostid = r[0]
        self.costhead['text'] = pcostid
        self.pcostid = pcostid

    def notepage15(self, note):
        self.pcostid = None
        app15 = Frame(note)
        app15.grid(row=0, column=0)
        for i in range(3):
            app15.rowconfigure(i, weight=1)
        for i in range(3):
            app15.columnconfigure(i, weight=1)
        app15.rowconfigure(0, weight=1)
        note.add(app15, text=' Costs ')
        Label(app15, text="Product Costs", foreground="#3496ff", font=('Berlin Sans FB Demi', 25)).grid(row=0, column=0,
                                                                                                        columnspan=1,
                                                                                                        sticky=sty,
                                                                                                        pady=9)
        self.btn12 = Button(app15, text="Delete costs", command=lambda: self.deletecost())
        self.btn12.grid(row=0, column=2, sticky=sty, pady=20, padx=10)
        self.mlb11 = MultiListbox(app15, (("Cost ID", 25), ("Cost Price", 30), ("Selling Price", 30), ("Qty", 15)))
        self.mlb11.grid(row=1, column=0, columnspan=3, sticky=sty)
        self.mlb11.tree.bind('<Double-Button-1>', self.setcostid)
        lf = LabelFrame(app15, text="ADD New Costs", labelanchor=N + W)
        lf.grid(row=2, column=0, sticky=sty, pady=5, padx=5)
        self.costhead = lf
        for i in range(3):
            lf.rowconfigure(i, weight=1)
        for i in range(2):
            lf.columnconfigure(i, weight=1)
        Label(lf, text="New Cost").grid(row=0, column=0, sticky=sty, pady=5, padx=5)
        self.ncost = Entry(lf)
        self.ncost.grid(row=0, column=1, sticky=sty, pady=5, padx=5)
        Label(lf, text="New Price").grid(row=1, column=0, sticky=sty, pady=5, padx=5)
        self.nprice = Entry(lf)
        self.nprice.grid(row=1, column=1, sticky=sty, pady=5, padx=5)
        self.btn13 = Button(lf, text="Add Cost", command=lambda: self.addcost())
        self.btn13.grid(row=2, column=1, sticky=sty, pady=5, padx=5)
        self.btn14 = Button(lf, text="Edit Cost", command=lambda: self.addcost(True))
        self.btn14.grid(row=2, column=0, sticky=sty, pady=5, padx=5)
        self.Add2Mlb15()

    def Add2Mlb21(self):
        self.mlb21.delete(0, END)
        estmpro = 0
        cap = 0
        brou = 0
        ins = self.mlb21.insert
        if self.modify == True:
            row = self.db.sqldb.execute(""" SELECT purchase_id,purchase_date,cost,price,QTY FROM purchase
                                            JOIN costs USING (cost_id) JOIN products USING (product_id)  WHERE product_id = "%s"  """ % (
                self.tup[0])).fetchall()
            for i in row:
                i = list(i)
                purid = i[0]
                price = i[3]
                cost = i[2]
                date = i[1]
                qty = i[4]
                profit = round(price - cost, 2)
                estmpro += (profit * qty)
                cap += cost * qty
                brou += qty
                i.append(profit)
                ins(END, i)
        self.te.configure(text=str(estmpro))
        self.ci.configure(text=str(cap))
        self.ib.configure(text=str(brou))

    def purchaseedit(self, event):
        i = self.mlb21.Select_index
        if i == None:
            return showinfo("Message", "No Item Selected", parent=self.master)
        r = self.mlb21.get(i)
        self.purid = r[0]
        root13 = Toplevel()
        root13.title("Purchase Edit")
        root13.grid()
        for i in range(5):
            root13.rowconfigure(i, weight=1)
        for i in range(2):
            root13.columnconfigure(i, weight=1)
        lf = root13
        self.purgui = root13
        color = 'gray98'
        root13['background'] = color
        Label(lf, text="Purchase ID : %s" % (self.purid), foreground="#3496ff", font=('Berlin Sans FB Demi', 18)).grid(
            row=0, column=0, columnspan=2, sticky=sty, pady=8, padx=7)

        r = self.db.sqldb.execute(
            """ SELECT purchase_date,QTY,cost,price FROM purchase JOIN costs USING (cost_id) WHERE purchase_id = "%s" """ % (
                self.purid)).fetchone()
        Label(lf, text="Purchase Date").grid(row=1, column=0, sticky=sty, pady=8, padx=2)
        Label(lf, text="Quantity").grid(row=2, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Cost").grid(row=3, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Price").grid(row=4, column=0, sticky=sty, pady=8, padx=7)
        self.purdate = CalendarButton(lf)
        self.purdate.grid(row=1, column=1, sticky=sty, pady=8, padx=7)
        try:
            self.purdate.insert(r[0])
        except:
            self.purdate.insert(self.purdate.getTimeStamp())
        self.purqty = Entry(lf)
        self.purqty.grid(row=2, column=1, sticky=sty, pady=8, padx=7)
        self.purqty.delete(0, END)
        self.purqty.insert(0, r[1])
        self.purcost = Entry(lf)
        self.purcost.grid(row=3, column=1, sticky=sty, pady=8, padx=7)
        self.purcost.delete(0, END)
        self.purcost.insert(0, r[2])
        self.purprice = Entry(lf)
        self.purprice.grid(row=4, column=1, sticky=sty, pady=8, padx=7)
        self.purprice.delete(0, END)
        self.purprice.insert(0, r[3])
        Button(lf, text="Save", command=lambda: self.purchasesave()).grid(row=5, column=1, sticky=sty, pady=8, padx=7)
        root13.wait_window()
        return 1

    def purchasesave(self):
        PID = self.tup[0]
        try:
            cost = float(Filter(self.purcost.get()))
            price = float(Filter(self.purprice.get()))
            qty = float(Filter(self.purqty.get()))
            date = Filter(self.purdate.get())
            date = " ".join(date.split())
        except:
            return showinfo(title="ERROR", message='costs and price must be numbers', parent=self.master)
        costid = self.db.sqldb.getcostID(PID, cost, price)
        if costid == None:
            costid = self.db.sqldb.addnewcost(PID, cost, price)
        self.db.editpurchase(self.purid, costid, qty, date)
        self.purgui.destroy()
        self.Add2Mlb21()
        return showinfo(title="Successful", message='Changes Saved', parent=self.master)

    def deletepurchase(self):
        i = self.mlb21.Select_index
        if i == None:
            return showinfo("Message", "No Item Selected", parent=self.master)
        r = self.mlb21.get(i)
        self.purid = r[0]
        ans = askokcancel("Message", "Sure You Want To Delete %s ?" % (self.purid), parent=self.master)
        if ans == True:
            self.db.deletepurchase(self.purid)
            return showinfo("Message", "%s Has Been Successfully Deleted" % (self.purid),
                            parent=self.master), self.Add2Mlb21()
        return False

    def notepage2(self, note):
        self.purid = None
        app1 = Frame(note)
        app1.grid(row=0, column=0)
        for i in range(3):
            app1.rowconfigure(i, weight=1)
        for i in range(3):
            app1.columnconfigure(i, weight=1)
        app1.rowconfigure(0, weight=1)
        note.add(app1, text=' Purchase ')
        Label(app1, text="Purchase Records", foreground="#3496ff", font=('Berlin Sans FB Demi', 25)).grid(row=0,
                                                                                                          column=0,
                                                                                                          columnspan=1,
                                                                                                          sticky=sty,
                                                                                                          pady=9)
        self.btn21 = Button(app1, text="Edit Purchase Records", command=lambda: self.purchaseedit(None))
        self.btn21.grid(row=0, column=1, sticky=sty, pady=20)
        self.btn22 = Button(app1, text="Delete Purchase Records", command=lambda: self.deletepurchase())
        self.btn22.grid(row=0, column=2, sticky=sty, pady=20, padx=10)
        self.mlb21 = MultiListbox(app1, (
            ("Purchase ID", 25), ("Purchase Date", 35), ("Cost Price", 25), ("Selling Price", 25), ("Qty", 10),
            ("Expected profit", 25)))
        self.mlb21.grid(row=1, column=0, columnspan=3, sticky=sty)
        self.mlb21.tree.bind('<Double-Button-1>', self.purchaseedit)
        lf = Frame(app1)
        lf.grid(row=2, column=0, sticky=sty)
        Label(lf, text="Total Profit Estimated  - ").grid(row=1, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Total Capital Invested  - ").grid(row=0, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Total Item Brought  - ").grid(row=2, column=0, sticky=sty, pady=8, padx=7)
        self.ib = Label(lf, text="0")
        self.ib.grid(row=2, column=1, sticky=sty, padx=2)
        self.ci = Label(lf, text="0")
        self.ci.grid(row=0, column=1, sticky=sty, padx=2)
        self.te = Label(lf, text="0")
        self.te.grid(row=1, column=1, sticky=sty, padx=2)
        self.Add2Mlb21()

    def Add2Mlb22(self):
        self.mlb22.delete(0, END)
        gp = 0
        pg = 0
        tis = 0
        ins = self.mlb22.insert
        if self.modify == True:
            row = self.db.sqldb.execute(""" SELECT selling_id,invoice_date,cost,sold_price,QTY FROM (SELECT * FROM sells JOIN invoices USING (invoice_id) )
                                            JOIN costs USING (cost_id) JOIN products USING (product_id) WHERE product_id = "%s" """ % (
                self.tup[0])).fetchall()
            for i in row:
                i = list(i)
                date = i[1]
                cost = i[2]
                price = i[3]
                qty = i[4]
                profit = round(price - cost, 2)
                pg += (profit * qty)
                gp += price * qty
                tis += qty
                i.append(profit)
                ins(END, i)
        self.gp.configure(text=str(gp))
        self.pg.configure(text=str(pg))
        self.tis.configure(text=str(tis))

    def sellsedit(self, event):
        i = self.mlb22.Select_index
        if i == None:
            return showinfo("Message", "No Item Selected", parent=self.master)
        r = self.mlb22.get(i)
        self.selid = r[0]
        root13 = Toplevel()
        root13.title("Sales Edit")
        root13.grid()
        for i in range(8):
            root13.rowconfigure(i, weight=1)
        for i in range(2):
            root13.columnconfigure(i, weight=1)
        lf = root13
        self.salegui = root13
        color = 'gray98'
        root13['background'] = color
        Label(lf, text="Selling ID : %s" % (self.selid), foreground="#3496ff", font=('Berlin Sans FB Demi', 18)).grid(
            row=0, column=0, columnspan=2, sticky=sty, pady=8, padx=7)

        r = self.db.sqldb.execute(""" SELECT invoice_date,invoice_no,QTY,cost,price,sold_price FROM (SELECT * FROM sells JOIN invoices USING (invoice_id) )
                                            JOIN costs USING (cost_id) JOIN products USING (product_id) WHERE selling_id = "%s" """ % (
            self.selid)).fetchone()
        Label(lf, text="Selling Date", width=15).grid(row=1, column=0, sticky=sty, pady=8, padx=2)
        Label(lf, text="Invoice No").grid(row=2, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Quantity").grid(row=3, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Cost").grid(row=4, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Selling Price").grid(row=5, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Sold Price").grid(row=6, column=0, sticky=sty, pady=8, padx=7)
        self.seldate = CalendarButton(lf)
        self.seldate.grid(row=1, column=1, sticky=sty, pady=8, padx=7)
        try:
            self.seldate.insert(r[0])
        except:
            self.seldate.insert(self.seldate.getTimeStamp())
        self.selinvno = Entry(lf, width=40)
        self.selinvno.grid(row=2, column=1, sticky=sty, pady=8, padx=7)
        self.selinvno.delete(0, END)
        self.selinvno.insert(0, r[1])
        self.selinvno['state'] = "readonly"

        self.selqty = Entry(lf)
        self.selqty.grid(row=3, column=1, sticky=sty, pady=8, padx=7)
        self.selqty.delete(0, END)
        self.selqty.insert(0, r[2])

        self.selcost = Entry(lf)
        self.selcost.grid(row=4, column=1, sticky=sty, pady=8, padx=7)
        self.selcost.delete(0, END)
        self.selcost.insert(0, r[3])

        self.selprice = Entry(lf)
        self.selprice.grid(row=5, column=1, sticky=sty, pady=8, padx=7)
        self.selprice.delete(0, END)
        self.selprice.insert(0, r[4])

        self.selsold = Entry(lf)
        self.selsold.grid(row=6, column=1, sticky=sty, pady=8, padx=7)
        self.selsold.delete(0, END)
        self.selsold.insert(0, r[5])

        Button(lf, text="Save", command=lambda: self.salesave()).grid(row=7, column=1, sticky=sty, pady=8, padx=7)
        root13.wait_window()
        return 1

    def salesave(self):
        PID = self.tup[0]
        try:
            cost = float(Filter(self.selcost.get()))
            price = float(Filter(self.selprice.get()))
            sold = float(Filter(self.selsold.get()))
            qty = float(Filter(self.selqty.get()))
            invno = float(Filter(self.selinvno.get()))
            date = Filter(self.seldate.get())
        except:
            return showinfo(title="ERROR", message='Costs,Price,Selling,Price,Invoice No And Qty must be numbers',
                            parent=self.master)
        costid = self.db.sqldb.getcostID(PID, cost, price)
        if costid == None:
            costid = self.db.sqldb.addnewcost(PID, cost, price)
        invid = self.db.sqldb.getinvoiceID(invno)
        if invid == None:
            return showinfo(title="ERROR", message='Invoice In That Number Dsn\'t Exsist', parent=self.master)
        print (self.selid, sold, qty, costid)
        self.db.editsells(self.selid, sold, qty, costid)
        self.salegui.destroy()
        self.Add2Mlb22()
        return showinfo(title="Successful", message='Changes Saved', parent=self.master)

    def deletesells(self):
        i = self.mlb22.Select_index
        if i == None:
            return showinfo("Message", "No Item Selected", parent=self.master)
        r = self.mlb22.get(i)
        self.selid = r[0]
        ans = askokcancel("Message", "Sure You Want To Delete %s ?" % (self.selid), parent=self.master)
        if ans == True:
            self.db.deletesells(self.selid)
            return showinfo("Message", "%s Has Been Successfully Deleted" % (self.selid),
                            parent=self.master), self.Add2Mlb22()
        return False

    def notepage3(self, note):
        app2 = Frame(note)
        app2.grid(row=0, column=0)
        for i in range(3):
            app2.rowconfigure(i, weight=1)
        for i in range(3):
            app2.columnconfigure(i, weight=1)
        note.add(app2, text=' Sales ')
        Label(app2, text="Sales Records", foreground="#3496ff", font=('Berlin Sans FB Demi', 25)).grid(row=0, column=0,
                                                                                                       columnspan=1,
                                                                                                       sticky=sty,
                                                                                                       pady=9)
        self.btn31 = Button(app2, text="Edit Selling Records", command=lambda: self.sellsedit(None))
        self.btn31.grid(row=0, column=1, sticky=sty, pady=20)
        self.btn32 = Button(app2, text="Delete Selling Records", command=lambda: self.deletesells())
        self.btn32.grid(row=0, column=2, sticky=sty, pady=20, padx=10)

        self.mlb22 = MultiListbox(app2, (
            ("Selling ID", 25), ("Sold Date", 35), ("Cost Price", 25), ("Sold Price", 25), ("Quantity", 15),
            ("Profit", 25)))
        self.mlb22.grid(row=1, column=0, columnspan=3, sticky=sty)
        self.mlb22.tree.bind('<Double-Button-1>', self.sellsedit)
        lf = Frame(app2)
        lf.grid(row=2, column=0, sticky=sty)
        Label(lf, text="Total Gain From Product  - ").grid(row=0, column=0, sticky=sty, pady=8, padx=7)
        self.gp = Label(lf, text="0")
        self.gp.grid(row=0, column=1, sticky=sty, padx=2)
        Label(lf, text="Total Profit  - ").grid(row=1, column=0, sticky=sty, pady=8, padx=7)
        self.pg = Label(lf, text="0")
        self.pg.grid(row=1, column=1, sticky=sty, padx=2)
        Label(lf, text="Total Item Sold  - ").grid(row=2, column=0, sticky=sty, pady=8, padx=7)
        self.tis = Label(lf, text="0")
        self.tis.grid(row=2, column=1, sticky=sty, padx=2)
        self.Add2Mlb22()
