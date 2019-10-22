



def anagram_solution1(s1,s2):
    a_list = list(s2)
    pos1 = 0
    still_ok = True
    while pos1 < len(s1) and still_ok :
        pos2 = 0
        found = False
        while pos2 < len(a_list) and not found :
            print s1[pos1]," == ",a_list[pos2]
            if s1[pos1] == a_list[pos2]:
                found = True
            else:
                pos2 = pos2 + 1
        if found:
            del a_list[pos2] 
        else:
            still_ok = False
        pos1 = pos1 + 1
    return still_ok

print(anagram_solution1('heart','aerth'))
