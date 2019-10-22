


lists  = ['', '', '', '', 'shakdjasd', '\n', 'jasdjlk', '', '\n', 'ahnsdjkjas', '\n', '', '', '']


def Split_reconstruct(lists):
    wrd = ""
    for i in range(len(lists)):
        if lists[i] == "" or lists[i] == " ":
            continue
        elif lists[i] == "\n" and lists[(i-1)] == "" :
            n= 0
            for e in range(0,i):
                if e != "":
                    n=n+1
                    if n > 0 and n <= 1 : 
                        wrd = wrd + lists[i]
                    else :
                        continue
                else :
                    continue
            continue
        elif lists[i] == "\n" and lists[(i+1)] == "" :
            n = 0
            for e in range(i,len(lists)):
                if e != "":
                    n= n + 1
                    if n > 0 and n <= 1 :
                        wrd = wrd + lists[i]
                    else :
                        continue
                else :
                    continue
            continue
        else :
            wrd = wrd + lists[i] +" "
    wrd = wrd[:(len(wrd)-1)]
    return wrd


Split_reconstruct(lists)
