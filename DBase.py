from Tkinter import *
from ttk import *
import random

class TableDisplay(Frame):
    def __init__(self, master, lists):
        Frame.__init__(self, master)
        self.Select_index = None
        self.b = []
        s =Style()
        s.configure("new.Treeview",font=("Ebrima",9))
        s.configure("new.Treeview.Heading",font=("Arial Rounded MT Bold",10))
        for i in lists:
            self.b.append(i[0])
        self.tree = Treeview(self,column = self.b,selectmode='browse',style = "new.Treeview")
        self.tree.grid(row = 0,column = 0,sticky= N+S+E+W)
        self.lists = []
        for l,w in lists:
            self.tree.column(l,width = w*5)
            self.tree.heading(l,text = l)
        frame = Frame(self); frame.grid(row = 0,column =1,sticky = N+S+E+W)
        bn = Label(frame,width = 1,relief=FLAT);bn.pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self.tree.yview)
        sb.pack(expand=YES, fill=Y)
        self.tree['yscrollcommand']=sb.set
        self.firstcolumn("No",width = 60)
        self.tree.bind('<1>',self.rowselect)
        self.V = StringVar()
        lbl = Label(self,relief=FLAT,textvariable = self.V,anchor = E)
        lbl.grid(row = 1,column = 0,columnspan =2,sticky =N+E+S+W)
        self.V.set("Number of item in the Table - %d     "%(len(self.lists)))

        
    def rowselect(self,event):
        inter = self.tree.identify_row(event.y)
        if inter == "":
            return 0
        self.Select_index = self.lists.index(inter)

    def firstcolumn(self,head = "",width = 0,stretch = 0):
        """Use To set the heading of the key column
           along with column width and stretchability
        """
        self.tree.column("#0",minwidth = 0,width =width,stretch=stretch)
        self.tree.heading('#0',text = head)

    def delete(self,first,last=None):
        self.__dele(first,last)
        self.V.set("Number of item in the Table - %d     "%(len(self.lists)))
        
    def __dele(self,first,last=None):
        """delete a perticular row"""
        if len(self.lists) == 0:
            return 0
        iid = self.lists[first]
        if last == END :
            for i in range(first,self.size()):
                iid = self.lists[i]
                self.tree.delete(iid)
            self.lists =[]
            return None
        elif last == None :
            del self.lists[first]
            return self.tree.delete(iid)

    def get(self, iid, column = None):
        """get value of the row if only iid is specified
           else if column is specified it gets the exact value of
           that row in the column
        """
        if iid == None :
            return 0
        iid = self.lists[iid]
        if column == None:
            l = []
            for i in range(len(self.b)):
                l.append(None)
            d =self.tree.set(iid,column = column)
            for i in d.keys():
                index = self.b.index(i)
                l[index]=d[i]
            return l
        else :
            return self.tree.set(iid,column = column)

    def setvalue(self,iid, column,Value):
        """set the value of the cell[iid][column]"""
        iid = self.lists[iid]
        return self.tree.set(iid,column = column,value= Value)

    def row(self,iid,**options):
        """use to retrive or set different values of
           row iid"""
        if type(iid)==int:
            iid = self.lists[iid]
        return self.tree.item(iid,**options)

    def column(self,iid,**options):
        """use to retrive or set different values of a column"""
        if type(iid)==int:
            iid = self.b[iid]
        return self.tree.column(iid,**options)

    def index(self,iid):
        """Corresponding index of the id value"""
        self.tree.index(iid)

    def insert(self,index,elements,fg = 'Black',bg=None,rowname = None):
        """add a new row at the end of the table"""
        n= len(self.lists)
        if rowname == None :
            rowname = self.size() + 1
        l = self.tree.insert(parent="", index=END, iid=None,values = elements,text=rowname,tags=n)
        self.lists.append(l)
        if bg == None:
            bg = 'grey99'
            if n%2 == 0 :
                bg = 'grey94'
        self.tree.tag_configure(n,background=bg,foreground = fg)
        self.V.set("Number of item in the Table - %d     "%(len(self.lists)))
        

    def size(self):
        return len(self.lists)

    def see(self, iid):
        self.tree.see(iid)

    def itemconfig(self,inf,bg):
        pass

class Holding(list):
    
    def __init__(self,index):
        super(Holding,self).__init__()
        self.fieldindex = index

    def update(self,index):
        self.fieldindex = index
        
class Lists(object):
    """A Inherited python list with enhanced
       functionality in get and set item
    """
    
    def __init__(self,master):
        self.list = []
        self.master = master

    def append(self,object):
        self.list.append(object)
    
    def reverse(self):
        self.list.reverse()
        
    def index(self,value):
        return self.list.index(value)

    def __str__(self):
        return self.list.__str__()

    def __repr__(self):
        return self.list.__repr__()

    def __delitem__(self,key):
        if type(key)==str:
            index = self.master.fieldindex[key][0]
        elif type(key)==int:
            index = key
        self.list[index] = None

    def __setitem__(self,key,value):
        if type(key) != str:
            raise Exception("DataBase Keys Can't be Integers")
        index = self.master.fieldindex[key][0]
        typ = self.master.fieldindex[key][1]
        try:
            if typ == float :
                value = round(typ(value),2)
            self.list[index] = typ(value)
        except(ValueError) :
            print key , value

    def __getitem__(self,key):
        if type(key)== str :
            index = self.master.fieldindex[key][0]
        elif type(key)== int :
            index = key
        return self.list[index]



class DBTable(object):
    """This Class is a Database container
            database contains 4 element
            1. Data Holding Table
            2. PrimaryKeys or Table rownames or keys
            3. Fieldnames or Table column names
            4. No of elemnt in the table
          Table Properties :-
            1. Every key is hashable and has corresponding index
            2. Table cell can be eaisly accessed by row and column names ie field and element names directly
            3. Table cell can also be accessed by indexing just like multidimentional list 
            4. Item are stored in the table using dict only with same fieldnames keys eg DB['Product1']={'Product Name':'Motor Pump','Log Date':'January 12,2015'}
            5. Item Can be converted to dict object from list object by DB.mkdict() method by proper fieldnames indexing
        """
    def __init__(self,name):
        self.fieldnames = {} #fieldnames are dict keys and values are 2 element tuple (index,type)
        self.primarykeys = {} #primarykeys are row elementnames dict keys and values are index of table
        self.table = Holding(self.fieldnames) # list to store database detail
        self.length = 0 #no of element in table
        self.name = name

    def change_primary_key(self,fieldname):
        """takes a fieldnames and changes all the
           key with the corresponding value in the field 
        """
        fl = self.get_fielditem(fieldname).values()
        for i in fl:
            if fl.count(i) > 1 :
                raise Exception("Duplication of Key Detected Primary Key can't be Changed")
        for i in self:
            newkey = self[i][fieldname]
            self[newkey] = self.mkdict(self[i])
            del self[i]

    def __del__(self):
        del self.fieldnames,self.primarykeys,self.table
        del self.length,self.name
        del self

    def __List_init(self):
        """Initailize a special type
           of List of above class"""
        l=Lists(self.table)
        for i in range(self.flen()):
            l.append(None)
        return l

    def get_fieldtype(self,cell):
        if type(cell) == int :
            for i in self.fieldnames.keys():
                if self.fieldnames[i][0] == cell :
                    return self.fieldnames[i][1]
            raise Exception("Table Index Not Found : %d"%(cell))
        elif type(cell) == str :
            l = self.fieldnames[cell]
            return l[1]
        raise Exception("Key Provided Dosn't Exists in the Table %s"%(cell))

    def set_fieldtype(self,field,typ):
        """change a field type to the type provided
           with all its item type converted
        """
        if type(field) == int :
            field = self.index2field(field)
        self.fieldnames[field][1] = typ
        d = self.get_fielditem(field)
        for i in d.keys():
            d[i] = typ(d[i])
        self.__set_fielditem(field,d)
        self.update()
            
    def index2field(self,index):
        """Convert a field index
           to its corresponding fieldname """
        for i in self.fieldnames.keys():
            if self.fieldnames[i][0] == index :
                return i
        raise Exception("Table Field Index Not Found : %d"%(index))

    def sizeof(self):
        """Returns the size of the dbtable"""
        t= self.table.__sizeof__()
        t+= self.primarykeys.__sizeof__()
        t+= self.fieldnames.__sizeof__()
        t+= self.length.__sizeof__()
        t+= self.__sizeof__()
        return t

    def __set_fielditem(self,field,dicts):
        """takes a field name and a dict containing
           primart keys as keys and corresponding fieldvalues
           as values
        """
        for i in dicts.keys():
            self[i][field] = dicts[i]

    def __repr__(self):
        """prints the database principal data structure"""
        st = "%s : [columns - %d ; rows - %d]"%(self.name,len(self.fieldnames.keys()),len(self.primarykeys.keys()))
        return st

    def update(self):
        """this method update new fieldnames to each
           Lists class for key/index retrival 
        """
        self.table.update(self.fieldnames)

    def flen(self):
        """Returns no of fieldnames present"""
        return len(self.fieldnames.keys())

    def del_field(self,fieldname):
        """delets a field in the table along
           with all its table columns """
        index = self.fieldnames[fieldname][0]
        for i in self.table:
            del i[fieldname]
        for i in self.fieldnames.keys():
            g = self.fieldnames[i][0]
            if g>index:
                self.fieldnames[i][0]=g-1
        self.fieldnames.pop(fieldname)
        return self.update()

    def get_fielditem(self,field):
        """returns a dictionary containing
           full list of item in that field
        """
        l={}
        index = self.findex(field)
        for i in self:
            l[i] = self[i][index]
        return l

    def add_fieldlist(self,fieldlist):
        """adds the fieldnames and fieldtypes
           in the list to the DBTABLE
        """
        for i in fieldlist:
            self.add_field(i[0],i[1])
        self.update()

    def rename_field(self,oldfield,newfield):
        """Rename a Fieldname only"""
        self.fieldnames[newfield] = self.fieldnames.pop(oldfield)
        self.update()

    def add_field(self,fieldname,fieldtype):
        """This method is called to add new field to the databse"""
        self.fieldnames[fieldname] = [len(self.fieldnames.keys()),fieldtype]
        if fieldtype == int :
            Null = 0
        elif fieldtype == float :
            Null = 0.0
        elif fieldtype == str :
            Null = ""
        else :
            Null = None
        for i in self.table:
            i.append(Null)
        return self.update()

    def has_field(self,field):
        return self.fieldnames.has_key(field)

    def has_key(self,key):
        return self.primarykeys.has_key(key)

    def __add_item(self,itemname):
        """this is a private method to add new None item"""
        l = self.__List_init()
        self.primarykeys[itemname] = self.length
        for i in self.fieldnames.keys():
            typ = self.fieldnames[i][1]
            if typ== int :
                l[i]=0
            elif typ == float :
                l[i]=0
            elif typ == str :
                l[i]=""
        self.table.append(l)
        self.length += 1
        return None
        
    def fields(self):
        """Returns a List Containing
           all fieldnames """
        return map(self.index2field,xrange(self.flen()))

    def findex(self,field):
        """returns fieldnames index of the table"""
        return self.fieldnames[field][0]

    def mkdict(self,val):
        """takes a list and returns a dict by
           looping with key:index of fieldnames
        """
        d= {}
        for i in self.fields():
            index = self.fieldnames[i][0]
            d[i] = val[index]
        return d

    def keys(self):
        """retrns the rownames in a lists"""
        return map(self.index2key,xrange(len(self)))

    def index(self,key):
        """takes a key and returns a
           corresponding inndex"""
        return self.primarykeys[key]

    def index2key(self,index):
        for i in self.primarykeys.keys():
            if self.primarykeys[i] == index :
                return i
        raise Exception("Table Index Not Found : %d"%(index))

    def __delitem__(self,key):
        if type(key) == int :
            key = self.index2key(key)
        index = self.primarykeys.pop(key)
        del self.table[index]
        for i in self.keys():
            g = self.index(i)
            if g>index:
                self.primarykeys[i]= g-1
        self.length -= 1

    def __len__(self):
        """return no of item in the database"""
        return len(self.primarykeys.keys())

    def __getitem__(self,key):
        """returns the item row from the db"""
        if type(key)==str:
            index = self.primarykeys[key]
        elif type(key)==int:
            index = key
        return self.table[index]

    def __iter__(self):
        return iter(self.keys())

    def __setitem__(self,key,val):
        if type(val) != dict and val != None :
            raise Exception("DataBase values Have to be dict or None")
        if type(key) != str:
            raise Exception("DataBase Keys Can't be Integers")
        boo = self.primarykeys.has_key(key)
        if val == None and boo == False :
            return self.__add_item(key)
        l = self.__List_init()
        for i in self.fields():
            typ = self.get_fieldtype(i)
            try :
                l[i] = typ(val[i])
            except(ValueError):
                l[i] = typ(0.0)
            except(KeyError):
                print i
                l[i] = typ("")
        if boo == True :
            index = self.index(key)
            self.table[index]=l
        else :
            self.primarykeys[key] = self.length
            self.table.append(l)
            self.length += 1
        return None

    def export(self,filename):
        import csv as c
        field = self.fields()
        field.insert(0,"PrimaryKey")
        wri = open(str(filename),'wb')
        writer = c.DictWriter(wri,fieldnames=field)
        writer.writerow(dict((fn,fn)for fn in field))
        for i in self:
            d = self.mkdict(self[i])
            d["PrimaryKey"]=i
            writer.writerow(d)
        wri.close()

    def generateuniquekey(self,first = None,le=5):
        import UniqueIdGenerator as uig
        if first == None :
            first = self.name[0]
        return uig.generateuniquekey(first,self,le)

    def displaytable(self):
        root = Tk()
        root.title(self.name)
        root.grid()
        root.rowconfigure(0,weight = 1)
        root.columnconfigure(0,weight=1)
        n =len(self.fields())
        l = range(n)
        for i in self.fields():
            index = self.findex(i)
            typ = self.get_fieldtype(i)
            if typ == int or typ == float :
                width = 15
            elif typ == str :
                try :
                    if len(self[0][i])>5 :
                        width = 35
                    else :
                        width = 10
                except(IndexError):
                    width= 10
            else :
                width = 15
            l[index]=(i,width)
        mlb = TableDisplay(root,l)
        mlb.grid(row = 0 ,column =0,sticky = N+S+E+W)
        mlb.rowconfigure(0,weight = 1)
        mlb.columnconfigure(0,weight=1)
        mlb.delete(0,END)
        mlb.firstcolumn("Primary keys",100,True)
        for i in self:
            tup = []
            for f in self.fields():
                if self.get_fieldtype(f) in (list,dict) :
                    tup.append(str(self.get_fieldtype(f)))
                    continue
                tup.append(self[i][f])
            mlb.insert(END,tup,rowname = i)
        root.mainloop()




