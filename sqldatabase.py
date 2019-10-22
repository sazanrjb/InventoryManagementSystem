import sqlite3 as sqldb
import time as t


def new_database_create(conn):
    conn.execute("PRAGMA foreign_keys")
    conn.execute("""CREATE TABLE IF NOT EXISTS category(
                 category_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 category_name TEXT NOT NULL UNIQUE); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS products(
                 product_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 product_name TEXT NOT NULL UNIQUE,
                 product_description TEXT,
                 category_id TEXT NOT NULL REFERENCES category(category_id)); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS costs(
                 cost_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 product_id TEXT NOT NULL REFERENCES products(product_id) ,
                 cost FLOAT NOT NULL DEFAULT 0.0,
                 price FLOAT NOT NULL DEFAULT 0.0); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS purchase(
                 purchase_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 cost_id TEXT NOT NULL REFERENCES costs(cost_id) ,
                 QTY INT NOT NULL DEFAULT 1,
                 purchase_date TEXT NOT NULL DEFAULT CURRENT_DATE); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS customers(
                 customer_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 customer_name TEXT NOT NULL ,
                 customer_address TEXT ,
                 customer_email TEXT); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS contacts(
                 phone_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 phone_no TEXT UNIQUE NOT NULL,
                 customer_id TEXT NOT NULL REFERENCES customers(customer_id)); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS invoices(
                 invoice_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 customer_id TEXT NOT NULL REFERENCES customers(customer_id),
                 invoice_no INT NOT NULL UNIQUE,
                 paid FLOAT NOT NULL ,
                 invoice_date TEXT NOT NULL DEFAULT CURRENT_DATE ); """)

    conn.execute("""CREATE TABLE IF NOT EXISTS sells(
                 selling_id TEXT UNIQUE PRIMARY KEY NOT NULL,
                 invoice_id TEXT NOT NULL REFERENCES invoices(invoice_id),
                 sold_price FLOAT NOT NULL ,
                 QTY INT NOT NULL ,
                 cost_id TEXT NOT NULL REFERENCES costs(cost_id)); """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS 
    details( company_name TEXT,
             company_email TEXT,
             company_address TEXT,
             company_phone TEXT,
             company_website TEXT,
             company_header TEXT,
             company_footer TEXT,
             currency TEXT,
             pic_address TEXT,
             invoice_start_no INT,
             sgst_rate INT,
             cgst_rate INT)
    """)
    if conn.execute("SELECT count(*) FROM details").fetchone()[0] == 0:
        conn.execute("INSERT INTO details VALUES('','','','','','','','Rs','logo.png',0,0,0)")
    conn.commit()
    return 1


class IDPresentError(Exception):
    pass


class Mydatabase(object):
    def __init__(self):

        self.connection = sqldb.connect("Database.db")
        new_database_create(self.connection)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def execute(self, query):
        return self.cursor.execute(query)

    def getcell(self, tablename, rowname, columnname, rowid):
        row = self.cursor.execute(
            """SELECT %s FROM %s WHERE %s = "%s" """ % (columnname, tablename, rowname, rowid)).fetchone()
        if row is None:
            return None
        return row[0]

    def setcell(self, tablename, rowname, columnname, rowid, value):
        self.cursor.execute(
            """UPDATE %s SET %s = %s  WHERE %s = "%s" """ % (tablename, columnname, value, rowname, rowid))

    def addcategory(self, category):
        catid = "CAT" + str(hash(category + hex(int(t.time() * 10000))))
        self.cursor.execute(
            """INSERT INTO category (category_id,category_name) VALUES ("%s","%s") """ % (catid, category))
        return catid

    def editcategory(self, catid, newname):
        self.cursor.execute("""UPDATE category SET category_name = "%s" WHERE category_id = "%s" """ % (newname, catid))
        return True

    def getcategory_id(self, category):
        row = self.cursor.execute("""SELECT category_id FROM category WHERE category_name = "%s" """ % category)
        catid = row.fetchone()
        if catid is None:
            return catid
        return catid[0]

    def deletecategory(self, catid):
        row = self.cursor.execute("""SELECT product_id FROM products WHERE category_id = "%s" """ % (catid))
        i = row.fetchone()
        if i is None:
            self.cursor.execute("""DELETE FROM category WHERE category_id = "%s" """ % (catid))
            return True
        return False

    def getproductID(self, name):
        row = self.cursor.execute("""SELECT product_id FROM products WHERE product_name = "%s" """ % (name))
        pid = row.fetchone()
        if pid is None: return pid
        return pid[0]

    def addproduct(self, name, description, category):
        proid = "PDT" + str(hash(name + hex(int(t.time() * 10000))))
        catid = self.getcategory_id(category)
        if catid == None:
            catid = self.addcategory(category)
        if self.getproductID(name) != None:
            raise Exception("Product already listed")
        self.cursor.execute(
            """INSERT INTO products (product_id,product_name,product_description,category_id) VALUES ("%s","%s","%s","%s")""" % (
                proid, name, description, catid))
        return proid

    def editproduct(self, PID, attribute, value):
        """attribute -> name or 1 , description or 2, category_id or 3 """
        dic = {1: "product_name", 2: "product_description", 3: "category_id"}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM products WHERE product_id = "%s" """ % (attribute, PID))
        row = row.fetchone()
        if row[0] == value:
            return False
        self.cursor.execute("""UPDATE products SET %s = "%s" WHERE product_id = "%s" """ % (attribute, value, PID))
        return True

    def deleteproduct(self, PID):
        row = self.cursor.execute("""SELECT cost_id FROM costs WHERE product_id = "%s" """ % (PID))
        i = row.fetchone()
        if i == None:
            self.cursor.execute("""DELETE FROM products WHERE product_id = "%s" """ % (PID))
            return True
        return False

    def getcostID(self, PID, cost, price):
        row = self.cursor.execute(
            """SELECT cost_id FROM costs WHERE product_id = "%s" AND cost = %f AND price = %f """ % (PID, cost, price))
        iid = row.fetchone()
        if iid == None: return iid
        return iid[0]

    def addnewcost(self, PID, cost, price):
        s = PID + str(cost) + str(price) + hex(int(t.time() * 10000))
        costid = "CST" + str(hash(s))
        if self.getcostID(PID, cost, price) != None:
            raise Exception("""cost already listed""")
        self.cursor.execute("""INSERT INTO costs (cost_id,product_id,cost,price) VALUES ("%s","%s",%.2f,%.2f)""" % (
            costid, PID, cost, price))
        return costid

    def editcost(self, costid, attribute, value):
        """attribute -> product_id or 1 , cost or 2 , price or 3 """
        dic = {1: "product_id", 2: "cost", 3: "price"}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM costs WHERE cost_id = "%s" """ % (attribute, costid))
        row = row.fetchone()
        if row[0] == value:
            return False
        if attribute == "product_id":
            value = "\"" + str(value) + "\""
        self.cursor.execute("""UPDATE costs SET %s = %s WHERE cost_id = "%s" """ % (attribute, str(value), costid))
        return True

    def deletecost(self, costid):
        row = self.cursor.execute("""SELECT purchase_id FROM purchase WHERE cost_id = "%s" """ % (costid))
        i = row.fetchone()
        row = self.cursor.execute("""SELECT selling_id FROM sells WHERE cost_id = "%s" """ % (costid))
        k = row.fetchone()
        if i == None and k == None:
            self.cursor.execute("""DELETE FROM costs WHERE cost_id = "%s" """ % (costid))
            return True
        return False

    def getpurchaseID(self, costid, date, qty):
        row = self.cursor.execute(
            """SELECT purchase_id FROM purchase WHERE cost_id = "%s" AND QTY = %.2f AND purchase_date = "%s" """ % (
                costid, qty, date))
        iid = row.fetchone()
        if iid == None: return iid
        return iid[0]

    def addnewpurchase(self, costid, date, qty):
        s = costid + date + str(qty) + hex(int(t.time() * 10000))
        purid = "PUR" + str(hash(s))
        if self.getpurchaseID(costid, date, qty) != None:
            raise ValueError("purchase already listed")
        self.cursor.execute(
            """ INSERT INTO purchase (purchase_id,cost_id,QTY,purchase_date) VALUES ("%s","%s",%.2f,"%s")""" % (
                purid, costid, qty, date))
        return purid

    def editpurchase(self, purid, attribute, value):
        """""""""attribute -> cost_id or 1 , QTY or 2 , purchase_date or 3 """""""""
        dic = {1: """cost_id""", 2: """QTY""", 3: """purchase_date"""}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM purchase WHERE purchase_id = "%s" """ % (attribute, purid))
        row = row.fetchone()
        if row[0] == value:
            return False
        if attribute == """cost_id""" or attribute == """purchase_date""":
            value = """\"""" + str(value) + """\""""
        self.cursor.execute(
            """UPDATE purchase SET %s = %s WHERE purchase_id = "%s" """ % (attribute, str(value), purid))
        return True

    def deletepurchase(self, purid):
        return self.cursor.execute(""" DELETE FROM purchase WHERE purchase_id = "%s" """ % (purid))

    def getphoneID(self, phone):
        row = self.cursor.execute("""SELECT phone_id FROM contacts WHERE phone_no = "%s" """ % (phone))
        iid = row.fetchone()
        if iid == None: return iid
        return iid[0]

    def addphone(self, phone, ctmid):
        phnid = """PHN""" + str(hash(phone + ctmid + hex(int(t.time() * 10000))))
        if self.getphoneID(phone) != None:
            raise Exception("""Phone Number already listed""")
        self.cursor.execute(
            """INSERT INTO contacts (phone_id,phone_no,customer_id) VALUES ("%s","%s","%s")""" % (phnid, phone, ctmid))
        return phnid

    def editphone(self, phnid, attribute, value):
        """""""""attribute -> phone_no or 1 , customer_id or 2  """""""""
        dic = {1: """phone_no""", 2: """customer_id"""}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM contacts WHERE phone_id = "%s" """ % (attribute, phnid))
        row = row.fetchone()
        if row[0] == value:
            return False
        self.cursor.execute("""UPDATE contacts SET %s = "%s" WHERE phone_id = "%s" """ % (attribute, value, phnid))
        return True

    def deletephone(self, phnid):
        ctmid = self.getcustomer_id_frm_phn_id(phnid)
        row = self.cursor.execute("""SELECT phone_id FROM contacts WHERE customer_id = "%s" """ % (ctmid))
        i = map(lambda x: x[0], row.fetchall())
        print i
        if len(i) > 1:
            self.cursor.execute("""DELETE FROM contacts WHERE phone_id = "%s" """ % (phnid))
            return True
        return False

    def getcustomerID(self, phone):
        row = self.cursor.execute("""SELECT customer_id FROM contacts WHERE phone_no = "%s" """ % (phone))
        iid = row.fetchone()
        if iid == None: return iid
        return iid[0]

    def addnewcustomer(self, name, address, email):
        ctmid = """CTM""" + str(hash( hex(int(t.time() * 10000))))
        self.cursor.execute(
            """INSERT INTO customers (customer_id,customer_name,customer_address,customer_email) VALUES ("%s","%s","%s","%s")""" % (
                ctmid, name, address, email))
        return ctmid

    def editcustomer(self, ctmid, attribute, value):
        """""""""attribute -> customer_name or 1 , customer_address or 2,customer_email or 3  """""""""
        dic = {1: """customer_name""", 2: """customer_address""", 3: """customer_email"""}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM customers WHERE customer_id = "%s" """ % (attribute, ctmid))
        row = row.fetchone()
        if row[0] == value:
            return False
        self.cursor.execute("""UPDATE customers SET %s = "%s" WHERE customer_id = "%s" """ % (attribute, value, ctmid))
        return True

    def deletecustomer(self, ctmid):
        row = self.cursor.execute("""SELECT invoice_id FROM invoices WHERE customer_id = "%s" """ % (ctmid))
        i = row.fetchone()
        if i == None:
            self.cursor.execute("""DELETE FROM customers WHERE customer_id = "%s" """ % (ctmid))
            self.cursor.execute("""DELETE FROM contacts WHERE customer_id = "%s" """ % (ctmid))
            return True
        return False

    def getinvoiceID(self, no):
        no = int(no)
        row = self.cursor.execute("""SELECT invoice_id FROM invoices WHERE invoice_no = %d """ % (no))
        iid = row.fetchone()
        if iid == None: return iid
        return iid[0]

    def addnewinvoice(self, ctmid, no, date, paid):
        invid = """INV""" + str(hash(ctmid + date + str(paid) + str(no) + hex(int(t.time() * 10000))))
        if self.getinvoiceID(no) != None:
            raise Exception("""invoice already listed""")
        self.cursor.execute(
            """INSERT INTO invoices (invoice_id,customer_id,invoice_no,paid,invoice_date) VALUES ("%s","%s",%d,%.2f,"%s")""" % (
                invid, ctmid, no, paid, date))
        return invid

    def editinvoice(self, invid, attribute, value):
        """""""""attribute -> customer_id or 1 ,invoice_no or 2, paid or 3,invoice_date or 4  """""""""
        dic = {1: """customer_id""", 2: "invoice_no", 3: """paid""", 4: """invoice_date"""}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM invoices WHERE invoice_id = "%s" """ % (attribute, invid))
        row = row.fetchone()
        if row[0] == value:
            return False
        if attribute == """customer_id""" or attribute == """invoice_date""":
            value = "\"" + str(value) + "\""
        self.cursor.execute("""UPDATE invoices SET %s = %s WHERE invoice_id = "%s" """ % (attribute, value, invid))
        return True

    def deleteinvoice(self, invid):
        row = self.cursor.execute("""SELECT selling_id FROM sells WHERE invoice_id = "%s" """ % (invid))
        i = row.fetchone()
        if i == None:
            self.cursor.execute("""DELETE FROM invoices WHERE invoice_id = "%s" """ % (invid))
            return True
        return False

    def getsellID(self, invid, costid):
        row = self.cursor.execute("""SELECT selling_id FROM sells WHERE
                    invoice_id = "%s" AND cost_id = "%s" """ % (invid, costid))
        iid = row.fetchone()
        if iid == None: return iid
        return iid[0]

    def addnewsell(self, invid, sold, qty, costid):
        selid = """SEL""" + str(hash(invid + str(sold) + str(qty) + costid + hex(int(t.time() * 10000))))
        if self.getsellID(invid, costid) != None:
            raise ValueError("""sell already listed""")
        self.cursor.execute(
            """INSERT INTO sells (selling_id,invoice_id,sold_price,QTY,cost_id) VALUES ("%s","%s",%.2f,%.2f,"%s")""" % (
                selid, invid, sold, qty, costid))
        return selid

    def editsells(self, selid, attribute, value):
        """""""""attribute -> invoice_id or 1 , sold_price or 2,QTY or 3 ,cost_id or 4 """""""""
        dic = {1: """invoice_id""", 2: """sold_price""", 3: """QTY""", 4: """cost_id"""}
        if type(attribute) == int:
            attribute = dic[attribute]
        row = self.cursor.execute("""SELECT %s FROM sells WHERE selling_id = "%s" """ % (attribute, selid))
        row = row.fetchone()
        if row[0] == value:
            return False
        if attribute == "cost_id" or attribute == "invoice_id":
            value = "\"" + str(value) + "\""
        self.cursor.execute("""UPDATE sells SET %s = %s WHERE selling_id = "%s" """ % (attribute, value, selid))
        return True

    def deletesells(self, selid):
        return self.cursor.execute(""" DELETE FROM sells WHERE selling_id = "%s" """ % (selid))

    def getquantity(self, PID):
        row = self.cursor.execute("""SELECT cost_id FROM costs WHERE product_id = "%s" """ % (PID))
        l = row.fetchall()
        qty = 0.0
        for i in l:
            i = i[0]
            qty += self.getcostquantity(i)
        return qty

    def getcostquantity(self, cost_id):
        qtytup = list(self.cursor.execute(""" SELECT q,qty FROM (SELECT SUM(QTY) AS qty FROM sells WHERE cost_id = "%s") JOIN 
                                            (SELECT SUM(QTY) AS q FROM purchase WHERE cost_id = "%s") """ % (
            cost_id, cost_id)).fetchone())
        qty = 0.0
        if qtytup[0] == None:
            qtytup[0] = 0.0
        if qtytup[1] == None:
            qtytup[1] = 0.0
        qty += (qtytup[0] - qtytup[1])
        return float(qty)

    def resetdatabase(self):
        self.cursor.execute(""" BEGIN ;
                            DROP TABLE category;
                            DROP TABLE products;
                            DROP TABLE costs;
                            DROP TABLE purchase;
                            DROP TABLE customers;
                            DROP TABLE invoices ;
                            DROP TABLE sells ;
                            DROP TABLE contacts ;
                            COMMIT; """)
        new_database_create(self.connection)
        return True

    def getcustomer_id_frm_phn_id(self, phnid):
        row = self.cursor.execute("""SELECT customer_id FROM contacts WHERE phone_id = "%s" """ % phnid)
        iid = row.fetchone()
        if iid is None:
            return iid
        return iid[0]

    def save_company_details(self, details):
        qry = """UPDATE details SET company_name = '%s',company_address='%s',
              company_phone='%s',company_email='%s',company_website='%s',company_header='%s',
              company_footer='%s',currency='%s',pic_address='%s',invoice_start_no=%d,sgst_rate=%d,
              cgst_rate=%d;""" % (details['comp_name'],
                                  details['comp_add'],
                                  details['comp_phn'],
                                  details['comp_email'],
                                  details['comp_site'],
                                  details['detail_top'],
                                  details['extra'],
                                  details['curry'],
                                  details['pic_add'],
                                  int(details['inv_start']),
                                  int(details['sgst']),
                                  int(details['cgst']))
        cursor = self.connection.cursor()
        cursor.execute(qry)
        self.connection.commit()
        return True

    @property
    def get_company_details(self):
        row = self.cursor.execute("SELECT * FROM details").fetchone()
        details = {'comp_name': row[0], 'comp_add': row[2], 'comp_phn': row[3], 'comp_email': row[1],
                   'comp_site': row[4], 'detail_top': row[5], 'extra': row[6], 'curry': row[7], 'pic_add': row[8],
                   'inv_start': row[9], 'sgst': row[10], 'cgst': row[11]}
        return details
