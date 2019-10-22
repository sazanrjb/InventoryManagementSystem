from Tkinter import *  # from x import * is bad practice
from ttk import *
from PIL import ImageTk, Image
from proWrd import Filter
from tkMessageBox import showinfo
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename


# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


def Invoke(master):
    try:
        fname = askopenfilename(parent=master.root,
                                filetypes=(('jepg File', "*.jpg"), ("PNG Image File", "*.png"), ("Bitmap Image File")))
    except:
        showinfo("File Error", "Choose Again", parent=master.root)
    if len(fname) == 0:
        showinfo("File Error", "You Must Choose a Logo For Your Invoice", parent=master.root)
        return None
    original = Image.open(str(fname))
    size1 = (250, 43)
    size2 = (703, 122)
    resize1 = original.resize(size1, Image.ANTIALIAS)
    resize2 = original.resize(size2, Image.ANTIALIAS)
    resize2.save("logo.png", 'png')
    img = ImageTk.PhotoImage(image=resize1)
    master.pics.image = img
    master.pics.configure(image=img)
    master.pics.grid(row=0, column=0, columnspan=2, rowspan=10, sticky=N + E)
    return resize2


class SampleApp:
    def __init__(self, master, db):
        self.db = db
        root = Toplevel(master)
        root.grid()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        root.lift()
        root.focus_force()
        root.grab_set()
        root.grab_release()
        root.geometry("%dx%d+%d+%d" % (600, 600, 100, 100))
        self.root = root

        fn = VerticalScrolledFrame(root)
        fn.grid(row=0, column=0, sticky=NSEW)

        app1 = Frame(fn.interior)
        app1.grid()

        # comany name

        Label(app1, text='Invoice Information',
              foreground="#3496ff", font=('Berlin Sans FB Demi', 20)).grid(row=0, column=0,
                                                                           columnspan=3,
                                                                           sticky=E + N + W + S,
                                                                           padx=10, pady=10)

        Label(app1, text='Company name').grid(row=1, column=0, sticky=E + N, padx=10, pady=10)

        self.company_name = Entry(app1, width=20)
        self.company_name.grid(row=1, column=1, columnspan=2, sticky=N + E + W + S, padx=10, pady=10)

        # Company Address
        Label(app1, text='Company Address').grid(row=2, column=0, sticky=E + N, padx=10, pady=10)

        self.company_address = Text(app1, width=10, height=7, wrap=WORD)
        self.company_address.grid(row=2, column=1, columnspan=2, sticky=N + E + W + S, padx=10, pady=10)
        self.company_address.configure(highlightthickness=1, highlightbackground="Grey", relief=FLAT)
        # Company Phone

        Label(app1, text='Phone').grid(row=3, column=0, sticky=E + N, padx=10, pady=10)

        self.company_phone = Entry(app1)
        self.company_phone.grid(row=3, column=1, columnspan=2, sticky=N + E + W + S, padx=10, pady=10)

        # Company Email

        Label(app1, text='Email').grid(row=4, column=0, sticky=E + N, padx=10, pady=10)

        self.company_email = Entry(app1)
        self.company_email.grid(row=4, column=1, columnspan=2, sticky=N + E + W + S, padx=10, pady=10)

        # Company Website

        Label(app1, text='Website  ').grid(row=5, column=0, sticky=E + N, padx=10, pady=10)

        self.company_website = Entry(app1)
        self.company_website.grid(row=5, column=1, columnspan=2, sticky=N + W + S + E, padx=10, pady=10)

        # Aditional Detail on top

        Label(app1, text='Aditional Detail on Top').grid(row=6, column=0, sticky=E + N, padx=10, pady=10)

        self.detail_top = Text(app1, width=7, height=7, wrap=WORD)
        self.detail_top.grid(row=6, column=1, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)
        self.detail_top.configure(highlightthickness=1, highlightbackground="Grey", relief=FLAT)

        # Currency
        Label(app1, text='Currency').grid(row=7, column=0, sticky=E + N, padx=10, pady=10)

        self.currency = Entry(app1)
        self.currency.grid(row=7, column=1, sticky=N + E + W + S, padx=10, pady=10)

        # Invoice Number

        Label(app1, text='Invoice Starting Number').grid(row=8, column=0, sticky=E + N, padx=10, pady=10)

        self.invoice_num_s = Entry(app1)
        self.invoice_num_s.grid(row=8, column=1, sticky=N + E + W + S, padx=10, pady=10)

        Label(app1, text='SGST Percentage').grid(row=9, column=0, sticky=E + N, padx=10, pady=10)

        # GST
        self.sgst_inp = Entry(app1)
        self.sgst_inp.grid(row=9, column=1, sticky=N + E + W + S, padx=10, pady=10)

        Label(app1, text='CGST Percentage').grid(row=10, column=0, sticky=E + N, padx=10, pady=10)

        self.cgst_inp = Entry(app1)
        self.cgst_inp.grid(row=10, column=1, sticky=N + E + W + S, padx=10, pady=10)

        # Extra Info on Bottom

        Label(app1, text='   Additional Detail on Bottom  ').grid(row=11, column=0, sticky=E + N, padx=10, pady=10)

        self.ei_buttom = Text(app1, width=7, height=7, wrap=WORD)
        self.ei_buttom.grid(row=11, column=1, columnspan=2, sticky=N + E + W + S, padx=10, pady=10)
        self.ei_buttom.configure(highlightthickness=1, highlightbackground="Grey", relief=FLAT)

        # picture Address
        Label(app1, text='Logo').grid(row=12, column=0, sticky=E + N, padx=10, pady=10)

        self.b1 = Button(app1, text='Choose File', command=lambda: Invoke(self))
        self.b1.grid(row=12, column=1, sticky=N + S + E + W, padx=10, pady=10)

        self.pics = Label(app1)
        self.pics.grid(row=13, column=1, columnspan=2, rowspan=10, sticky=NE, padx=10, pady=10)

        self.s1ico = Image.open("Data/floppy_disk_blue.png").resize((25, 25), Image.ANTIALIAS)
        self.s1ico = ImageTk.PhotoImage(image=self.s1ico)

        self.save = Button(app1, text="Save",command=lambda: self.De_Save(), width=30, image=self.s1ico,compound=LEFT)
        self.save.grid(row=24, column=1, sticky=N + E + W + S, padx=10, pady=10)

    def De_Save(self):
        detail = {'comp_name': Filter(self.company_name.get()),
                  'comp_add': Filter(str(self.company_address.get(0.0, END))),
                  'comp_phn': Filter(self.company_phone.get()),
                  'comp_email': Filter(str(self.company_email.get())),
                  'comp_site': Filter(str(self.company_website.get())),
                  'detail_top': Filter(str(self.detail_top.get(0.0, END))),
                  'curry': Filter(str(self.currency.get())),
                  'extra': Filter(str(self.ei_buttom.get(0.0, END))),
                  'sgst': Filter(self.sgst_inp.get()),
                  'cgst': Filter(self.cgst_inp.get()),
                  'pic_add': "logo.png"}
        if Filter(str(self.invoice_num_s.get()).split()) == "":
            detail['inv_start'] = "0"
        else:
            detail['inv_start'] = Filter(str(self.invoice_num_s.get()))
        self.db.sqldb.save_company_details(detail)
        return showinfo("Info", "Company Detail Saved Successfully",parent=self.root)

    @property
    def load__de(self):
        try:
            detail = self.db.sqldb.get_company_details
        except:
            self.De_Save()
            # Company name
        self.company_name.delete(0, END)
        try:
            comp_name = detail['comp_name']
        except:
            comp_name = ""
        self.company_name.insert(0, comp_name)
        # Company Address
        self.company_address.delete(0.0, END)
        try:
            comp_add = detail['comp_add']
        except:
            comp_add = ""
        self.company_address.insert(0.0, comp_add)
        # Company Phone
        self.company_phone.delete(0, END)
        try:
            comp_phn = detail['comp_phn']
        except:
            comp_phn = ""
        self.company_phone.insert(0, comp_phn)
        # Company Email
        self.company_email.delete(0, END)
        try:
            comp_email = detail['comp_email']
        except:
            comp_email = ""
        self.company_email.insert(0, comp_email)
        # Company Website
        self.company_website.delete(0, END)
        try:
            comp_site = detail['comp_site']
        except:
            comp_site = ""
        self.company_website.insert(0, comp_site)
        # Company top Detail
        self.detail_top.delete(0.0, END)
        try:
            detail_top1 = detail['detail_top']
        except:
            detail_top1 = ""
        self.detail_top.insert(0.0, detail_top1)
        # Currency
        self.currency.delete(0, END)
        try:
            curry = detail['curry']
        except:
            curry = ""
        self.currency.insert(0, curry)
        # Extra Info
        self.ei_buttom.delete(0.0, END)
        try:
            extra = detail['extra']
        except:
            extra = ""
        self.ei_buttom.insert(0.0, extra)
        # Invoice start
        self.invoice_num_s.delete(0, END)
        self.invoice_num_s.insert(0, str(detail['inv_start']))

        self.sgst_inp.delete(0, END)
        self.sgst_inp.insert(0, str(detail['sgst']))

        self.cgst_inp.delete(0, END)
        self.cgst_inp.insert(0, str(detail['cgst']))
        # Pic
        try:
            original = Image.open("logo.png")
        except(IOError):
            original = Image.new("RGB", (250, 43), "white")
        size1 = (250, 43)
        resize2 = original.resize(size1, Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image=resize2)
        self.pics.image = img
        self.pics.configure(image=img)
        return 1
