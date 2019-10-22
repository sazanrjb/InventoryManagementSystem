from PIL import Image
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from Table import Table, N, S, E, W

L_margin = 0.5 * inch
data = ['No', 'Product', 'Qty', 'Unit Price', 'Amount']
extra = [["", "", "", "", ""]]


def calucate_y(y, lines, ofset):
    lines = lines.split('\n')
    multiplier = len(lines)
    new_y = y + (multiplier * ofset)
    return new_y


def draw_string(string, canvas_instance, x, y, lead):
    textobject = canvas_instance.beginText()
    textobject.setTextOrigin(x, y)
    textobject.setLeading(lead)
    for i in string.split('\n'):
        if len(i) > 90:
            i = i.split(" ")
            s = len(i) / 4
            wrd = ""
            for w in range(3 * s):
                wrd = wrd + i[w] + " "
            textobject.textLine(wrd)
            wrd = ""
            for w in range(3 * s, len(i)):
                wrd = wrd + i[w] + " "
            textobject.textLine(wrd)
        else:
            textobject.textLine(i)
    return canvas_instance.drawText(textobject)


def pdf_document(pic_add, inv_no, company_name, date, company_add,
                 cus_name, cus_add, plist, currency, total_amt, s_g_s_t, c_g_s_t,
                 sub_total, grand_total, discount, bottom_detail):
    try:
        pil = Image.open(pic_add).resize((250, 43), Image.ANTIALIAS).transpose(Image.FLIP_TOP_BOTTOM)
    except IOError:
        pil = Image.new('RGB', (250, 43))
    p = ImageReader(pil)
    c = canvas.Canvas("Invoice\Invoice   " + inv_no + ".pdf", pagesize=A4, bottomup=0)
    c.setViewerPreference("FitWindow", "true")
    c.setFont("Times-Bold", 24)
    c.drawImage(p, 2.5 * inch, 0.5 * inch)
    heading = 2 * inch
    c.drawString(L_margin, heading, company_name)
    c.setFillColor(HexColor('#9558fb'))
    c.setLineWidth(0.1)
    c.rect(5.65 * inch - 15, heading - 20, (7.8500000000000005 * inch - 5.65 * inch) + 15, 0.34 * inch, 1, 1)
    c.setFillColor(colors.white)
    c.setFont("Times-Bold", 20)
    c.drawString(5.65 * inch, heading, "Invoice")
    for i in range(4 - len(inv_no)):
        inv_no = "0" + inv_no
    inv_no = "#" + inv_no
    c.drawRightString(7.8500000000000005 * inch - 15, heading, inv_no)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    c.drawString(5.65 * inch - 15, (heading + 0.35 * inch), "Invoice Date")
    c.drawRightString(7.8500000000000005 * inch, (heading + 0.35 * inch), date)
    c.setFont("Helvetica", 11)
    draw_string(company_add, c, L_margin, (heading + 0.5 * inch), 15)
    c.setFont("Times-Bold", 15)
    c.drawString(L_margin, calucate_y((heading + 0.5 * inch), company_add, 0.23 * inch), "Bill To :")
    c.setFont("Times-Bold", 16)
    c.drawString(L_margin, calucate_y((heading + 0.5 * inch), company_add, 0.23 * inch) + 0.3 * inch,
                 cus_name)
    hei = calucate_y((heading + 0.5 * inch), company_add, 0.23 * inch) + 0.3 * inch
    c.setFont("Helvetica", 11)
    draw_string(cus_add, c, L_margin, hei + 0.25 * inch, 15)
    ori = (hei + inch, L_margin)
    rowheight = [0.25 * inch]
    columnwidth = [0.35 * inch, 3.5 * inch, 1.1 * inch, 0.9 * inch, 1.5 * inch]
    item = plist
    if len(item) < 11:
        itemmultiply = 10 - len(item)
        item = item + extra * itemmultiply
    s = Table(c, ori, no_of_rows=len(item) + 1, no_of_column=len(item[0]), rowheight=rowheight, columnwidth=columnwidth)
    for i in range(5):
        if i == 0:
            lining = N + W + S
        elif i == 4:
            lining = N + E + S
        else:
            lining = N + S
        s.modify(0, i, text=data[i], fontcolour=colors.white, bg=HexColor('#9558fb'), bpad=2 * mm,
                 font=("Helvetica", 11), justify='center', lining=lining)
    for i in range(len(item)):
        las = len(item) - 1
        if i == 0:
            lining = N + E + W
        elif i == las:
            lining = S + E + W
        else:
            lining = E + W
        if i % 2 == 0:
            bg = HexColor('#f2ecfd')
        else:
            bg = HexColor('#e8dcff')
        for t in range(len(item[i])):
            if t == 1:
                justify = 'left'
            elif t == 4 or t == 3:
                justify = 'right'
            else:
                justify = 'center'
            s.modify(i + 1, t, text=item[i][t], fontcolour=colors.black, bpad=2 * mm, font=("Helvetica", 11),
                     justify=justify, lining=lining, bg=bg)
    s.Draw()
    tab2_ori = s.Get_Cor(-1, -2)
    x2, y2 = tab2_ori[0][0]
    w2, h2 = tab2_ori[0][1]
    tab2_ori = [x2, y2 + h2 + 0.2 * inch]
    tab2_ori.reverse()
    cw = [0.9 * inch, 0.5 * inch, 1 * inch]
    rh = [0.25 * inch, 0.25 * inch, 0.25 * inch, 0.25 * inch, 0.25 * inch]
    tab = Table(c, tab2_ori, rowheight=rh, columnwidth=cw, no_of_rows=5, no_of_column=3)
    tab.modify(0, 0, text="Total Amt", justify='right', bpad=2 * mm, font=("Helvetica", 11), fontcolour=colors.black)
    tab.modify(1, 0, text="SGST", justify='right', bpad=2 * mm, font=("Helvetica", 11), fontcolour=colors.black)
    tab.modify(2, 0, text="CGST", justify='right', bpad=2 * mm, font=("Helvetica", 11), fontcolour=colors.black)
    tab.modify(3, 0, text="SubTotal", justify='right', bpad=2 * mm, font=("Helvetica", 11), fontcolour=colors.black)
    tab.modify(4, 0, text="Discount", justify='right', bpad=2 * mm, font=("Helvetica", 11), fontcolour=colors.black)

    tab.modify(0, 1, text=currency, justify='right', bpad=2 * mm, font=("Helvetica", 11), fontcolour=colors.black,
               lining=N + S + W)
    tab.modify(1, 1, text=currency, justify='right', bpad=2 * mm, font=("Helvetica", 11), fontcolour=colors.black,
               lining=N + S + W)
    tab.modify(2, 1, text=currency, justify='right', bpad=2 * mm, font=("Helvetica", 11), fontcolour=colors.black,
               lining=N + S + W)
    tab.modify(3, 1, text=currency, justify='right', bpad=2 * mm, font=("Helvetica", 11), fontcolour=colors.black,
               lining=N + S + W)
    tab.modify(4, 1, text=currency, justify='right', bpad=2 * mm, font=("Helvetica", 11), fontcolour=colors.black,
               lining=N + S + W)

    tab.modify(0, 2, text=str(total_amt), justify='right', bpad=2 * mm, font=("Helvetica", 11),
               fontcolour=colors.black,
               rightpadding=5.5 * mm, lining=N + S + E)
    tab.modify(1, 2, text=str(s_g_s_t), justify='right', bpad=2 * mm, font=("Helvetica", 11),
               fontcolour=colors.black,
               rightpadding=5.5 * mm, lining=N + S + E)
    tab.modify(2, 2, text=str(c_g_s_t), justify='right', bpad=2 * mm, font=("Helvetica", 11),
               fontcolour=colors.black,
               rightpadding=5.5 * mm, lining=N + S + E)
    tab.modify(3, 2, text=str(sub_total), justify='right', bpad=2 * mm, font=("Helvetica", 11),
               fontcolour=colors.black,
               rightpadding=5.5 * mm, lining=N + S + E)
    tab.modify(4, 2, text=str(discount), justify='right', bpad=2 * mm, font=("Helvetica", 11),
               fontcolour=colors.black,
               rightpadding=5.5 * mm, lining=N + S + E)
    tab.Draw()
    c.setFont("Helvetica", 11)
    draw_string(bottom_detail, c, L_margin, y2 + h2 + 0.40909 * inch, 15)
    b = sum(columnwidth) + L_margin
    tab2_ori = tab.Get_Cor(-1, -1)
    x2, y2 = tab2_ori[0][0]
    w2, h2 = tab2_ori[0][1]
    c.setFont('Times-Bold', 19)
    c.setFillColor(HexColor('#9558fb'))
    ju = c.stringWidth("GrandTotal  - " + currency + " " + str(grand_total), 'Times-Bold', 19)
    c.rect((x2 + w2 - 15) - ju - 15, y2 + 0.9 * inch, ju + 30, 0.4 * inch, 1, 1)
    c.setFillColor(colors.white)
    c.drawRightString(x2 + w2 - 15, y2 + 1.2 * inch, "GrandTotal  - " + currency.decode("utf-8") + "  " + str(grand_total))
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    if len(item) >= 10:
        sign = 11 * inch
    else:
        sign = 9.5 * inch
    c.drawString(L_margin, sign, "Customer Signature")
    c.drawRightString(b - 0.12 * inch, sign, "Signature")
    c.showPage()
    try:
        c.save()
        return True
    except IOError:
        return False
