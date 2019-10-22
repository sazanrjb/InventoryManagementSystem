from Tkinter import *
from ttk import *


class MultiListbox(Frame):
    def __init__(self, master, lists, height=None):
        Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.Select_index = None
        self.Select_iid = None
        self.b = []
        self.count = 0
        s = Style()
        s.configure("new.Treeview", font=("Ebrima", 9))
        s.configure("new.Treeview.Heading", font=("Arial Rounded MT Bold", 10))
        append = self.b.append
        for i in lists:
            append(i[0])
        if height == None:
            self.tree = Treeview(self, column=self.b, selectmode='browse', style="new.Treeview")
        else:
            self.tree = Treeview(self, column=self.b, selectmode='browse', style="new.Treeview", height=height)
        self.tree.grid(row=0, column=0, sticky=N + S + E + W)
        self.lists = []
        self.parentelements = []
        tree = self.tree
        for l, w in lists:
            tree.column(l, width=w * 5)
            tree.heading(l, text=l)
        frame = Frame(self);
        frame.grid(row=0, column=1, sticky=N + S + E + W)
        bn = Label(frame, width=1, relief=FLAT);
        bn.pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self.tree.yview)
        sb.pack(expand=YES, fill=Y)
        self.tree['yscrollcommand'] = sb.set
        self.firstcolumn("No", width=60)
        self.tree.bind('<1>', self.rowselect)
        self.V = StringVar()
        lbl = Label(self, relief=FLAT, textvariable=self.V, anchor=E, font=("Ebrima", 8))
        lbl.grid(row=1, column=0, columnspan=2, sticky=N + E + S + W, pady=0, padx=15)
        self.V.set("Number of Entries - %d" % (len(self.lists)))

    def rowselect(self, event):
        inter = self.tree.identify_row(event.y)
        if inter == "":
            return 0
        self.Select_iid = inter
        self.Select_index = self.lists.index(inter)

    def firstcolumn(self, head="", width=0, stretch=0):
        """Use To set the heading of the key column
           along with column width and stretchability
        """
        self.tree.column("#0", minwidth=0, width=width, stretch=stretch)
        self.tree.heading('#0', text=head)

    def trueparent(self, iid):
        piid = iid
        while piid != "":
            iid = piid
            piid = self.tree.parent(iid)
        return iid

    def delete(self, first, last=None):
        self.__dele(first, last)
        self.V.set("Number of Entries - %d" % (self.count))
        if self.count < 1 :
            self.Select_index = None

    def __dele(self, first, last):
        """delete a perticular row"""
        if len(self.lists) == 0:
            return 0
        iid = self.lists[first]
        if last == END:
            self.count = 0
            niid = self.parentelements[0]
            while niid != "":
                cdel = niid
                niid = self.tree.next(niid)
                self.tree.delete(cdel)
            self.parentelements = []
            self.lists = []
            return None
        elif last == None:
            del self.lists[first]
            try:
                self.parentelements.remove(iid)
            except(ValueError):
                pass
            self.count -= 1
            return self.tree.delete(iid)

    def get(self, iid, column=None):
        """get value of the row if only iid is specified
           else if column is specified it gets the exact value of
           that row in the column
        """
        if iid == None:
            return 0
        iid = self.lists[iid]
        if column == None:
            l = range(len(self.b))
            d = self.tree.set(iid, column=column)
            bi = self.b.index

            def done(i):
                index = bi(i)
                l[index] = d[i]

            non = map(done, d.keys())
            del non
            return l
        else:
            return self.tree.set(iid, column=column)

    def setvalue(self, iid, column, Value):
        """set the value of the cell[iid][column]"""
        iid = self.lists[iid]
        return self.tree.set(iid, column=column, value=Value)

    def row(self, iid, **options):
        """use to retrive or set different values of
           row iid"""
        if type(iid) == int:
            iid = self.lists[iid]
        return self.tree.item(iid, **options)

    def column(self, iid, **options):
        """use to retrive or set different values of a column"""
        if type(iid) == int:
            iid = self.b[iid]
        return self.tree.column(iid, **options)

    def index(self, iid):
        """Corresponding index of the id value"""
        return self.lists.index(iid)

    def insert(self, index, elements, fg='Black', bg=None, rowname=None, parent="", tag=None):
        """add a new row at the end of the table"""
        tags = self.count
        if rowname == None:
            rowname = self.count + 1
        if parent != "":
            if tag == None:
                tags = 1
            else:
                tags = tag
        l = self.tree.insert(parent=parent, index=END, iid=None, values=elements, text=rowname, tags=tags)
        self.lists.append(l)
        if parent == "":
            self.parentelements.append(l)
            self.count += 1
        if bg == None:
            bg = 'grey99'
            if tags % 2 == 0:
                bg = 'grey94'
        self.tree.tag_configure(tags, background=bg, foreground=fg)
        self.V.set("Number of Entries - %d" % (self.count))
        return l

    def size(self):
        return len(self.lists)

    def see(self, iid):
        if type(iid) == int:
            iid = self.lists[iid]
        return self.tree.see(iid)
