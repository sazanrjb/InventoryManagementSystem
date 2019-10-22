import os
import tkFont
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
from tkMessageBox import askokcancel
from tkMessageBox import showinfo
from ttk import *

from PIL import ImageTk, Image
from proWrd import Filter

import TableTree as tableTree
from Cato_Opt import Category
from NewCustomer import NewCustomer
from NewInvoice import ADDInvoice
from NewProduct import NewProduct
from PdfGenarator import pdf_document
from PurchaseLog import Purchase_Log
from buttoncalender import CalendarButton
from pcclass import InventoryDataBase
from scroll_frame import SampleApp

# variable access by all

db = InventoryDataBase()

# Window

root = Tk()
root.title("Inventory Manager")
root.iconbitmap('data/database_4.ico')
root.minsize(1024, 768)
root.grid()
root.rowconfigure(0, weight=1)
for h in range(12):
    root.columnconfigure(h, weight=1)
root.rowconfigure(2, weight=2)
root.wm_state('zoomed')

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
filemenu.add_command(label="  Save Customer and Product", command=lambda: db.Save(), bitmap='info', compound=LEFT)
filemenu.add_command(label="  Load Database File", command=lambda: ask_dbfile(), bitmap='question', compound=LEFT)
filemenu.add_command(label="  Exit", command=lambda: call_save(), bitmap='error', compound=LEFT)
editmenu.add_command(label="Company Details", command=lambda: cdmp_del(), bitmap='info', compound=LEFT)
editmenu.add_command(label="Reset All", command=lambda: reset(), bitmap='info', compound=LEFT)
root.config(menu=menubar)

color = 'gray98'
root['background'] = color

styl = Style()
styl.configure("r.TFrame", background=color)
styl.configure("r.TNotebook", background=color)
styl.configure("r.TButton", background=color)
styl.configure("r.TLabel", background=color)
styl.configure(".", background=color, font=("Arial Rounded MT Bold", 10))
styl.configure("r.TLabelframe", background=color)

# notebook
upnote = Frame(root, style='r.TFrame')
upnote.grid(row=2, column=0, columnspan=12, sticky=N + S + E + W)
upnote.columnconfigure(0, weight=1)
upnote.rowconfigure(0, weight=1)

note = Notebook(upnote, style='r.TNotebook')
note.grid(row=0, column=0, sticky=N + S + E + W)
note.rowconfigure(0, weight=1)
note.columnconfigure(0, weight=1)

saveico = Image.open("Data/floppy_disk_blue.png").resize((50, 50), Image.ANTIALIAS)
saveico = ImageTk.PhotoImage(image=saveico)
Button(root, text="Save", command=lambda: db.save(), compound=TOP, image=saveico, width=2).grid(row=0, column=0,
                                                                                                sticky=N + S + W + E)

npico = Image.open("Data/new_file.png").resize((50, 50), Image.ANTIALIAS)
npico = ImageTk.PhotoImage(image=npico)
productbtn = Button(root, text="New Product", command=lambda: a_d_d__product(modify=False), image=npico, compound=TOP,
                    width=2)
productbtn.grid(row=0, column=1, sticky=N + S + W + E)

ncico = Image.open("Data/user_group_new.png").resize((50, 50), Image.ANTIALIAS)
ncico = ImageTk.PhotoImage(image=ncico)
customerbtn = Button(root, text="New Customer", command=lambda: a_d_d__customer(modify=False), image=ncico,
                     compound=TOP,
                     width=2)
customerbtn.grid(row=0, column=2, sticky=N + S + W + E)

setting_ico = Image.open("Data/settings_ico2.png").resize((50, 50), Image.ANTIALIAS)
setting_ico = ImageTk.PhotoImage(image=setting_ico)
Button(root, text="Edit Company Details", command=lambda: cdmp_del(),
       image=setting_ico, compound=TOP, width=2).grid(row=0,
                                                      column=3,
                                                      sticky=N + S + W + E)

app = Frame(note)
app.grid(row=0, column=0, sticky=N + S + E + W)
note.add(app, text='    Invoice    ')

app.columnconfigure(0, weight=1)
app.rowconfigure(1, weight=1)
app.rowconfigure(2, weight=5)

Label(app, text="Create Invoice And Sell Product", foreground="#3496ff", font=('Berlin Sans FB Demi', 20),
      background="White").grid(row=0, column=0, sticky=N + S + E + W)

add_together = Frame(app)
add_together.grid(row=1, column=0, sticky=N + E + S + W)
add_together.rowconfigure(0, weight=1)

for h in range(3):
    add_together.columnconfigure(h, weight=1)

Lf01 = LabelFrame(add_together, text="Customer Options", labelanchor=N, style="r.TLabelframe", width=2500)
Lf01.grid(row=0, column=0, sticky=N + E + S + W, padx=10, pady=10)
for h in range(3):
    Lf01.rowconfigure(h, weight=1)
for h in range(1, 2):
    Lf01.columnconfigure(h, weight=1)

# Customer name
lbl0 = Label(Lf01, text="Customer name", anchor=E)
lbl0.grid(row=0, column=0, sticky=N + E + S + W, pady=10, padx=5)

customer_name = Combobox(Lf01, postcommand=lambda: customer_name__search(), width=35)
customer_name.grid(row=0, column=1, sticky=N + E + S + W, pady=8, padx=10)

# Phone

lbl3 = Label(Lf01, text="Customer Contact No", anchor=E)
lbl3.grid(row=1, column=0, sticky=N + E + S + W, pady=10, padx=5)

customer_phone = Entry(Lf01, justify=RIGHT)
customer_phone.grid(row=1, column=1, sticky=N + S + E + W, pady=10, padx=10)

# Address


lbl1 = Label(Lf01, text="Customer Address", anchor=E)
lbl1.grid(row=2, column=0, sticky=N + E + W, pady=10, padx=5)

customer_address = Text(Lf01, width=5, height=5, wrap=WORD, relief=FLAT)
customer_address.grid(row=2, column=1, sticky=N + E + S + W, pady=10, padx=10)
customer_address.configure(highlightthickness=1, highlightbackground="Grey", relief=FLAT)

#       Product name
Lf02 = LabelFrame(add_together, text="Product Options", labelanchor=N)
Lf02.grid(row=0, column=1, sticky=N + E + S + W, padx=5, pady=10)
Lf02.columnconfigure(1, weight=1)
for h in range(5):
    Lf02.rowconfigure(h, weight=1)

lbl6 = Label(Lf02, text="Product name", anchor=E)
lbl6.grid(row=0, column=0, sticky=N + E + S + W, padx=5, pady=10)

product_name = Combobox(Lf02, postcommand=lambda: product_name__search(), width=40)
product_name.grid(row=0, column=1, sticky=N + E + W + S, padx=5, pady=10)

# Product Detail
lbl8 = Label(Lf02, text="Product Description")
lbl8.grid(row=1, column=0, sticky=N + E, padx=5, pady=10)

product_detail = Text(Lf02, width=4, height=2, wrap=WORD, relief=FLAT)
product_detail.grid(row=1, column=1, rowspan=2, sticky=N + E + S + W, pady=10, padx=5)
product_detail.configure(highlightthickness=1, highlightbackground="Grey", relief=FLAT)

# Product Price

lbl9 = Label(Lf02, text="Unit Price")
lbl9.grid(row=4, column=0, sticky=N + E, padx=5, pady=10)

product_price = Entry(Lf02, justify=RIGHT)
product_price.grid(row=4, column=1, sticky=N + E + S + W, padx=5, pady=10)

# QTY
lbl11 = Label(Lf02, text="Quantity")
lbl11.grid(row=3, column=0, sticky=N + E, padx=5, pady=10)

quantity = Entry(Lf02, justify=RIGHT)
quantity.grid(row=3, column=1, sticky=N + E + S + W, padx=5, pady=10)

# invoice option

Lf04 = LabelFrame(add_together, text="Invoice Options", labelanchor=N)
Lf04.grid(row=0, column=2, sticky=N + E + S + W, padx=5, pady=10)
Lf04.columnconfigure(1, weight=1)
for h in range(1, 10):
    Lf04.rowconfigure(h, weight=1)
# Invoice Date

Label(Lf04, text="Invoice Date", anchor=N + W).grid(row=0, column=0, sticky=N + E + W + S, padx=0, pady=0)

invoice_date = CalendarButton(Lf04)
invoice_date.grid(row=1, column=0, columnspan=2, sticky=N + E + S + W, padx=5, pady=0)

# Invoice Number
Label(Lf04, text="Invoice Number", anchor=N + W).grid(row=2, column=0, sticky=N + E + W + S, padx=5, pady=5)

invoice_number = Spinbox(Lf04, from_=0, to=10000, increment=1.0, wrap=True, readonlybackground='gray98')
invoice_number.grid(row=2, column=1, sticky=N + E + W + S, padx=5, pady=5)
# +- Button

Cartindeldbnfram = Frame(Lf04)
Cartindeldbnfram.grid(row=9, column=0, columnspan=2, sticky=E + W + N + S, padx=0, pady=0)
Cartindeldbnfram.rowconfigure(0, weight=1)
Cartindeldbnfram.columnconfigure(0, weight=1)
Cartindeldbnfram.columnconfigure(1, weight=1)

tmp = Image.open("Data/cart_add.png").resize((25, 25), Image.ANTIALIAS)
tmp = ImageTk.PhotoImage(image=tmp)
Button(Cartindeldbnfram, text="Add To Cart", image=tmp,
       compound=LEFT, command=lambda: add_2_cart()).grid(row=0, column=0,
                                                         sticky=E + W + N + S,
                                                         padx=5,
                                                         pady=5)

tmp2 = Image.open("Data/cart_remove.png").resize((25, 25), Image.ANTIALIAS)
tmp2 = ImageTk.PhotoImage(image=tmp2)
Button(Cartindeldbnfram, text="Remove From Cart", image=tmp2,
       compound=LEFT, command=lambda: remove_from_cart()).grid(row=0, column=1,
                                                               sticky=E + W + N + S, padx=5,
                                                               pady=5)

# side

dframe = Frame(app)
dframe.grid(row=2, column=0, sticky=N + S + E + W)
dframe.columnconfigure(0, weight=1)
dframe.rowconfigure(0, weight=1)

# Amount
Lf03 = LabelFrame(dframe, text="Billing Options", labelanchor=N)
Lf03.grid(row=0, column=1, sticky=N + E + S + W)

Fon = tkFont.Font(family='Times', size=17)
Fon1 = tkFont.Font(family='Times', size=14)

# AMOUNT

lbl27 = Label(Lf03, text="Amount :", font=Fon1)
lbl27.grid(row=0, column=0, sticky=E + N + S, padx=10, pady=10)

Amt_var = DoubleVar()

Amount = Label(Lf03, font=Fon1, textvariable=Amt_var)
Amount.grid(row=0, column=1, sticky=N + E + S + W, padx=10, pady=10)


# GST

def get_sgst():
    return db.sqldb.get_company_details['sgst']


def get_cgst():
    return db.sqldb.get_company_details['cgst']


def tax_update(a, b, c):
    sgst_var.set(round(get_sgst() * (Amt_var.get() / 100), 2))
    cgst_var.set(round(get_cgst() * (Amt_var.get() / 100), 2))
    subtol_var.set(round(sgst_var.get() + cgst_var.get() + Amt_var.get(), 2))
    entry20.delete(0, END)
    entry20.insert(0, str(subtol_var.get()))
    Discount_var.set(0.0)
    Gtol_var.set(subtol_var.get())


Amt_var.trace('w', tax_update)

Label(Lf03, text="SGST @ " + str(get_sgst()) + "% : ", font=Fon1).grid(row=1, column=0, sticky=E + N + S, padx=10,
                                                                       pady=10)

sgst_var = DoubleVar()

sgst = Label(Lf03, font=Fon1, textvariable=sgst_var)
sgst.grid(row=1, column=1, sticky=N + E + S + W, padx=10, pady=10)

Label(Lf03, text="CGST @ " + str(get_cgst()) + "% : ", font=Fon1).grid(row=2, column=0, sticky=E + N + S, padx=10,
                                                                       pady=10)

cgst_var = DoubleVar()

cgst = Label(Lf03, font=Fon1, textvariable=cgst_var)
cgst.grid(row=2, column=1, sticky=N + E + S + W, padx=10, pady=10)

Separator(Lf03, orient=HORIZONTAL).grid(row=3, column=0, columnspan=2, sticky="ew", padx=8, pady=4)

# subtotal

Label(Lf03, text="Sub Total :", font=Fon1).grid(row=4, column=0, sticky=E + N + S, padx=10, pady=10)
subtol_var = DoubleVar()
Label(Lf03, font=Fon1, textvariable=subtol_var).grid(row=4, column=1, sticky=W + N + S, padx=10, pady=10)

# Paid

lbl20 = Label(Lf03, text="Paid :", font=Fon1)
lbl20.grid(row=5, column=0, sticky=E + N + S, padx=10)

entry20 = Entry(Lf03)
entry20.grid(row=5, column=1, sticky=N + S + E + W, padx=5)

# Discount

lbl28 = Label(Lf03, text="Discount :", font=Fon1)
lbl28.grid(row=6, column=0, sticky=E + N + S, padx=10, pady=10)

Discount_var = DoubleVar()

Discount = Label(Lf03, font=Fon1, textvariable=Discount_var)
Discount.grid(row=6, column=1, sticky=W + N + S, padx=10, pady=10)

# Grand Total

Separator(Lf03, orient=HORIZONTAL).grid(row=7, column=0, columnspan=2, sticky="ew", padx=8, pady=4)

lbl25 = Label(Lf03, text="Grand Total :", font=Fon)
lbl25.grid(row=8, column=0, sticky=E + N + S, padx=10, pady=10)

Gtol_var = DoubleVar()

Gtol = Label(Lf03, font=Fon, textvariable=Gtol_var, width=10)
Gtol.grid(row=8, column=1, sticky=N + E + S + W, padx=10, pady=10)

# Generate
genico = Image.open("Data/new_doc.png").resize((50, 50), Image.ANTIALIAS)
genico = ImageTk.PhotoImage(image=genico)

butn_Gen = Button(Lf03, text="Generate Invoice", command=lambda: transfer(), image=genico, compound=LEFT)
butn_Gen.grid(row=9, column=0, columnspan=2, sticky=E + W + S + N, pady=10, padx=8)

# Table

mlb = tableTree.MultiListbox(dframe,
                             (("Cost ID", 20), ('Product', 35), ('Description', 45), ("QTY", 6), ("Unit Price", 9)))
mlb.grid(row=0, column=0, sticky=N + S + E + W, padx=10)

#     note purchase product

upf = Frame(note)
upf.grid(row=0, column=0, sticky=N + W + S + E)
note.add(upf, text="    Purchase    ")
upf.columnconfigure(0, weight=1)
upf.rowconfigure(1, weight=1)

Label(upf, text="Products Purchase", foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0, column=0,
                                                                                                  sticky=N + S + E + W)

app6 = Frame(upf)
app6.grid(row=1, column=0, sticky=N + W + S + E)

for i in range(1):
    app6.columnconfigure(i, weight=1)
for i in range(1, 5):
    if i == 2:
        continue
    app6.rowconfigure(i, weight=1)

Label(app6, background="Brown").grid(row=0, column=0, sticky=N + S + E + W)

lfp = Frame(app6, padding="0.2i")
lfp.grid(row=1, column=0, sticky=N + S + E + W)

for i in range(1, 6):
    if i in (0, 2, 4):
        continue
    lfp.columnconfigure(i, weight=1)
for i in range(0, 7):
    lfp.rowconfigure(i, weight=1)

Label(lfp, text="Product name  ").grid(row=1, column=0, sticky=E, padx=10, pady=5)

entry61 = Combobox(lfp, postcommand=lambda: product_entry_search())
entry61.grid(row=1, column=1, sticky=W + E, padx=10, pady=5)

Label(lfp, text="Quantity  ").grid(row=3, column=0, sticky=E, padx=10, pady=5)

entry62 = Entry(lfp)
entry62.grid(row=3, column=1, sticky=W + E, padx=10, pady=5)

Label(lfp, text="Cost Price  ").grid(row=5, column=0, sticky=E, padx=10, pady=5)

entry63 = Entry(lfp)
entry63.grid(row=5, column=1, sticky=W + E, padx=10, pady=5)

Label(lfp, text="Purchase Date").grid(row=1, column=2, sticky=E, padx=10, pady=5)

btn64 = CalendarButton(lfp)
btn64.grid(row=1, column=3, sticky=W + E + S + N, padx=10, pady=5)

Label(lfp, text="Selling Price  ").grid(row=3, column=2, sticky=E, padx=10, pady=5)

entry65 = Entry(lfp)
entry65.grid(row=3, column=3, sticky=W + E, padx=10, pady=5)

editbtnfram = Frame(lfp)
editbtnfram.grid(row=5, column=3, sticky=N + E + S + W, padx=0, pady=0)
editbtnfram.rowconfigure(0, weight=1)
editbtnfram.columnconfigure(0, weight=1)
editbtnfram.columnconfigure(1, weight=1)

tmp4 = Image.open("Data/edit_add.png").resize((25, 25), Image.ANTIALIAS)
tmp4 = ImageTk.PhotoImage(image=tmp4)
Button(editbtnfram, text="Add",
       image=tmp4, compound=LEFT,
       command=lambda: add2_purchase_table()).grid(row=0, column=0, sticky=N + E + S + W,
                                                   padx=10, pady=5)
tmp5 = Image.open("Data/symbol_remove.png").resize((25, 25), Image.ANTIALIAS)
tmp5 = ImageTk.PhotoImage(image=tmp5)
Button(editbtnfram, text="Remove",
       image=tmp5, compound=LEFT,
       command=lambda: delete_from_purchase_table()).grid(row=0, column=1,
                                                          sticky=N + W + S + E, padx=10,
                                                          pady=5)

btn65 = Button(lfp, text=" Inventory Purchase Log ", width=20, command=lambda: ipurlog())
btn65.grid(row=5, column=2, sticky=N + S + E + W, padx=10, pady=5)

Label(lfp, text="Category  ").grid(row=1, column=4, sticky=E, padx=10, pady=5)

entry66 = Combobox(lfp, postcommand=lambda: ckeys())
entry66.grid(row=1, column=5, sticky=W + E, padx=10, pady=5)

Label(lfp, text="Description  ").grid(row=3, column=4, sticky=E + N, padx=10, pady=5)

text61 = Text(lfp, width=0, height=2, wrap=WORD, relief=FLAT)
text61.grid(row=3, column=5, rowspan=3, sticky=W + E + N + S, padx=10, pady=5)
text61.configure(highlightthickness=1, highlightbackground="Grey", relief=FLAT)

mlb21 = tableTree.MultiListbox(app6,
                               (('Product name', 35), ("Cost Price", 25), ("Selling Price", 25), ("QTY", 15),
                                ("Date", 35)))
mlb21.grid(row=3, column=0, columnspan=1, sticky=N + S + E + W)

tmp3 = Image.open("Data/next.png").resize((70, 70), Image.ANTIALIAS)
tmp3 = ImageTk.PhotoImage(image=tmp3)

btn62 = Button(app6, text="Complete Transaction", width=35,
               image=tmp3, compound=LEFT,
               command=lambda: add2_inventory())
btn62.grid(row=4, column=0, sticky=N + E + S, pady=10)

Label(app6, background="Brown").grid(row=5, column=0, sticky=N + S + E + W)

# page 3
# frame 3

app2 = Frame(note)
app2.grid(row=0, column=0)

app2.columnconfigure(0, weight=1)
app2.columnconfigure(1, weight=7)
app2.rowconfigure(2, weight=1)

note.add(app2, text='    Inventory    ')

Label(app2, text='Inventory Product List',
      foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0, column=0,
                                                                   columnspan=2,
                                                                   sticky=E + N + W + S,
                                                                   padx=10, pady=0)

app2sub2 = Frame(app2)
app2sub2.grid(row=1, column=0, sticky=N + S + W + E, padx=5, pady=0)

app2sub2.columnconfigure(1, weight=1)
app2sub2.columnconfigure(0, weight=5)
app2sub2.rowconfigure(0, weight=1)

lf3 = LabelFrame(app2sub2, text="Product Search Option")
lf3.grid(row=0, column=0, sticky=N + S + W + E, padx=2, pady=10)
for h in xrange(1, 3):
    lf3.columnconfigure(h, weight=1)
for h in xrange(2):
    lf3.rowconfigure(h, weight=1)
Label(lf3, text="Search KeyWord").grid(row=0, column=0, sticky=N + W + S + E, padx=5, pady=7)
product_search = Combobox(lf3, width=35, postcommand=lambda: product__search())
product_search.grid(row=0, column=1, columnspan=2, sticky=N + W + S + E, padx=5, pady=7)

tmp6 = Image.open("Data/search.png").resize((20, 20), Image.ANTIALIAS)
tmp6 = ImageTk.PhotoImage(image=tmp6)
Button(lf3, text="Search", width=15,
       image=tmp6,
       command=lambda: b_product__search()).grid(row=1, column=1, sticky=N + W + S + E,
                                                 padx=5, pady=5)
tmp7 = Image.open("Data/view_refresh.png").resize((20, 20), Image.ANTIALIAS)
tmp7 = ImageTk.PhotoImage(image=tmp7)
Button(lf3, text="Refresh", width=15, image=tmp7,
       command=lambda: b_product__search(refresh=True)).grid(row=1, column=2,
                                                             sticky=N + W + S + E, padx=5,
                                                             pady=5)

lf31 = LabelFrame(app2sub2, text="Product Edit Option")
lf31.grid(row=0, column=1, sticky=N + W + S + E, padx=2, pady=10)
for h in range(2):
    lf31.columnconfigure(h, weight=1)
for h in range(2):
    lf31.rowconfigure(h, weight=1)
Button(lf31, text="Add Product",
       image=tmp4, compound=LEFT,
       command=lambda: a_d_d__product(), width=20).grid(row=0, column=0, sticky=N + W + E + S,
                                                        padx=5, pady=5)
Button(lf31, text="Remove Product",
       image=tmp5, compound=LEFT,
       command=lambda: remove__product(mlb31), width=20).grid(row=0, column=1,
                                                              sticky=N + W + S + E, padx=5,
                                                              pady=5)

tmp_modify = Image.open("Data/settings.png").resize((20, 20), Image.ANTIALIAS)
tmp_modify = ImageTk.PhotoImage(image=tmp_modify)
Button(lf31, text="Modify Product",
       image=tmp_modify, compound=LEFT,
       command=lambda: a_d_d__product(modify=True), width=20).grid(row=1, column=0,
                                                                   sticky=N + W + S + E,
                                                                   padx=5, pady=5)
tmp_extra = Image.open("Data/settings_2.png").resize((20, 20), Image.ANTIALIAS)
tmp_extra = ImageTk.PhotoImage(image=tmp_extra)

Button(lf31, text="Category Options",
       image=tmp_extra, compound=LEFT,
       command=lambda: category_opt_event(), width=20).grid(row=1, column=1,
                                                            sticky=N + W + S + E, padx=5,
                                                            pady=5)

mlb31 = tableTree.MultiListbox(app2,
                               (('Product ID', 5), ('Product Name', 45), ('Category', 25), ('Description', 65),
                                ("QTY", 10)))
mlb31.grid(row=2, column=0, columnspan=2, sticky=N + S + E + W)

# page 4
# listing

app3 = Frame(note)
app3.grid(row=0, column=0)
app3.columnconfigure(0, weight=1)
app3.columnconfigure(1, weight=5)
app3.rowconfigure(2, weight=1)

note.add(app3, text="    Customers    ")
Label(app3, text='Customer Database List',
      foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0, column=0,
                                                                   columnspan=2,
                                                                   sticky=E + N + W + S,
                                                                   padx=10, pady=0)
df = Frame(app3)
df.grid(row=1, column=0, sticky=N + S + W + E)
df.columnconfigure(0, weight=5)
df.columnconfigure(1, weight=1)

lf41 = LabelFrame(df, text="Customer Search Options")
lf41.grid(row=0, column=0, sticky=N + S + W + E, padx=2, pady=0)
lf41.columnconfigure(1, weight=1)
lf41.columnconfigure(2, weight=1)
for h in xrange(2):
    lf41.rowconfigure(h, weight=1)
Label(lf41, text="Search KeyWord").grid(row=0, column=0, sticky=N + S + E, padx=5, pady=5)
customer_search = Combobox(lf41, postcommand=lambda: customer__search(), width=35)
customer_search.grid(row=0, column=1, columnspan=2, sticky=N + W + S + E, padx=5, pady=5)

Button(lf41, text="Search", width=15, image=tmp6,
       command=lambda: b_customer__search()).grid(row=1, column=1, sticky=N + W + S + E,
                                                  padx=5, pady=5)
Button(lf41, text="Refresh", width=15, image=tmp7,
       command=lambda: b_customer__search(refresh=True)).grid(row=1, column=2,
                                                              sticky=N + W + S + E,
                                                              padx=5, pady=5)

lf42 = LabelFrame(df, text="Customer Edit Options")
lf42.grid(row=0, column=1, sticky=N + W + S + E, padx=2, pady=0)
lf42.columnconfigure(0, weight=1)
lf42.columnconfigure(1, weight=1)
for h in xrange(2):
    lf42.rowconfigure(h, weight=1)
Button(lf42, text="Add Customer", width=20,
       image=tmp4, compound=LEFT,
       command=lambda: a_d_d__customer()).grid(row=0, column=0, sticky=N + W + S + E,
                                               padx=5, pady=5)
Button(lf42, text="Remove Customer", width=20,
       image=tmp5, compound=LEFT,
       command=lambda: remove__customer(mlb41)).grid(row=0, column=1,
                                                     sticky=N + W + S + E,
                                                     padx=5, pady=5)
Button(lf42, text="Modify Customer", width=20,
       image=tmp_modify, compound=LEFT,
       command=lambda: a_d_d__customer(modify=True)).grid(row=1, column=0,
                                                          sticky=N + W + E + S,
                                                          padx=5, pady=5)
Button(lf42, text="Invoice Option", width=20,
       image=tmp_extra, compound=LEFT,
       command=lambda: invoice_opt_event()).grid(row=1, column=1,
                                                 sticky=N + W + E + S, padx=5,
                                                 pady=5)

mlb41 = tableTree.MultiListbox(app3,
                               (('Customer ID', 5), ('Customer Name', 40), ('Phone No', 15), ('Address', 70),
                                ("Email", 30)))
mlb41.grid(row=2, column=0, columnspan=2, sticky=N + S + E + W, pady=10)

# Page  5

app4 = Frame(note)
app4.grid(row=0, column=0)
for h in range(8):
    app4.columnconfigure(h, weight=1)
app4.columnconfigure(24, weight=1)

note.add(app4, text="    Imports and Exports    ")
Label(app4, text='Import and Export CSV',
      foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0, column=0,
                                                                   sticky=E + N + W + S,
                                                                   padx=10, pady=0)
lf2 = LabelFrame(app4, text="Import Option")
lf2.grid(row=2, column=0, rowspan=5, columnspan=6, sticky=N + W + S + E, padx=10, pady=10)
for h in range(7):
    lf2.columnconfigure(h, weight=1)
lbl54 = Label(lf2, text="Import Product List From   ")
lbl54.grid(row=2, column=1, sticky=N + E + S + W, padx=10, pady=10)
entry51 = Entry(lf2, width=35)
entry51.grid(row=2, column=2, columnspan=2, sticky=N + E + S + W, padx=10, pady=10)
btn51 = Button(lf2, text="Browse File", command=lambda: brow__file(entry51))
btn51.grid(row=2, column=5, sticky=N + E + S + W, padx=10, pady=10)

C51 = Canvas(app4, width=350, height=350, bg="White")
C51.grid(row=2, rowspan=15, column=8, columnspan=15, sticky=N + E + W + S, padx=10, pady=10)
Fon3 = tkFont.Font(family='Times', size=24)
Fon4 = tkFont.Font(family='Times', size=16)
ir3 = C51.create_text(205, 280, text="Total Solution To Inventory \n                         Management", font=Fon4)
ir = C51.create_text(150, 50, text="     Inventory   Manager", font=Fon3)
ir1 = C51.create_text(220, 90, text="         Powered by", font=Fon4)
ir2 = C51.create_text(127, 215, text="Das \n      Enterprise", font=Fon3)
lbl58 = Label(lf2, text="Import Customer List From   ")
lbl58.grid(row=4, column=1, sticky=N + E + S + W, padx=10, pady=10)
entry52 = Entry(lf2, width=35)
entry52.grid(row=4, column=2, columnspan=2, sticky=N + E + S + W, padx=10, pady=10)
btn52 = Button(lf2, text="Browse File", command=lambda: brow__file(entry52))
btn52.grid(row=4, column=5, sticky=N + E + S + W, padx=10, pady=10)
btn55 = Button(lf2, text="Import", command=lambda: import_csv(entry51.get(), entry52.get()))
btn55.grid(row=6, column=4, columnspan=2, sticky=N + E + S + W, padx=10, pady=10)

# LabelFrame Export Option

lf1 = LabelFrame(app4, text="Export Option")
lf1.grid(row=8, column=0, rowspan=9, columnspan=6, sticky=N + W + S + E, padx=10, pady=10)
for h in range(7):
    lf1.columnconfigure(h, weight=1)

lbl511 = Label(lf1, text="Export To  Folder ")
lbl511.grid(row=8, column=1, sticky=N + E + S + W, padx=10, pady=10)

entry53 = Entry(lf1, width=35)
entry53.grid(row=8, column=2, columnspan=2, sticky=N + E + S + W, padx=10, pady=10)

btn53 = Button(lf1, text="Choose File", command=lambda: save__as__file(entry53))
btn53.grid(row=8, column=5, sticky=N + E + S + W, padx=10, pady=10)

btn55 = Button(lf1, text="Export", command=lambda: export(entry53))
btn55.grid(row=12, column=4, columnspan=2, sticky=N + E + S + W, padx=10, pady=10)


#
# from Graph import Graph
#
# app72 = Graph(note, currency.get(), db)
# app72.grid(row=0, column=0, sticky=N + S + E + W)
# note.add(app72, text='    Statistics   ')
# app72.columnconfigure(0, weight=6)
# app72.columnconfigure(1, weight=1)
# app72.rowconfigure(0, weight=1)


# function

def ckeys():
    entry66['values'] = db.categorylist
    return None


def ipurlog():
    root23 = Tk()
    root23.grid()
    root23.title("Purchase Log")
    root23.rowconfigure(0, weight=1)
    root23.columnconfigure(0, weight=1)
    p = Purchase_Log(root23, db)
    p.grid(row=0, column=0, sticky=N + S + E + W)
    root23.mainloop()


def product_entry_search():
    inp = str(entry61.get())
    if inp == " ":
        inp = ""
    l = productnamesearch(inp)
    return add(entry61, l)


def call_purchase_search(event):
    product_entry_search()


def special_purchase_search(event):
    inp = str(entry61.get())
    l = db.sqldb.execute("""SELECT cost,price,category_name,product_description FROM costs JOIN products USING (product_id)
                JOIN category USING (category_id) WHERE product_name =  "%s" """ % (inp.title())).fetchone()
    if l is None:
        l = db.sqldb.execute("""SELECT category_name,product_description FROM  products 
                JOIN category USING (category_id) WHERE product_name =  "%s" """ % (inp.title())).fetchone()
        category = l[0]
        des = l[1]
        entry62.delete(0, END)
        entry62.insert(0, "1.0")
        entry66.delete(0, END)
        text61.delete(0.0, END)
        entry66.insert(0, str(category))
        text61.insert(0.0, str(des))
        return 1
    cost = l[0]
    price = l[1]
    category = l[2]
    des = l[3]
    entry62.delete(0, END)
    entry63.delete(0, END)
    entry65.delete(0, END)
    entry66.delete(0, END)
    text61.delete(0.0, END)
    entry62.insert(0, "1.0")
    entry63.insert(0, str(cost))
    entry65.insert(0, str(price))
    entry66.insert(0, str(category))
    text61.insert(0.0, str(des))


def add2_purchase_table():
    name = Filter(entry61.get()).title()
    qty = Filter(entry62.get()).title()
    cost = Filter(entry63.get()).title()
    date = Filter(btn64.get()).title()
    price = Filter(entry65.get()).title()
    cat = Filter(entry66.get()).title()
    des = split_reconstruct(text61.get(0.0, END).split(" ")).title()
    if len(qty.split()) == 0:
        return showinfo("Input Error", "The Quantity provided Is Not Valid", parent=root)
    if len(date.split()) == 0:
        return showinfo("Input Error", "The Date provided Is Not Valid", parent=root)
    if len(cat.split()) == 0:
        return showinfo("Input Error", "The Category provided Is Not Valid", parent=root)
    if len(cost.split()) == 0:
        return showinfo(title="Input Error", message='Product Cost Must Be Specified', parent=root)
    if len(price.split()) == 0:
        price = cost
    try:
        price = float(price)
        cost = float(cost)
        qty = float(qty)
    except ValueError:
        return showinfo(title="Input Error", message='Product Quantity or Cost Price or Selling price Must Be Numbers',
                        parent=root)
    pid = db.sqldb.getproductID(name)
    if pid is None:
        aut = askokcancel("Authenticate", "The Product is not in the Product list \nLike To Add IT ?", parent=root)
        if not aut:
            return 0
        pid = db.addproduct(name, cat, des)
    costid = db.sqldb.getcostID(pid, cost, price)
    if costid is None:
        db.addcost(name, cost, price)
    lopp = [name, cost, price, qty, date]
    mlb21.insert(END, lopp)
    entry61.delete(0, END)
    entry62.delete(0, END)
    entry63.delete(0, END)
    entry65.delete(0, END)
    entry66.delete(0, END)
    text61.delete(0.0, END)
    return 1


def delete_from_purchase_table():
    index = mlb21.Select_index
    if index is None or index > mlb21.size():
        return showinfo('Error', 'Nothing is Selected To Remove')
    mlb21.delete(index)


def add2_inventory():
    for item in xrange(mlb21.size()):
        tup = mlb21.get(item)
        name = tup[0].title()
        cost = round(float(tup[1]), 2)
        price = round(float(tup[2]), 2)
        qty = round(float(tup[3]))
        date = tup[4]
        pid = db.sqldb.getproductID(name)
        costid = db.sqldb.getcostID(pid, cost, price)
        try:
            db.addpurchase(pid, costid, date, qty)
        except ValueError:
            ans = askokcancel("Purchase already listed",
                              "The puchase is already Listed \nLike to increase the product Quantity ?")
            if ans:
                pur_i_d = db.sqldb.getpurchaseID(costid, date, qty)
                qty += db.sqldb.getcell("purchase", "purchase_id", "QTY", "\"" + pur_i_d + "\"")
                db.sqldb.editpurchase(pur_i_d, 2, qty)
    mlb21.delete(0, END)
    return showinfo("Info", "All Products Has Been Added to the Inventory")


def reset():
    s = askokcancel("Warning", "Are you sure you want to reset every thing ?")
    if s:
        reset_coform()
    return 1


def reset_coform():
    db.sqldb.resetdatabase()
    return None


def remove__product(obj):
    del_row = obj.Select_index
    if del_row is None or del_row > obj.size():
        return showinfo('Error', 'Nothing is Selected To Remove')
    tup = obj.get(del_row)
    ans = askokcancel('WARNING', "Do You Really Want To Delete " + tup[1] + " ?")
    if ans:
        ie = db.deleteproduct(tup[0])
        if ie:
            showinfo('Info', tup[1] + ' Successfully Deleted')
        else:
            showinfo('Error', 'Sorry Cannot Delete, Product is attached to Invoices or Purchase. Delete Them first.')
    return b_product__search(refresh=True)


def remove__customer(obj):
    del_row = obj.Select_index
    if del_row is None or del_row > obj.size():
        return showinfo('Error', 'Nothing is Selected To Remove')
    tup = obj.get(del_row)
    ans = askokcancel('WARNING', "Do You Really Want To Delete " + tup[1] + " ?")
    if ans:
        ie = db.deletecustomer(tup[0])
        if ie:
            showinfo('Info', tup[1] + 'Has Been Deleted')
        else:
            showinfo('Error', 'Sorry Cannot Delete, Customer is attached to invoices')
        return b_customer__search(refresh=True)
    else:
        return b_customer__search(refresh=True)


BC_log1 = [""]
BP_log1 = [""]


def b_product__search(refresh=False):
    if not refresh:
        fst = split_reconstruct(str(product_search.get()).split())
        BP_log1[0] = fst
    else:
        fst = BP_log1[0]
    fst_l = set(db.searchproduct(fst))
    return print__p_table(fst_l)


def print__p_table(lists):
    lists = list(lists)
    lists.sort()
    mlb31.delete(0, END)
    for item in lists:
        tup = db.sqldb.execute(""" SELECT product_id,product_name,category_name,product_description FROM  products
                        JOIN category USING (category_id) WHERE product_name = "%s" """ % item).fetchall()
        for p in tup:
            p = list(p)
            qty = float(db.sqldb.getquantity(p[0]))
            p.append(qty)
            bg = None
            colour = "White"
            if float(qty) > 0:
                colour = "Black"
            elif float(qty) == 0:
                colour = "Red"
            if float(qty) < 0:
                bg = "Brown"
            mlb31.insert(END, p, colour, bg)
    product_search.delete(0, END)
    return 1


def b_customer__search(refresh=False):
    if not refresh:
        fst = Filter(str(customer_search.get()))
        BC_log1[0] = fst
    else:
        fst = BC_log1[0]
    fst_l = set(db.searchcustomer(fst))
    return print__c_table(fst_l)


def print__c_table(lists):
    lists = list(lists)
    lists.sort()
    mlb41.delete(0, END)
    for item in lists:
        tup = db.sqldb.execute("""SELECT customer_id,customer_name,phone_no,customer_address,customer_email
                       FROM customers JOIN contacts USING (customer_id)  WHERE customer_name = "%s" """ % (
            item)).fetchall()
        for c in tup:
            guiid = mlb41.insert(END, c, bg=None, tag="ta")
            tup1 = db.sqldb.execute("""SELECT invoice_id,invoice_no,invoice_date,paid
                           FROM invoices WHERE customer_id = "%s" ORDER BY invoice_no """ % (c[0])).fetchall()
            mlb41.insert(END, ("Invoice ID", "Invoice No", "Invoice Time Stamp", "Paid"), parent=guiid, rowname="",
                         bg='grey93', fg='Red', tag="lo")
            for p in tup1:
                mlb41.see(mlb41.insert(END, p, parent=guiid, rowname="", bg='White', fg='Blue', tag="lol"))
    mlb41.see("")
    customer_search.delete(0, END)
    return 1


def special__p_search(event):
    st = str(product_name.get())
    l = db.sqldb.execute("""SELECT product_description,price FROM costs JOIN products USING (product_id)
                 WHERE product_name =  "%s" """ % st).fetchone()
    des = l[0]
    price = l[1]
    qty = 1.00
    product_detail.delete(0.0, END)
    product_detail.insert(0.0, des)
    product_price.delete(0, END)
    product_price.insert(0, price)
    quantity.delete(0, END)
    quantity.insert(0, qty)


def special__c_search(event):
    st = str(customer_name.get())
    l = db.sqldb.execute("""SELECT customer_address,phone_no FROM customers JOIN contacts USING (customer_id)
                 WHERE customer_name =  "%s" """ % st).fetchone()
    add_inner = l[0]
    phn = l[1]
    customer_address.delete(0.0, END)
    customer_address.insert(0.0, add_inner)
    customer_phone.delete(0, END)
    customer_phone.insert(0, phn)


def call__pn_search(event):
    product_name__search()


def productnamesearch(string):
    return db.searchproduct(string.title())


def customernamesearch(string):
    return db.searchcustomer(string.title())


def invoicenosearch(string):
    return db.searchinvoice(string.title())


def categorynamesearch(string):
    return db.searchcategory(string.title())


def product_name__search():
    inp = str(product_name.get())
    if inp == " ":
        inp = ""
    l = productnamesearch(inp)
    return add(product_name, l)


def call__cn_search(event):
    customer_name__search()


def customer_name__search():
    inp = Filter(customer_name.get())
    if inp == " ":
        inp = ""
    l = customernamesearch(inp)
    return add(customer_name, l)


def call__cu_search(event):
    customer__search()


# def call__i_search(event):
#     invoice__search()


def customer__search():
    inp = str(customer_search.get())
    if inp == " ":
        inp = ""
    l = customernamesearch(inp)
    return add(customer_search, l)


# def invoice__search():
#     inp = str(invoice_search.get())
#     if inp == " ":
#         inp = ""
#     l = invoicenosearch(inp)
#     return add(invoice_search, l)


# def call__c_search(event):
#     category__search()
#
#
# def category__search():
#     inp = str(category_search.get())
#     if inp == " ":
#         inp = ""
#     l = categorynamesearch(inp)
#     return add(category_search, l)


def product__search():
    inp = str(product_search.get())
    if inp == " ":
        inp = ""
    l = productnamesearch(inp)
    return add(product_search, l)


def call__p_search(event):
    product__search()


def add(obj, l):
    l.sort()
    obj["value"] = ""
    obj["value"] = l


# def ask__cd_file():
#     fname = askopenfilename(filetypes=(('Inventory Manager Company Detail File', "*.dat"), ('All File', "*.*")))
#     try:
#         ds = open(fname, 'r')
#     except(IOError):
#         showinfo("No File", "No File With Such name Found !")
#         return 0
#     del ds
#     if len(fname) != 0:
#         Load_De(fname)
#     return 1


def ask_dbfile():
    fname = askopenfilename(filetypes=(('Inventory Manager Database File', "*.ic"), ('All File', "*.*")))
    try:
        ds = open(fname, 'r')
    except IOError:
        showinfo("No File", "No File With Such name Found !")
        return 0
    del ds
    boo = db.load(fname)
    b_customer__search(refresh=True)
    b_product__search(refresh=True)
    if not boo:
        return showinfo("Message", "Loading of product Not Completed")
    return showinfo("Message", "Loading of product successful")


def export(objentry1):
    from ImportExport import ExportCsv
    ans = askokcancel("WARNING", "2 FILES WILL BE EXPORTED SURE YOU WANT EXPORT IN THIS FOLDER ?")
    if not ans:
        return False
    exportfile1 = Filter(str(objentry1.get()))
    if len(str(exportfile1).split()) == 0:
        pass
    else:
        ec = ExportCsv(exportfile1, db)
        if ec.returns:
            objentry1.delete(0, END)
        del ec
    return showinfo("Message", "Your File Has Been Exported Successfully")


def brow__file(obj):
    """Should alawys use entry widget as obj"""
    from tkFileDialog import askopenfilename
    try:
        fname = askopenfilename(filetypes=(('Csv File', "*.csv"), ('All File', "*.*")))
    except[IOError]:
        fname = ""
        showinfo("File Error", "Choose Again")
    if len(fname) == 0:
        showinfo("File Error", "You Must Choose a Csv File For Your Inventory")
        return None
    obj.delete(0, END)
    obj.insert(0, fname)
    return 1


def save__as__file(obj):
    """Should alawys use entry widget as obj"""
    try:
        fname = asksaveasfilename(defaultextension='.csv', filetypes=[('Csv File', "*.csv"), ('TEXT File', "*.txt")])
    except[IOError]:
        fname = ""
        showinfo("File Error", "You must Export And Have A Backup")
    if len(fname) == 0:
        showinfo("File Error", "You Must Choose a Csv File For Your Inventory")
        return None
    obj.delete(0, END)
    obj.insert(0, fname)
    return 1


def import_csv(objentry1, objentry2):
    from ImportExport import ImportCsv
    importfile1 = Filter(str(objentry1))
    importfile2 = Filter(str(objentry2))
    if len(str(importfile1).split()) == 0:
        pass
    else:
        ic = ImportCsv(importfile1, "Product", db)
        if ic.returns:
            entry51.delete(0, END)
        del ic
    if len(str(importfile2).split()) == 0:
        pass
    else:
        ic = ImportCsv(importfile2, "Customer", db)
        if ic.returns:
            entry52.delete(0, END)
        del ic
    return 1


def invoice_opt_event():
    invoice__option()


def invoice__option():
    rootn = Toplevel(master=root)
    rootn.title("Invoice Options")
    rootn.columnconfigure(0, weight=1)
    rootn.rowconfigure(0, weight=1)
    ADDInvoice(rootn, db)
    rootn.wait_window()
    return 1


def category_opt_event():
    category__opt()
    return 1


def category__opt():
    rootd = Toplevel(master=root)
    rootd.title("Category Options")
    rootd.columnconfigure(0, weight=1)
    rootd.rowconfigure(0, weight=1)
    Category(rootd, db)
    rootd.wait_window()
    return True


def d_click__on__list(event):
    index = int(mlb31.tree.identify_column(event.x)[1])
    if index == 3:
        return category_opt_event()
    elif 1 < index < 6:
        return a_d_d__product(modify=True)
    else:
        return 0


def d_click__on__c_list(event):
    index = int(mlb41.tree.identify_column(event.x)[1])
    if index == 5:
        return invoice_opt_event()
    elif 7 > index > 1:
        return a_d_d__customer(modify=True)
    else:
        return 0


def getpdfdate(timestamp):
    p = timestamp.split()
    del p[3]
    return " ".join(p)


product_search.bind('<Any-KeyRelease>', call__p_search)
customer_search.bind('<Any-KeyRelease>', call__cu_search)
customer_name.bind('<Any-KeyRelease>', call__cn_search)
product_name.bind('<Any-KeyRelease>', call__pn_search)
customer_name.bind('<<ComboboxSelected>>', special__c_search)
product_name.bind('<<ComboboxSelected>>', special__p_search)
mlb41.tree.bind('<Double-Button-1>', d_click__on__c_list)
mlb31.tree.bind('<Double-Button-1>', d_click__on__list)
entry61.bind('<Any-KeyRelease>', call_purchase_search)
entry61.bind('<<ComboboxSelected>>', special_purchase_search)


def process_cart(invid):
    no_of_product = 0
    for item in xrange(int(mlb.size())):
        tup = mlb.get(item)
        no_of_product += float(tup[3])
    discount_per_product = float(Discount_var.get()) / no_of_product
    lik = []
    for item in xrange(int(mlb.size())):
        r = mlb.get(item)
        costid = str(r[0])
        product_name2 = str(r[1])
        product_description = str(r[2])
        product_qty = float(r[3])
        product_price2 = float(r[4])
        product_amount = product_qty * product_price2
        product_info = product_name2 + ' ' + product_description
        listsw = [item + 1, product_info, product_qty, product_price2, str(product_amount)]
        lik.append(listsw)
        sold_price = product_price2 - discount_per_product
        db.addsells(costid, sold_price, invid, product_qty)
    mlb.delete(0, END)
    return lik


def generate__invoice(product__list_forpdf, custup, invoicetup, detail):
    invoi_num = invoicetup[1]
    invoice__date2 = invoicetup[0]
    # Discount = invoicetup[4]
    # Amount = invoicetup[3]
    grand_total = invoicetup[2]
    cust_name = custup[1]
    cust_address = custup[2]
    cust_phone = custup[3]
    Company = detail['comp_name']
    Company_Adress = detail['comp_add']
    email = detail['comp_email']
    phone = detail['comp_phn']
    Detail_top = detail['detail_top']
    Extra_Info = detail['extra']
    Currency = detail['curry']

    PDfCompany_Adress = Company_Adress + "\n" + Detail_top + "\n" + email + "\n" + phone
    pdfcust_address = cust_address + "\n" + cust_phone
    pdf_document(pic_add="logo.png",
                 inv_no=str(invoi_num),
                 company_name=str(Company),
                 date=getpdfdate(invoice__date2),
                 company_add=str(PDfCompany_Adress),
                 cus_name=str(cust_name),
                 cus_add=str(pdfcust_address),
                 plist=product__list_forpdf,
                 grand_total=str(grand_total),
                 bottom_detail=str(Extra_Info),
                 currency=Currency,
                 total_amt=Amt_var.get(),
                 s_g_s_t=sgst_var.get(),
                 c_g_s_t=cgst_var.get(),
                 discount=Discount_var.get(),
                 sub_total=subtol_var.get()
                 )
    fileline = "Invoice\Invoice   " + invoi_num + ".pdf"
    try:
        os.startfile(fileline)
    except:
        fileline = askopenfilename(
            filetypes=(('Microsoft Word Document File', "*.docx"), ("Protable Document File", "*.pdf")))
        os.startfile(fileline)
    return None


def transfer():
    Invoi_num = invoice__maintain()
    detail = db.sqldb.get_company_details
    if Invoi_num is None:
        return 1
    alooas = db.sqldb.getinvoiceID(Invoi_num)
    if alooas is not None:
        return showinfo("Error", "Invoice Number Already Exists And Assigned To another Customer", parent=root)
    if mlb.size() == 0:
        showinfo("Input Error", "You Should Choose a Product", parent=root)
        return 1
    custup = pre_inv()
    if custup is None:
        return showinfo("Error", "Customer Detail Incomplete", parent=root)
    if len(detail['comp_name']) == 0 or len(detail['comp_add']) == 0 or len(detail['comp_phn']) == 0:
        showinfo("Input Error", "Company Detail Incomplete", parent=root)
        return 1
    ctmid, cust_name, cust_address, cust_phone = custup
    invoice__date2 = str(invoice_date.get())
    discount = str(Discount_var.get())
    amount = str(Amt_var.get())
    Grand_total = str(Gtol_var.get())
    invid = db.addinvoice(ctmid, Invoi_num, Grand_total, invoice__date2)
    Product_List_forpdf = process_cart(invid)
    invoicetup = (invoice__date2, Invoi_num, Grand_total, amount, discount)
    # if len(discount) == 0:
    #     discount = 0
    generate__invoice(Product_List_forpdf, custup, invoicetup, detail)
    Discount_var.set(0.0)
    Amt_var.set(0.0)
    Gtol_var.set(0.0)
    customer_name.delete(0, END)
    customer_address.delete(0.0, END)
    customer_phone.delete(0, END)
    invoice_num()
    return 1


def split_reconstruct(item):
    lists = []
    for r in item:
        q = ""
        for w in r:
            if w == "\n" and r == item[0]:
                continue
            elif w == "\n" and r == item[(len(item) - 1)]:
                continue
            else:
                q = q + w
        lists.append(q)
    wrd = ""
    for item in range(len(lists)):
        if lists[item] == "" or lists[item] == " ":
            continue
        elif lists[item] == "\n" and lists[(item - 1)] == "":
            n = 0
            for e in range(0, item):
                if lists[e] != "":
                    n = n + 1
                    if 0 < n <= 1:
                        wrd = wrd + lists[item]
                    else:
                        continue
                else:
                    continue
            continue
        elif lists[item] == "\n" and lists[(item + 1)] == "":
            n = 0
            for e in range(item, len(lists)):
                if lists[e] != "":
                    n = n + 1
                    if 0 < n <= 1:
                        wrd = wrd + lists[item]
                    else:
                        continue
                else:
                    continue
            continue
        else:
            wrd = wrd + lists[item] + " "
    wrd = wrd[:(len(wrd) - 1)]
    return wrd


def invoice__maintain():
    detail = db.sqldb.get_company_details
    x = Filter(str(invoice_number.get()))
    if not x.isdigit():
        showinfo("Warning", "Invoice Number have to be Number and Nothing else")
        return None
    detail['inv_start'] = str(x)
    db.sqldb.save_company_details(detail)
    return detail['inv_start']


def invoice_num():
    detail = db.sqldb.get_company_details
    num = detail['inv_start']
    num = int(num) + 1
    invoice_number['state'] = NORMAL
    invoice_number.delete(0, END)
    invoice_number.insert(0, str(num))
    invoice_number['state'] = 'readonly'
    return 0


def invoice__date():
    invoice_date.insert(invoice_date.getTimeStamp())
    return 1


def remove_from_cart():
    index = mlb.Select_index
    if index is None or index > mlb.size():
        return showinfo(title='Error', message='Nothing is Selected To Remove')
    tup = mlb.get(index)
    a = float(tup[3]) * float(tup[4])
    amount = float(Amt_var.get()) - a
    Amt_var.set(amount)
    mlb.delete(index)


def adddiscount(event):
    paid = Filter(entry20.get())
    if len(paid) == 0:
        return 1
    if not paid.isdigit():
        try:
            paid = float(paid)
        except ValueError:
            showinfo("Entry Error", "Discount Must Be Numbers Before ADDING The Discount")
            return 1
    paid = float(paid)
    dis = float(subtol_var.get()) - paid
    Discount_var.set(str(dis))
    Gtol_var.set(str(paid))


entry20.bind('<Any-KeyRelease>', adddiscount)


def add_2_cart():
    product = Filter(str(product_name.get()))
    p_de = Filter(str(product_detail.get(0.0, END)))
    p_price = Filter(str(product_price.get()))
    qty = Filter(str(quantity.get()))
    if len(product) == 0:
        showinfo("Empty Entry Error", "Product name Must Be Filled Before ADDING The Product")
        return 1
    if len(p_price) == 0:
        showinfo("Empty Entry Error", "Product Price Must Be Filled Before ADDING The Product")
        return 1
    try:
        p_price = float(p_price)
    except ValueError:
        showinfo("Empty Entry Error", "Product Price Must Be Numbers Before ADDING The Product")
        return 1
    if len(qty) == 0:
        showinfo("Empty Entry", "Product Quantity Must Be Filled Before ADDING The Product")
        return 1
    try:
        qty = float(qty)
    except ValueError:
        showinfo("Empty Entry Error", "Product quantity Must Be Numbers Before ADDING The Product")
        return 1
    PID = db.sqldb.getproductID(product)
    if PID is None:
        return showinfo("Empty Entry Error", "Product Not Listed Try ADDING The Product")
    costid = db.getanycostid(PID, p_price)
    if costid is None:
        return showinfo("Error", "No Purchase has Been Made For This Product, The Product Is Not In Stock")
    boo = False
    for ITEM in xrange(int(mlb.size())):
        r = mlb.get(ITEM)
        if costid == r[0]:
            newqty = float(r[3]) + float(qty)
            mlb.setvalue(ITEM, "QTY", newqty)
            boo = True
    if not boo:
        tup = (costid, product, p_de, float(qty), p_price)
        mlb.insert(END, tup)
    a = float(p_price) * float(qty)
    amount = float(Amt_var.get())
    amount += a
    Amt_var.set(amount)
    product_name.delete(0, END)
    product_detail.delete(0.0, END)
    product_price.delete(0, END)
    quantity.delete(0, END)
    return None


def pre_inv():
    name = Filter(str(customer_name.get()))
    address = Filter(str(customer_address.get(0.0, END)))
    phone = Filter(str(customer_phone.get()))
    if len(name) == 0 or len(address) == 0 or len(phone) == 0:
        showinfo("Empty Entry", "You Should Enter Every Detail")
        return None
    if not phone.isdigit():
        showinfo(title="Error", message='Not a Valid Phone Number', parent=root)
        return None
    ctmid = db.sqldb.getcustomerID(phone)
    if ctmid is None:
        ctmid = db.addcustomer(name, address, phone, "")
    else:
        dbcmname = db.sqldb.getcell("customers", "customer_id", "customer_name", ctmid)
        if dbcmname != name:
            showinfo("Error", "Phone Number Already registerd in %s's Name" % dbcmname)
            return None
    return ctmid, name, address, phone


def make_sure_path_exist(path):
    import os
    filepath = os.getcwd()
    if not os.path.exists(filepath + "\\" + path):
        os.mkdir(filepath + "\\" + path)
    else:
        pass
    return 1


def a_d_d__product(modify=False):
    tup = []
    if not modify:
        titlel = "New Product"
    else:
        titlel = "Modify Product"
        index = mlb31.Select_index
        tup = mlb31.get(index)
        if index is None or index > mlb31.size():
            return showinfo(title='Error', message='Nothing is Selected To Modify')
    root12 = Toplevel(master=root)
    root12.title(titlel)
    root12.grid()
    root12.focus()
    root12.rowconfigure(0, weight=1)
    root12.columnconfigure(0, weight=1)
    np = NewProduct(root12, tup, modify, db)
    np.grid(row=0, column=0, sticky=N + S + W + E)
    np.rowconfigure(0, weight=1)
    np.columnconfigure(0, weight=1)
    root12.wait_window()
    return b_product__search(refresh=True)


def a_d_d__customer(modify=False):
    tup = []
    if not modify:
        titlel = "New Customer"
    else:
        titlel = "Modify Customer"
        index = mlb41.Select_index
        if index is None or index > mlb41.size():
            return showinfo('Error', 'Nothing is Selected To Modify')
        piid = mlb41.trueparent(mlb41.Select_iid)
        index = mlb41.index(piid)
        tup = mlb41.get(index)
    root13 = Toplevel(master=root)
    root13.title(titlel)
    root13.focus()
    root13.grid()
    root13.rowconfigure(0, weight=1)
    root13.columnconfigure(0, weight=1)
    nc = NewCustomer(root13, modify, tup, db)
    nc.grid(row=0, column=0, sticky=N + W + S + E)
    nc.rowconfigure(0, weight=1)
    nc.columnconfigure(0, weight=1)
    root13.wait_window()
    return b_customer__search(refresh=True)


def call_save():
    ans = askokcancel("WARNING", "Do You Want To Save All Changes")
    if ans:
        db.save()
        root.destroy()
    else:
        root.destroy()


def cdmp_del():
    sapp = SampleApp(root, db)
    sapp.load__de


invoice__date()
invoice_num()
b_product__search(refresh=True)
b_customer__search(refresh=True)
make_sure_path_exist("invoice")
make_sure_path_exist("Data")
root.protocol(name="WM_DELETE_WINDOW", func=call_save)

root.mainloop()
