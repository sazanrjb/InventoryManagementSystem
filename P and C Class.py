import copy
import dbhash
import shelve
from DBase import DBTable


class InventoryDataBase(object):

    def __init__(self):
        self.dic ={}
        self.cato = {}
        self.nam ={}
        self.invn = {}

    def load(self,filename = "Product and Customer.ic"):
        f = shelve.open(filename)
        try:
            self.dic = copy.deepcopy(f["dic"])
            self.cato = copy.deepcopy(f["cato"])
            self.nam = copy.deepcopy(f["nam"])
            self.invn = copy.deepcopy(f["invn"])
        except(KeyError):
            print "key error"
            self.dic = {}
            self.cato = {}
            self.nam = {}
            self.invn = {}
        f.close()
        del f
        return 1

    def load(self,filename = "Product and Customer.ic"):
        f = shelve.open(filename)
        if f.has_key('dic')== False :
            return 0
        for i in f["dic"].keys():
            print i
            self.commit()
            name = f["dic"][i]['name']
            category = f["dic"][i]['category']
            description = f["dic"][i]['description']
            cost = f["dic"][i]['cost']
            price =  f["dic"][i]['price']
            try :
                PID = self.addproduct(name,category,description)
                costid = self.addcost(name,cost,price)
            except :
                PID = self.sqldb.getproductID(name)
                costid = self.sqldb.getcostID(PID,cost,price)
            slog = f["dic"][i]['slog']
            plog = f["dic"][i]['plog']
            for i in plog.keys():
                date = plog[i]["Date"]
                cost = plog[i]['Cost Price']
                price =  plog[i]['Selling Price']
                qty = plog[i]["Quantity"]
                try:
                    self.addpurchase(PID,costid,date,qty)
                except :
                    continue
        for i in f["nam"].keys():
            print i
            self.commit()
            name = f["nam"][i]['Name']
            invoice = f["nam"][i]['Invoice Nos']
            address = f["nam"][i]['address']
            email = f["nam"][i]['email']
            phone = f["nam"][i]['phone']
            try :
                ctmid = self.addcustomer(name,address,phone,email)
            except :
                ctmid = self.sqldb.getcustomerID(phone)
            invoice = InvoiceSplit(invoice)
            for h in invoice :
                paid = f["invn"][str(h)]["Paid"]
                date = f["invn"][str(h)]["Date"]
                try :
                    invid = self.addinvoice(ctmid,h,paid,date)
                except :
                    invid = self.sqldb.getinvoiceID(h)
                for pro in f["invn"][str(h)]["Products"]:
                    PID = self.sqldb.getproductID(pro)
                    if pro == 'Philips - Induction' :
                        pro = 'Philips Induction'
                    if pro == 'Godrej - 190 Litre Mo' :
                        pro = 'Godrej- 190 Litre Model - 190Ct62'
                    cost = f["dic"][pro]["cost"]
                    price = f["dic"][pro]["price"]
                    sold = cost
                    qty = 1.0
                    for key in  f["dic"][pro]["slog"]:
                        if date == f["dic"][pro]["slog"][key]["Date"] :
                            sold = f["dic"][pro]["slog"][key]["Sold Price"]
                            qty = f["dic"][pro]["slog"][key]["Quantity"]
                    costid = self.sqldb.getcostID(PID,cost,price)
                    print costid,PID,cost,price
                    try:
                        self.addsells(costid,sold,invid,qty)
                    except :
                        print sold,invid,qty
                    
        f.close()
        self.commit()
        del f
        return True
    
    def Save(self):
        if len(self.dic.keys()) == 0 or len(self.nam.keys()) == 0:
            return showinfo('Info','Nothing To Save')
        f = shelve.open("Product and Customer.ic",'n')
        f["dic"] = self.dic
        f["cato"] = self.cato
        f["nam"] = self.nam
        f["invn"] = self.invn
        f["sig"] = True
        f.sync()
        f.close()
        return showinfo('Info','Save Successfull')
    
    def Save():
        f = shelve.open("Product and Customer.ic",'n')
        f["dic"] = self.dic
        f["cato"] = self.cato
        f["nam"] = self.nam
        f["invn"] = self.invn
        f.sync()
        f.close()
        return showinfo('Info','Save Successfull')







