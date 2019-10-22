from ttkcalendar import Calendar
import calendar
from Tkinter import *
from ttk import *
import time as t
import datetime
from proWrd import Filter, InvoiceSplit
from PIL import ImageTk, Image


class CalendarButton(Frame):
    def __init__(self, master, **kw):
        self.datevar = StringVar()
        self.master = master
        Frame.__init__(self, master, **kw)
        self.tmp = Image.open("Data/calender.png").resize((30, 30), Image.ANTIALIAS)
        self.tmp = ImageTk.PhotoImage(image=self.tmp)
        self.btn = Button(self, textvariable=self.datevar,
                          image=self.tmp, compound=RIGHT,
                          command=lambda: self.opencalender(), takefocus=False)
        self.btn.pack(side=TOP, expand=YES, fill=BOTH)
        self.bind('<Button-1>', self.coor)
        self.btn.bind('<Button-1>', self.coor)
        now = self.getTimetuple()
        self.timetuple2object(now)
        self.update()

    def timetuple2object(self, now):
        self.year = now.tm_year
        self.month = now.tm_mon
        self.day = now.tm_mday
        self.hour = now.tm_hour
        self.min = now.tm_min
        self.sec = now.tm_sec

    def update(self):
        date = datetime.datetime(self.year, self.month, self.day, self.hour, self.min, self.sec)
        st = date.ctime()
        self.datevar.set("")
        self.datevar.set(st)

    def coor(self, event):
        try:
            w = int(str(self.rootc1).split(".")[1])
        except(AttributeError):
            return 0
        f = event.widget
        try:
            c = int(str(f).split(".")[1])
        except(ValueError):
            return 0
        if cmp(c, w) != 0:
            self.rootc1.destroy()
            self.rootc1.unbind_all('<Button-1>')
            try:
                self.btn['state'] = NORMAL
            except(TclError):
                print "calenbutt"

    def getTimetuple(self, stamp=None):
        if stamp == None:
            return t.localtime()
        return t.strptime(stamp)

    def getTimeStamp(self, timetuple=None):
        if timetuple == None:
            return t.asctime()
        return t.asctime(timetuple)

    def insert(self, string):
        tup = self.getTimetuple(string)
        self.timetuple2object(tup)
        self.update()

    def get(self):
        return self.datevar.get()

    def gotit(self, se, event=None):
        date = se.get_date()
        self.hour = int(Filter(self._h.get()))
        self.min = int(Filter(self._m.get()))
        self.sec = int(Filter(self._s.get()))
        if date != None:
            self.year = date[0]
            self.month = date[1]
            self.day = date[2]
        self.update()
        self.rootc1.destroy()
        self.btn['state'] = NORMAL
        self.rootc1.unbind_all('<Button-1>')

    def opencalender(self):
        self.update_idletasks()
        screenw = self.winfo_screenwidth()
        h = self.winfo_reqheight()
        w = self.winfo_width()
        x = self.winfo_rootx()
        if x > screenw / 2:
            if w < 260:
                x = x - (260 - w)
        y = self.winfo_rooty() + h
        if w < 260:
            w = 260
        self.rootc1 = Toplevel()
        self.rootc1.wm_attributes("-transparentcolor", 'gray98')
        self.rootc1.bind_all('<Button-1>', self.coor, "+")
        self.rootc1.title('Ttk Calendar')
        self.rootc1.columnconfigure(0, weight=1)
        self.rootc1.columnconfigure(1, weight=1)
        self.rootc1.columnconfigure(2, weight=1)
        self.rootc1.columnconfigure(3, weight=1)
        self.rootc1.columnconfigure(4, weight=1)
        self.rootc1.columnconfigure(5, weight=1)
        self.rootc1.rowconfigure(0, weight=1)
        self.rootc1.rowconfigure(1, weight=1)
        self.rootc1.rowconfigure(2, weight=1)
        self.rootc1.overrideredirect(1)
        self.rootc1.focus_set()
        self.rootc1.geometry('%sx220+%d+%d' % (w, x, y))
        ttkcal = Calendar(self.rootc1, firstweekday=calendar.SUNDAY)
        ttkcal.grid(row=0, column=0, columnspan=6, sticky=N + S + E + W)
        ttkcal.bind('<Button-1>', self.coor)
        Label(self.rootc1, text="Hour", width=15, background="grey99").grid(row=1, column=0, sticky=N + S + E + W)
        self._h = Spinbox(self.rootc1, from_=0, to=23)
        self._h.grid(row=1, column=1, sticky=N + S + E + W)
        Label(self.rootc1, text="Min", width=15, background="grey99").grid(row=1, column=2, sticky=N + S + E + W)
        self._m = Spinbox(self.rootc1, from_=0, to=59)
        self._m.grid(row=1, column=3, sticky=N + S + E + W)
        Label(self.rootc1, text="Sec", width=15, background="grey99").grid(row=1, column=4, sticky=N + S + E + W)
        self._s = Spinbox(self.rootc1, from_=0, to=59)
        self._s.grid(row=1, column=5, sticky=N + S + E + W)
        btn = Button(self.rootc1, text='Done', command=lambda: self.gotit(ttkcal))
        btn.grid(row=2, column=0, columnspan=6, sticky=N + S + E + W)
        self.btn['state'] = DISABLED
        self._h.delete(0, END)
        self._m.delete(0, END)
        self._s.delete(0, END)
        now = self.getTimetuple()
        self._h.insert(0, now.tm_hour)
        self._m.insert(0, now.tm_min)
        self._s.insert(0, now.tm_sec)
        self.rootc1.mainloop()
