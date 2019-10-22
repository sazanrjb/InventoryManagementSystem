from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm

data = [['No', 'Product', 'Unit Price', 'Qty', 'Amount']]
N = 'n'
W = 'w'
E = 'e'
S = 's'


class Table:
    def __init__(self, master, origin, **options):
        # type: (canvas, tuple, object) -> Table
        self.master = master
        try:
            self.tablewidth = options['Width']
            self.tableheight = options['Height']
        except(KeyError):
            options['Width'] = 5 * inch
            options['Height'] = 5 * inch
            self.tablewidth = options['Width']
            self.tableheight = options['Height']
        self.row = []
        self.column = []
        xlist = [origin[0]]
        ylist = [origin[1], self.tableheight]
        self.row.append(origin[0])
        self.column.append(origin[1])
        self.no_of_rows = options['no_of_rows']
        self.no_of_column = options['no_of_column']
        self.__table = []
        self.cell_Cor = []
        for i in range(self.no_of_rows):
            self.__table.append([])
            self.cell_Cor.append([])
            for h in range(self.no_of_column):
                self.__table[i].append({})
                self.cell_Cor[i].append([])
        self.rowheight = []
        self.columnwidth = []
        d = 'rowheight' in options.keys()
        if d == False:
            self.rowheight.append(self.tableheight / self.no_of_rows)
            self.rowheight *= self.no_of_rows
        else:
            for i in range(self.no_of_rows):
                try:
                    self.rowheight.append(options['rowheight'][i])
                except(IndexError):
                    self.rowheight.append(0.3 * inch)
        d = 'columnwidth' in options.keys()
        if d == False:
            self.columnwidth.append(self.tablewidth / self.no_of_column)
            self.columnwidth *= self.no_of_column
        else:
            for i in range(self.no_of_column):
                try:
                    self.columnwidth.append(options['columnwidth'][i])
                except(IndexError):
                    self.columnwidth.append(0.3 * inch)
        for i in range(len(self.rowheight)):
            self.row.append(self.row[i] + self.rowheight[i])
        for i in range(len(self.columnwidth)):
            self.column.append(self.column[i] + self.columnwidth[i])
        for row in range(len(self.__table)):
            for cell in range(len(self.__table[row])):
                self.__table[row][cell]['origin'] = (self.column[cell], self.row[row])
                self.__table[row][cell]['cellspan'] = (self.columnwidth[cell], self.rowheight[row])
                self.__table[row][cell]['bg'] = colors.white
                self.__table[row][cell]['font'] = ("Helvetica", 20)
                self.__table[row][cell]['fontcolour'] = colors.black
                self.__table[row][cell]['justify'] = 'Left'.upper()
                self.__table[row][cell]['rightpadding'] = 1 * mm
                self.__table[row][cell]['leftpadding'] = 1 * mm
                self.__table[row][cell]['text'] = ""
                self.__table[row][cell]['image'] = ""
                self.__table[row][cell]['bpad'] = 0
                self.__table[row][cell]['gridwidth'] = 0.05
                self.__table[row][cell]['stroke'] = colors.white
                self.__table[row][cell]['lining'] = W + E + N + S
                self.__table[row][cell]['bordercolor'] = colors.black

    def modify(self, row, column, **argv):
        for i in argv.keys():
            self.__table[row][column][str(i)] = argv[i]
        return self.__table[row][column]

    def table(self, row=None, column=None):
        cell = self.__table[row][column]
        return cell

    def Get_Cor(self, row, cell):
        cell = self.cell_Cor[row][cell]
        return cell

    def DrawXLine(self, master, x1, y, width):
        x2 = x1 + width
        return master.line(x1, y, x2, y)

    def DrawYLine(self, master, x, y1, height):
        y2 = y1 + height
        return master.line(x, y1, x, y2)

    def DrawRect(self, master, x, y, width, height, fill):
        return master.rect(x, y, width, height, stroke=1, fill=fill)

    def DrawGrid(self, xlist, ylist):
        return self.master.grid(xlist, ylist)

    def DrawString(self, master, text, x, y):
        return master.drawString(x, y, text)

    def Draw(self):
        master = self.master
        for row in range(len(self.__table)):
            for cell in range(len(self.__table[row])):
                master.setFillColor(self.__table[row][cell]['bg'])
                x, y = self.__table[row][cell]['origin']
                width, height = self.__table[0][cell]['cellspan'][0], self.__table[row][cell]['cellspan'][1]
                text = unicode(self.__table[row][cell]['text'])
                fname, fsize = self.__table[row][cell]['font']
                rpad = self.__table[row][cell]['rightpadding']
                lpad = self.__table[row][cell]['leftpadding']
                bpad = self.__table[row][cell]['bpad']
                justify = self.__table[row][cell]['justify']
                sW = master.stringWidth(text, fname, fsize)
                gridwidth = self.__table[row][cell]['gridwidth']
                stroke = self.__table[row][cell]['stroke']
                lining = self.__table[row][cell]['lining']
                bordercolor = self.__table[row][cell]['bordercolor']
                if sW + rpad + lpad > width and row == 0:
                    width = sW + rpad + lpad
                    height = height
                    try:
                        self.__table[row][cell + 1]['origin'] = (x + width, y)
                    except(IndexError):
                        pass
                elif sW + rpad + lpad > width and row != 0:
                    while sW + rpad + lpad > width:
                        fsize = fsize - 1
                        sW = master.stringWidth(text, fname, fsize)
                try:
                    self.__table[row][cell + 1]['origin'] = (x + width, y)
                except(IndexError):
                    pass
                master.setLineWidth(gridwidth)
                master.setStrokeColor(stroke)
                self.cell_Cor[row][cell].append([(x, y), (width, height)])
                self.DrawRect(master, x, y, width, height, 1)
                self.__table[0][cell]['cellspan'] = (width, height)
                master.setFont(fname, fsize, leading=None)
                master.setFillColor(self.__table[row][cell]['fontcolour'])
                if justify.upper() == 'left'.upper():
                    dx, dy = x + lpad, y + (height) - bpad
                    self.DrawString(master, text, dx, dy)
                elif justify.upper() == 'center'.upper():
                    dx, dy = x + (width / 2), y + (height) - bpad
                    master.drawCentredString(dx, dy, text)
                elif justify.upper() == 'right'.upper():
                    dx, dy = x + (width) - rpad, y + (height) - bpad
                    master.drawRightString(dx, dy, text)
                master.setStrokeColor(bordercolor)
                box = self.cell_Cor[row][cell]
                for line in lining:
                    if line.lower() == 'n':
                        x1, y1 = box[0][0]
                        x2 = x1 + box[0][1][0]
                        y2 = y1
                        self.master.line(x1, y1, x2, y2)
                    elif line.lower() == 'w':
                        x1, y1 = box[0][0]
                        y2 = y1 + box[0][1][1]
                        x2 = x1
                        self.master.line(x1, y1, x2, y2)
                    elif line.lower() == 's':
                        x1, y1 = box[0][0]
                        y2 = y1 + box[0][1][1]
                        y1 = y2
                        x2 = x1 + box[0][1][0]
                        self.master.line(x1, y1, x2, y2)
                    elif line.lower() == 'e':
                        x1, y1 = box[0][0]
                        y2 = y1 + box[0][1][1]
                        x2 = x1 + box[0][1][0]
                        x1 = x2
                        self.master.line(x1, y1, x2, y2)

        return 1
