
import time as t

def getnoofdays(month):
    mon = {"January":31,"February":28,"March":31,"April":30,"May":31,"June":30,"July":31,"August":31,"September":30,"October":31,"November":30,"December":31}
    if month == "February" :
        if t.localtime().tm_year%4 == 0 :
            return 29
        else :
            return 28
    else :
        return mon[month]

def getxlist(self,month):
    data = [0]*getnoofdays(month)
    for i in self.dic.keys():
        slog = self.dic[i]['slog']
        for h in slog.keys():
            date = slog[h]['Date'].split()
            if date[0] == month:
                day = date[1].split(',')[0]
                profit = slog[h]['Sold Price']-slog[h]['Cost Price']
                data[int(day)-1] += slog[h]['Quantity']*(profit)
    return tuple(data)

def getparear(self):
    data = []
    for i in self.dic.keys():
        slog = self.dic[i]['slog']
        profit = 0
        for h in slog.keys():
            profit += slog[h]['Sold Price']-slog[h]['Cost Price']
        data.append(profit)
    return tuple(data)

def getprocostd(self):
    data = []
    for i in self.dic.keys():
        data.append(self.dic[i]['cost'])
    return tuple(data)
            

def getpropriced(self):
    data = []
    for i in self.dic.keys():
        data.append(self.dic[i]['price'])
    return tuple(data)





