from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,cm
from reportlab.lib.units import inch,mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table,BaseDocTemplate,TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from PIL import Image
from Table import Table,N,S,E,W
import os

L_margin = 0.5*inch
inv_no = "10000"
Address = "296 G.T. Road Belur Bazar Howrah - 711202 \nDeals In Electronics\nVat No - 8445632422\nDasemporiumbelur@Gmail.Com\n8100448204"
date = "August 4, 2015"
C_name = "Ajay Chakraborty"
C_address = "12/1 Saratchandra Auta Lane, Flat No - 204, Howrah, West Bengal, Zip 711107, India\n3365334016"
data= ['No', 'Product', 'Qty', 'Unit Price', 'Amount']
item = [["2","Godrej- 192 Litre Model - 192Pqs62 Model - 192Pqs62 ","1.0","100.0","100.0"],["1","Ams - 16' T/FModel - 16' T/F","1.0","100.0","100.0"]]
Gtol = 3.00

detalB= "Goods Once Sold Cannot Be Taken Back\nBest Service Is Our Motto\nThank You Visit Again\nService To Be Provided By The Company Within Warranty Peroid\nSubjected To Howrah Jurisdiction"

extra = [["","","","",""]]
    
    

def CalucateY(Y,lines,ofset):
    y = Y
    lines = lines.split('\n')
    multiplier = len(lines)
    newY = y+(multiplier*ofset)
    return newY
    

    
def DrawString(string,canvas,x,y,lead):
    textobject = canvas.beginText()
    textobject.setTextOrigin(x,y)
    textobject.setLeading(lead)
    for i in string.split('\n'):
        if len(i)>90:
            i = i.split(" ")
            s=len(i)/4
            wrd = ""
            for w in range(3*s):
                wrd = wrd + i[w] + " "
            textobject.textLine(wrd)
            wrd = ""
            for w in range(3*s,len(i)):
                wrd = wrd + i[w] +" "
            textobject.textLine(wrd)
        else :
            textobject.textLine(i)
    return canvas.drawText(textobject)

def PDFDocument(**argv):
    pil = Image.open(argv["pic_add"]).resize((250,43),Image.ANTIALIAS).transpose(Image.FLIP_TOP_BOTTOM)
    p = ImageReader(pil)
    w,h = A4
    c = canvas.Canvas("Invoice\Invoice   "+argv['inv_no']+".pdf", pagesize=A4,bottomup = 0)
    c.setFont("Times-Bold", 24)
    c.drawImage(p,2.5*inch,0.5*inch)
    heading = 2*inch
    c.drawString(L_margin , heading, argv['company_name'])
    c.setFillColor(HexColor('#9558fb'))
    c.rect(5.65*inch - 15,heading-20,(7.8500000000000005*inch-5.65*inch)+15,0.35*inch,1,1)
    c.setFillColor(colors.white)
    c.drawString(5.65*inch , heading, "Invoice")
    for i in range(4-len(argv['inv_no'])):
        argv['inv_no'] = "0" + argv['inv_no']
    argv['inv_no'] = "#" + argv['inv_no']
    c.drawRightString(7.8500000000000005*inch-15 , heading,argv['inv_no'] )
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    c.drawString(5.65*inch , (heading+0.35*inch), "Invoice Date")
    c.drawRightString(7.8500000000000005*inch , (heading+0.35*inch), argv['date'] )
    c.setFont("Helvetica", 11)
    DrawString(argv['company_add'],c,L_margin,(heading + 0.5*inch),15)
    c.setFont("Times-Bold", 15)
    c.drawString(L_margin , CalucateY((heading + 0.5*inch),Address,0.23*inch),"Bill To :")
    c.setFont("Times-Bold", 16)
    c.drawString(L_margin , CalucateY((heading + 0.5*inch),Address,0.23*inch)+0.3*inch,argv['cus_name'])
    hei = CalucateY((heading + 0.5*inch),Address,0.23*inch)+0.3*inch
    c.setFont("Helvetica", 11)
    DrawString(argv['cus_add'],c,L_margin,hei + 0.25*inch,15)
    ori = (hei+inch,L_margin)
    rowheight = [0.25*inch]
    columnwidth = [0.35*inch,3.5*inch,1.1*inch,0.9*inch,1.5*inch]
    item = argv['plist']
    if len(item) < 11:
        itemmultiply = 10 - len(item)
        item = item + extra*itemmultiply
    amt = 0
    for i in item:
        if i[4] == "":
            continue
        amt = amt + float(i[4])
    s = Table(c,ori,no_of_rows=len(item)+1,no_of_column = len(item[0]),rowheight= rowheight,columnwidth=columnwidth)
    for i in range(5):
        if i == 0:
            lining = N+W+S
        elif i == 4:
            lining = N+E+S
        else :
            lining = N+S
        s.modify(0,i,text=data[i],fontcolour = colors.white,bg = HexColor('#9558fb'),bpad=2*mm,font = ("Helvetica", 11),justify = 'center',lining = lining)
    for i in range(len(item)):
        las = len(item) -1
        if i == 0:
            lining = N+E+W
        elif i == las:
            lining = S+E+W
        else :
            lining = E+W
        if i%2 == 0:
            bg = HexColor('#f2ecfd')
        else :
            bg = HexColor('#e8dcff')
        for t in range(len(item[i])):
            if t == 1:
                justify = 'left'
            elif t == 4 or t == 3 :
                justify = 'right'
            else :
                justify = 'center'
            s.modify(i+1,t,text=item[i][t],fontcolour = colors.black,bpad=2*mm,font = ("Helvetica", 11),justify = justify,lining = lining,bg = bg )
    s.Draw()
    tab2_ori = s.Get_Cor(-1,-2)
    x2,y2 = tab2_ori[0][0]
    w2,h2 = tab2_ori[0][1]
    tab2_ori = [x2,y2+h2+0.2*inch]
    tab2_ori.reverse()
    cw = [0.9*inch,1.5*inch]
    rh = [0.25*inch,0.25*inch]
    tab = Table(c,tab2_ori,rowheight= rh,columnwidth=cw,no_of_rows = 2,no_of_column = 2)
    tab.modify(0,0,text = "SubTotal",justify = 'right',bpad = 2*mm,font =("Helvetica", 11),fontcolour = colors.black)
    tab.modify(1,0,text = "Discount",justify = 'right',bpad = 2*mm,font =("Helvetica", 11),fontcolour = colors.black)
    tab.modify(0,1,text = str(amt),justify = 'right',bpad = 2*mm,font =("Helvetica", 11),fontcolour = colors.black,rightpadding = 12*mm)
    Gtol = argv['Gtol']
    dis = amt - Gtol
    tab.modify(1,1,text = str(dis),justify = 'right',bpad = 2*mm,font =("Helvetica", 11),fontcolour = colors.black,rightpadding = 12*mm)
    tab.Draw()
    c.setFont("Helvetica", 11)
    DrawString(argv['bottom_detail'],c,L_margin,y2+h2+0.40909*inch,15)
    b = sum(columnwidth)+L_margin
    tab2_ori = tab.Get_Cor(-1,-1)
    x2,y2 = tab2_ori[0][0]
    w2,h2 = tab2_ori[0][1]
    c.setFont('Times-Bold', 20)
    c.setFillColor(HexColor('#9558fb'))
    ju = c.stringWidth("GrandTotal  -  "+str(Gtol),'Times-Bold',20)
    c.rect((x2+w2-15)-ju-15,y2+0.9*inch,ju+30,0.4*inch,1, 1)
    c.setFillColor(colors.white)
    c.drawRightString(x2+w2-15,y2+1.2*inch,"GrandTotal  -  "+str(Gtol))
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    if len(item)>= 10 :
        Sign = 11*inch
    else :
        Sign = 9.5*inch
    c.drawString(L_margin , Sign,"Customer Signature")
    c.drawRightString(b-0.12*inch , Sign,"Signature")

    c.showPage()
    c.save()
    
    os.startfile("Invoice\Invoice   "+inv_no+".pdf")
    
PDFDocument(pic_add = "logo.png",inv_no=inv_no,company_name = "Das Emporium",date = date,company_add = Address,cus_name = C_name,cus_add =C_address,plist =item,
            Gtol =Gtol,bottom_detail = detalB)
