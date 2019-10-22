
import Document_def as D

class Document(object):
    def __init__(self,name,Address,Phone):
        self.Name = name
        self.Address = Address
        self.Phone = Phone

    def Customer_Detail(self):
        B = "\n"
        Del = "Name - " + str(self.Name)+ B + "Address - " + str(self.Address) + B +"Phn - " + str(self.Phone)
        return Del

    def Create_Invoice(self,Company,Invoice_num,Invoice_Date,Company_Address,Email,Phone,Detail_top,Product_List,Extra_Info,Discount,Amount):
        Customer_Name = self.Name
        Customer_Address = self.Address
        Customer_Phone = self.Phone
        Pic_Address = "logo.png"
        D.Doc(Pic_Address,Company,Invoice_num,Invoice_Date,Company_Address,Customer_Name,Customer_Address,Email,Phone,Detail_top,Customer_Phone,Product_List,Extra_Info,Discount,Amount)
        return 1
