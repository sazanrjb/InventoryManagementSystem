from DBase import DBTable
from proWrd import Filter

class DatabaseTypeError(Exception):
    pass
class IncompleteDataError(Exception):
    pass

class InvalidDataError(Exception):
    pass

class Product(object):

    def __init__(self,name,category,**kwrgs):
        self.__name = ""
        self.__category = ""
        self.__description = ""
        self.__itemnr = ""
        self.__cost = 0.0
        self.__price = 0.0
        self.__id = ""
        self.__qty = 0.0
        self.__plog = self.__createPurchaseDBTable()
        self.__slog = self.__createSellingDBTable()
        self.name = name
        self.category = category
        for i in kwrgs.keys():
            try:
                self[i] = kwrgs[i]
            except(KeyError) :
                raise IncompleteDataError("All aruguments for creating a product in not provided or wrong")
            except(ValueError) :
                raise InvalidDataError("Invalid Data Type Provided with '%s'"%(i))

    def __str__(self):
        st = "%s -[Price: %g, Qty: %g, Category: %s, Cost: %g, id: %s, Description: %s, Itemnumber: %s, Plog: %s, Slog: %s]"%(self.name,self.price,self.qty,
                                                                                                                              self.category,self.cost,self.id,
                                                                                                                              self.description,self.itemnr,
                                                                                                                              self.plog.__repr__(),self.slog.__repr__())
        return st
    def __repr__(self):
        st = "%s -[Price: %g, Qty: %g, Category: %s, Cost: %g, id: %s, Description: %s, Itemnumber: %s, Plog: %s, Slog: %s]"%(self.name,self.price,self.qty,
                                                                                                                              self.category,self.cost,self.id,
                                                                                                                              self.description,self.itemnr,
                                                                                                                              self.plog.__repr__(),self.slog.__repr__())
        return st

    def getname(self):
        return self.__name
    def getcategory(self):
        return self.__category
    def getdes(self):
        return self.__description
    def getitemnumber(self):
        return self.__itemnr
    def getcost(self):
        return self.__cost
    def getprice(self):
        return self.__price
    def getid(self):
        return self.__id
    def getqty(self):
        return self.__qty
    def getplog(self):
        return self.__plog
    def getslog(self):
        return self.__slog
    def setname(self,name):
        self.__name = Filter(str(name)).title()
    def setcategory(self,category):
        self.__category = Filter(str(category)).title()
    def setdes(self,des):
        self.__description = Filter(str(des)).title()
    def setitemnumber(self,nmbr):
        self.__itemnr = nmbr
    def setcost(self,cost):
        self.__cost = round(float(cost),2)
    def setprice(self,price):
        self.__price = round(float(price),2)
    def setid(self,id):
        self.__id = str(id)
    def setqty(self,qty):
        self.__qty = round(float(qty))
    def setplog(self,plog):
        if isinstance(plog,DBTable) == True :
            self.__plog=plog
        else :
            raise Exception("Wrong Argument")
    def setslog(self,slog):
        if isinstance(slog,DBTable) == True :
            self.__slog=slog
        else :
            raise Exception("Wrong Argument")

    name = property(getname,setname)
    category = property(getcategory,setcategory)
    description = property(getdes,setdes)
    itemnr = property(getitemnumber,setitemnumber)
    cost = property(getcost,setcost)
    price = property(getprice,setprice)
    id = property(getid,setid)
    qty = property(getqty,setqty)
    plog = property(getplog,setplog)
    slog = property(getslog,setslog)

    def keys(self):
        l = vars(self).keys()
        for i in xrange(len(l)) :
            l[i]= l[i].rsplit('_Product__')[1]
        return l

    def has_key(self,key):
        l = self.keys()
        l.extend(['Cost Price','quantity','Price','Plog','Slog'])
        return key in l

    def product2dict(self):
        d = {}
        for i in self.keys():
            d[i] = self[i]
        return d

    def __createSellingDBTable(self):
        slog = DBTable("Selling Records")
        slog.add_field("Date",str)
        slog.add_field("Cost Price",float)
        slog.add_field("Sold Price",float)
        slog.add_field("Quantity",float)
        return slog

    def __createPurchaseDBTable(self):
        Plog = DBTable("Purchase Records")
        Plog.add_field("Date",str)
        Plog.add_field("Cost Price",float)
        Plog.add_field("Selling Price",float)
        Plog.add_field("Quantity",float)
        return Plog

    def addplogentry(self,date,cost,price,qty):
        """kwrgs -> date ,cost ,price,qty
        """
        plog = self.plog
        key = plog.generateuniquekey()
        plog[key] = None
        plog[key]["Date"] = date
        plog[key]["Cost Price"] = round(float(cost),2)
        plog[key]["Selling Price"] = round(float(price),2)
        plog[key]["Quantity"] = round(float(qty))
        self.plog =plog
        self['qty'] = round(float(qty)) + self['qty']
        self['cost'] = round(float(cost),2)
        self['price'] = round(float(price),2)
        return True

    def addslogentry(self,soldp,date,qty):
        slog = self.slog
        key = slog.generateuniquekey()
        slog[key]= None
        slog[key]["Date"] = date
        slog[key]["Cost Price"] = self['cost']
        slog[key]["Sold Price"] = round(float(soldp),2)
        slog[key]["Quantity"] = round(float(qty))
        self.slog = slog
        new_qty = self['qty'] - round(float(qty))
        self['qty'] = new_qty
        return True

    def editplogentry(self,row,column,val):
        Plog = self["Plog"]
        column = Plog.index2field(column)
        typ = Plog.get_fieldtype(column)
        Plog[row][column] = typ(val)
        return True

    def editslogentry(self,row,column,val):
        Slog = self["Slog"]
        column = Slog.index2field(column)
        typ = Slog.get_fieldtype(column)
        Slog[row][column] = typ(val)
        return True

    def key2setattr(self,key,val):
        try :
            getattr(self,key)
            return setattr(self,key,val)
        except(AttributeError):
            if key == 'Cost Price' :
                return setattr(self,'cost',val)
            elif key == 'itemnumber' :
                return setattr(self,'itemnr',val)
            elif key == 'quantity' :
                return setattr(self,'qty',val)
            elif key == 'Price' :
                return setattr(self,'price',val)
            elif key == 'Plog' :
                return setattr(self,'plog',val)
            elif key == 'Slog' :
                return setattr(self,'slog',val)
            raise Exception("Attribute '%s' Not Found"%(key))

    def key2attr(self,key):
        try :
            return getattr(self,key)
        except(AttributeError):
            if key == 'Cost Price' :
                return getattr(self,'cost')
            elif key == 'itemnumber' :
                return getattr(self,'itemnr',val)
            elif key == 'quantity' :
                return getattr(self,'qty')
            elif key == 'Price' :
                return getattr(self,'price')
            elif key == 'Plog' :
                return getattr(self,'plog')
            elif key == 'Slog' :
                return getattr(self,'slog')
            raise Exception("Attribute '%s' Not Found"%(key))

    def __getitem__(self,key):
        return self.key2attr(key)
    def __setitem__(self,key,val):
        self.key2setattr(key,val)




class Customer(object):

    def __init__(self,name,**kwrgs):
        self.__name = ""
        self.__address = ""
        self.__phone = ""
        self.__id = ""
        self.__invoice = ""
        self.__email = ""
        self.__due = 0.0
        self.name = name
        for i in kwrgs.keys():
            try:
                self[i] = kwrgs[i]
            except(KeyError) :
                raise IncompleteDataError("All aruguments for creating a product in not provided or wrong")
            except(ValueError) :
                raise InvalidDataError("Invalid Data Type Provided with '%s'"%(i))

    def __str__(self):
        st = "%s - [id: %s, phone no: %s, address: %s, invoice: %s, email: %s, due: %d]"%(self.name,self.id,self.phone,self.address,self.invoice,self.email,self.due)
        return st
    def __repr__(self):
        st = "%s - [id: %s, phone no: %s, address: %s, invoice: %s, email: %s, due: %d]"%(self.name,self.id,self.phone,self.address,self.invoice,self.email,self.due)
        return st

    def getname(self):
        return self.__name
    def getaddress(self):
        return self.__address
    def getphone(self):
        return self.__phone
    def getid(self):
        return self.__id
    def getinvoice(self):
        return self.__invoice
    def getemail(self):
        return self.__email
    def getdue(self):
        return self.__due
    def setname(self,value):
        self.__name = str(value).title()
    def setaddress(self,value):
        self.__address = str(value).title()
    def setphone(self,value):
        self.__phone = str(value)
    def setid(self,value):
        self.__id = str(value)
    def setinvoice(self,value):
        self.__invoice = str(value)
    def setemail(self,value):
        self.__email = str(value).title()
    def setdue(self,value):
        self.__due = round(float(value),2)

    name = property(getname,setname)
    address = property(getaddress,setaddress)
    phone = property(getphone,setphone)
    id = property(getid,setid)
    invoice = property(getinvoice,setinvoice)
    email = property(getemail,setemail)
    due = property(getdue,setdue)

    def keys(self):
        l = vars(self).keys()
        for i in xrange(len(l)) :
            l[i]= l[i].rsplit('_Customer__')[1]
        return l

    def has_key(self,key):
        l = self.keys()
        l.extend(['ID No','Name','Phone No','Invoice Nos','Due','Address','Email'])
        return key in l

    def customer2dict(self):
        d = {}
        for i in self.keys():
            d[i] = self[i]
        return d

    def key2setattr(self,key,value):
        try :
            getattr(self,key)
            return setattr(self,key,value)
        except(AttributeError):
            if key == 'ID No' :
                return setattr(self,'id',value)
            elif key == 'Name' :
                return setattr(self,'name',value)
            elif key == 'Invoice Nos' :
                return setattr(self,'invoice',value)
            elif key == 'Phone No' :
                return setattr(self,'phone',value)
            elif key == 'Due' :
                return setattr(self,'due',value)
            elif key == 'Address' :
                return setattr(self,'address',value)
            elif key == 'Email' :
                return setattr(self,'email',value)
            raise Exception("Attribute '%s' Not Found"%(key))

    def key2attr(self,key):
        try :
            return getattr(self,key)
        except(AttributeError):
            if key == 'ID No' :
                return getattr(self,'id')
            elif key == 'Name' :
                return getattr(self,'name')
            elif key == 'Invoice Nos' :
                return getattr(self,'invoice')
            elif key == 'Phone No' :
                return getattr(self,'phone')
            elif key == 'Due' :
                return getattr(self,'due')
            elif key == 'Address' :
                return getattr(self,'address')
            elif key == 'Email' :
                return getattr(self,'email')
            raise Exception("Attribute '%s' Not Found"%(key))
        
    def __getitem__(self,key):
        return self.key2attr(key)
    def __setitem__(self,key,val):
        self.key2setattr(key,val)

