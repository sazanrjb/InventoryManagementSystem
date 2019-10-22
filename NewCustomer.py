from Tkinter import *
from ttk import *
import tkFont as F
from proWrd import Filter, InvoiceSplit
from tkMessageBox import showinfo
from tkMessageBox import askokcancel
from TableTree import MultiListbox
import UniqueIdGenerator as uig
from buttoncalender import CalendarButton

sty = N + W + S + E


class NewCustomer(Frame):
    def __init__(self, master, modify, tup, db):
        Frame.__init__(self, master)
        self.master = master
        self.db = db
        self.modify = modify
        self.tup = tup
        bg = 'White'
        fg = "#3496ff"
        self.app = Frame(master)
        self.app.grid(row=0, column=0, sticky=sty)
        self.app.rowconfigure(1, weight=1)
        self.app.columnconfigure(0, weight=1)
        if modify == True:
            value = tup[1]
            self.ctmid = tup[0]
        else:
            value = "Customer Name"
            self.ctmid = None
        self.name = Label(self.app, text=value, font=('Arial Black', 26), foreground=fg)
        self.name.grid(row=0, column=0, sticky=sty, pady=10)

        note = Notebook(self.app)
        note.grid(row=1, column=0, sticky=sty)
        note.rowconfigure(0, weight=1)
        note.columnconfigure(0, weight=1)
        self.notepage1(note, modify, tup)
        if modify == True:
            self.notepage2(note)

    def update_name(self, event):
        name = Filter(self.entry5.get()).title()
        if len(name) == 0:
            name = "Customer Name"
        self.name.configure(text=name)

    def editinvoice(self):
        i = self.mlb21.Select_index
        if i == None:
            return showinfo("Message", "No Item Selected", parent=self.master)
        piid = self.mlb21.trueparent(self.mlb21.Select_iid)
        i = self.mlb21.index(piid)
        r = self.mlb21.get(i)
        self.invid = r[0]
        root13 = Toplevel()
        root13.title("Invoice Edit")
        root13.grid()
        for i in range(5):
            root13.rowconfigure(i, weight=1)
        for i in range(2):
            root13.columnconfigure(i, weight=1)
        lf = root13
        self.invgui = root13
        color = 'gray98'
        root13['background'] = color
        Label(lf, text="Invoice ID : %s" % (self.invid), foreground="#3496ff", font=('Berlin Sans FB Demi', 18)).grid(
            row=0, column=0, columnspan=2, sticky=sty, pady=8, padx=7)

        r = self.db.sqldb.execute(""" SELECT invoice_date,invoice_no,customer_name,phone_no FROM invoices
                JOIN customers USING (customer_id) JOIN contacts USING (customer_id) WHERE invoice_id = "%s" """ % (
            self.invid)).fetchone()
        Label(lf, text="Invoice Date", width=20).grid(row=1, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Invoice No").grid(row=2, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Customer Name").grid(row=3, column=0, sticky=sty, pady=8, padx=7)
        Label(lf, text="Customer Phone").grid(row=4, column=0, sticky=sty, pady=8, padx=7)
        self.invdate = CalendarButton(lf)
        self.invdate.grid(row=1, column=1, sticky=sty, pady=8, padx=7)
        try:
            self.invdate.insert(r[0])
        except:
            self.invdate.insert(self.invdate.getTimeStamp())
        self.invno = Spinbox(lf, from_=0, to=9999)
        self.invno.grid(row=2, column=1, sticky=sty, pady=8, padx=7)
        self.invno.delete(0, END)
        self.invno.insert(0, r[1])

        self.cusname = Entry(lf, width=40)
        self.cusname.grid(row=3, column=1, sticky=sty, pady=8, padx=7)
        self.cusname.delete(0, END)
        self.cusname.insert(0, r[2])

        self.cusphn = Entry(lf)
        self.cusphn.grid(row=4, column=1, sticky=sty, pady=8, padx=7)
        self.cusphn.delete(0, END)
        self.cusphn.insert(0, r[3])

        Button(lf, text="Save", command=lambda: self.invoicesave()).grid(row=5, column=1, sticky=sty, pady=8, padx=7)
        root13.wait_window()
        return 1

    def invoicesave(self):
        try:
            no = float(Filter(self.invno.get()))
            phn = Filter(self.cusphn.get())
            date = Filter(self.invdate.get())
        except:
            return showinfo(title="ERROR", message='Invoice Number must be numbers', parent=self.master)
        ctmid = self.db.sqldb.getcustomerID(phn)
        if ctmid == None:
            return showinfo(title="ERROR", message='Customer Not Found', parent=self.master)
        self.db.editinvoice(self.invid, ctmid, no, date)
        self.invgui.destroy()
        self.mlb21load()
        return showinfo(title="Successful", message='Changes Saved', parent=self.master)

    def deleteinvoice(self):
        i = self.mlb21.Select_index
        if i == None:
            return showinfo("Message", "No Item Selected", parent=self.master)
        r = self.mlb21.get(i)
        self.invid = r[0]
        ans = askokcancel("Message", "Sure You Want To Delete %s ?" % (self.invid), parent=self.master)
        if ans == True:
            b = self.db.deleteinvoice(self.invid)
            if b == True:
                return showinfo("Message", "%s Has Been Successfully Deleted" % (self.invid),
                                parent=self.master), self.mlb21load()
            else:
                return showinfo("Message", "%s Is Attached To Selling Records" % (self.invid),
                                parent=self.master), self.mlb21load()
        return False

    def notepage2(self, note):
        self.invid = None
        app1 = Frame(note)
        app1.grid(row=0, column=0, sticky=sty)
        note.add(app1, text=' Invoices ')
        for i in range(5):
            app1.rowconfigure(i, weight=1)
        for i in range(3):
            app1.columnconfigure(i, weight=1)
        Label(app1, text="Invoice Attached", font=('Berlin Sans FB Demi', 21), foreground="#3496ff").grid(row=0,
                                                                                                          column=0,
                                                                                                          sticky=sty,
                                                                                                          padx=10,
                                                                                                          pady=10)
        self.mlb21 = MultiListbox(app1,
                                  (("Invoice ID", 30), ("Invoice Number", 25), ("Invoice Date", 35), ("Paid", 20)))
        self.mlb21.grid(row=1, column=0, columnspan=3, sticky=sty)
        Button(app1, text="Edit Invoice", command=lambda: self.editinvoice()).grid(row=0, column=1, sticky=sty, pady=20)
        Button(app1, text="Delete Invoice", command=lambda: self.deleteinvoice()).grid(row=0, column=2, sticky=sty,
                                                                                       pady=20, padx=5)
        self.lbl1 = Label(app1, text="Total Amount Earned - 0 ")
        self.lbl1.grid(row=2, column=0, sticky=sty, padx=5, pady=5)
        self.lbl2 = Label(app1, text="Total No of Product - 0 ")
        self.lbl2.grid(row=3, column=0, sticky=sty, padx=5, pady=5)
        self.lbl3 = Label(app1, text="Total Amount Due - 0 ")
        self.lbl3.grid(row=4, column=0, sticky=sty, padx=5, pady=5)
        if self.modify == True:
            self.mlb21load()
        return 1

    def mlb21load(self):
        self.mlb21.delete(0, END)
        ctmid = self.tup[0]
        invoices = self.db.sqldb.execute("""SELECT invoice_id,invoice_no,invoice_date,paid
                           FROM invoices WHERE customer_id = "%s" ORDER BY invoice_no """ % (ctmid)).fetchall()
        tp = 0.0
        tpro = 0
        td = 0.0
        for i in invoices:
            invid = i[0]
            paid = i[3]
            tp = tp + float(paid)
            iid = self.mlb21.insert(END, i)
            tup1 = self.db.sqldb.execute(""" SELECT  product_name,cost,sold_price,QTY  FROM  (SELECT * FROM sells JOIN costs USING (cost_id) JOIN products USING (product_id) )
                    JOIN invoices USING (invoice_id) WHERE invoice_id = "%s" ORDER BY product_name """ % (
                invid)).fetchall()
            self.mlb21.insert(END, ["Product Name", "Cost Price", "Selling Price", "Qty"], parent=iid, rowname="+",
                              bg='grey90', fg='Blue', tag="l5")
            tpro += len(tup1)
            for g in xrange(len(tup1)):
                self.mlb21.insert(END, tup1[g], parent=iid, rowname=g, bg='white')
        self.lbl1["text"] = "Total Amount Earned - %d " % (tp)
        self.lbl2["text"] = "Total No of Product - %d " % (tpro)
        self.lbl3["text"] = "Total Amount Due - %d " % (td)
        return 0

    def phnrefresh(self, ctmid):
        self.mlb2221.delete(0, END)
        d = self.db.execute(""" SELECT phone_no FROM contacts WHERE customer_id = "%s" """ % (ctmid))
        for i in d:
            self.mlb2221.insert(END, i)
        return None

    def phoneedit(self, edit):
        tup = []
        if edit == True:
            index = self.mlb2221.Select_index
            if index == None or index > self.mlb2221.size():
                return showinfo('Select Error', 'Noting Is Selected', parent=self.master)
            piid = self.mlb2221.trueparent(self.mlb2221.Select_iid)
            index = self.mlb2221.index(piid)
            tup = self.mlb2221.get(index)
        self.t = Toplevel(master=self.master)
        self.t.title('Add Contact Number')
        if edit == True:
            self.t.title('Edit Contact Number')
        self.t['bg'] = 'white'
        self.t.focus()
        Label(self.t, text="Contact Number", background='white').grid(row=1, column=0, padx=5, pady=5)
        self.e = Entry(self.t)
        self.e.grid(row=1, column=1, sticky=E + S + W + N, padx=5, pady=5)
        btn = Button(self.t, text="Save Phone", command=lambda: self.Savephone(edit, tup))
        btn.grid(row=2, column=1, sticky=E + S + W + N, padx=5, pady=5)
        if edit == True:
            Label(self.t, text="Phone ID : ", background='white').grid(row=0, column=0, padx=5, pady=5)
            Label(self.t, text=self.db.sqldb.getphoneID(tup[0]), background='white').grid(row=0, column=1, padx=5,
                                                                                          pady=5)
            self.e.delete(0, END)
            self.e.insert(0, tup[0])
        self.t.wait_window()
        return None

    def Savephone(self, edit, tup):
        phone = Filter(self.e.get())
        if self.db.sqldb.getphoneID(phone) is not None:
            return showinfo('Error', 'Phone Number Is Already Added.', parent=self.t)
        # phnid = self.db.sqldb.getphoneID(phone)
        # ctmid = self.ctmid
        # if phnid is not None and edit == False:
        #     return showinfo('Type Error', 'Phone Number Is Already Listed', parent=self.t)
        # if not phone.isdigit():
        #     return showinfo('Type Error', 'Not a Valid Phone Number', parent=self.t)
        # if edit:
        #     pphn = self.db.sqldb.getphoneID(tup[0])
        #     if pphn is not None:
        #         self.db.editphone(pphn, phone, ctmid)
        #     else:
        #         return showinfo('Type Error', 'Phone Number Already Listed', parent=self.t)
        # else:
        #     if ctmid is None:
        #         return showinfo('Error', 'Add Phone Number After Adding Customer.', parent=self.t)
        #     self.db.addphone(phone, ctmid)
        if edit:
            index = self.mlb2221.Select_index
            if index is None or index > self.mlb2221.size():
                return showinfo('Select Error', 'Noting Is Selected', parent=self.master)
            piid = self.mlb2221.trueparent(self.mlb2221.Select_iid)
            index = self.mlb2221.index(piid)
            self.mlb2221.setvalue(index,0,phone)
        else :
            self.mlb2221.insert(END, phone)
        self.t.destroy()
        return None

    def phonedelete(self):
        index = self.mlb2221.Select_index
        if index is None or index > self.mlb2221.size():
            return showinfo('Select Error', 'Noting Is Selected', parent=self.master)
        piid = self.mlb2221.trueparent(self.mlb2221.Select_iid)
        index = self.mlb2221.index(piid)
        tup = self.mlb2221.get(index)
        phnid = self.db.sqldb.getphoneID(tup[0])
        if phnid == None:
            self.mlb2221.delete(index)
            return None
        d = self.db.deletephone(phnid)
        if d:
            self.mlb2221.delete(index)
            return showinfo('Info', 'Phone Number Deleted Successfully', parent=self.master)
        else:
            return showinfo('Info', 'Phone Number Cannot Be deleted attached with Customer', parent=self.master)
        return None

    def notepage1(self, note, modify, tup):
        app = Frame(note)
        app.grid(row=0, column=0, sticky=sty)
        note.add(app, text='Customer')
        for i in range(20):
            app.rowconfigure(i, weight=1)
        for i in range(3):
            app.columnconfigure(i, weight=1)
        Label(app, text="Customer Detail", font=('Berlin Sans FB Demi', 21), foreground="#3496ff").grid(row=0, column=0,
                                                                                                        sticky=sty,
                                                                                                        columnspan=2,
                                                                                                        padx=10,
                                                                                                        pady=10)
        lbl = Label(app, text='Customer Name  ')
        lbl.grid(row=1, column=0, sticky=sty, padx=5, pady=5)

        self.entry5 = Entry(app, width=55)
        self.entry5.grid(row=1, column=1, sticky=sty, padx=5, pady=5)
        self.entry5.bind('<Any-KeyRelease>', self.update_name)

        lbl3 = Label(app, text="Email ")
        lbl3.grid(row=2, column=0, sticky=sty, padx=5, pady=5)
        self.entry3 = Entry(app, width=35)
        self.entry3.grid(row=2, column=1, sticky=sty, padx=5, pady=5)

        lbl1 = Label(app, text="Customer Address ", anchor=N)
        lbl1.grid(row=3, column=0, sticky=sty, padx=5, pady=5)
        self.text = Text(app, width=26, height=5, wrap=WORD, relief=FLAT)
        self.text.grid(row=3, column=1, sticky=sty, padx=5, pady=5)
        self.text.configure(highlightthickness=1, highlightbackground="Grey")

        tmpapp = Frame(app)
        tmpapp.grid(row=1, column=2, rowspan=4, sticky=sty, padx=0, pady=0)
        tmpapp.columnconfigure(0, weight=1)
        tmpapp.rowconfigure(0, weight=5)
        tmpapp.rowconfigure(1, weight=1)

        self.mlb2221 = MultiListbox(tmpapp, [("Phone Number", 30)], height=5)
        self.mlb2221.grid(row=0, column=0, sticky=sty, padx=5, pady=5)

        tmpapp = Frame(tmpapp)
        tmpapp.grid(row=1, column=0, sticky=sty, padx=0, pady=0)
        tmpapp.rowconfigure(0, weight=1)

        Button(tmpapp, text='Add', command=lambda: self.phoneedit(False)).grid(row=0, column=0, sticky=sty, padx=5,
                                                                               pady=5)
        Button(tmpapp, text='Edit', command=lambda: self.phoneedit(True)).grid(row=0, column=1, sticky=sty, padx=5,
                                                                               pady=5)
        Button(tmpapp, text='Delete', command=lambda: self.phonedelete()).grid(row=0, column=2, sticky=sty, padx=5,
                                                                               pady=5)

        tmpapp = Frame(app)
        tmpapp.grid(row=4, column=1, sticky=sty, padx=0, pady=0)
        tmpapp.columnconfigure(0, weight=1)
        tmpapp.columnconfigure(1, weight=1)
        tmpapp.rowconfigure(0, weight=1)

        btn = Button(tmpapp, text='Save', width=12, command=lambda: self.Save(modify, tup))
        btn.grid(row=0, column=0, sticky=sty, padx=5, pady=5)
        copy = Button(tmpapp, text='Save As Copy', width=12, command=lambda: self.Save(False, tup))
        copy.grid(row=0, column=1, sticky=sty, padx=5, pady=5)
        if modify == False:
            copy['state'] = DISABLED

        if modify == True:
            ctmid = self.tup[0]
            d = self.db.sqldb.execute(
                """ SELECT customer_name,customer_address,customer_email FROM customers WHERE customer_id = "%s" """ % (
                    ctmid)).fetchone()
            name = d[0]
            add = d[1]
            email = d[2]
            self.phnrefresh(ctmid)
            self.entry5.delete(0, END)
            self.entry5.insert(0, name)
            self.text.delete(0.0, END)
            self.text.insert(0.0, add)
            self.entry3.delete(0, END)
            self.entry3.insert(0, email)

    def Save(self, modify, tup):
        """
           tup[0] = id no
           tup[1] = customer name
           tup[2] = phn no
           tup[3] = address
           tup[4] = email
        """

        name = Filter(self.entry5.get()).title()
        add = Filter(self.text.get(0.0, END)).title()
        email = Filter(self.entry3.get()).title()
        if len(name.split()) == 0:
            return showinfo(title="Error", message='Customer Name Must Be Specified', parent=self.master)
        ctmid = None
        if not modify:
            ctmid = self.db.addcustomer(name, address=add, email=email)
        else:
            ctmid = self.tup[0]
            ask = askokcancel("Key Error",
                              "Are You Sure You Want To Change The Customer Name From %s To %s ?" % (tup[1], name),
                              parent=self.master)
            if not ask:
                return 1
            self.db.editcustomer(ctmid, name, add, email)
        if ctmid is not  None :
            for i in xrange(self.mlb2221.size()):
                tup = self.mlb2221.get(i)
                phnid = self.db.sqldb.getphoneID(tup[0])
                if phnid is None:
                    self.db.addphone(tup[0],ctmid)
        self.master.destroy()
        return showinfo("ADDED", 'Saved Successfully')
