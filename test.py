
opr = ['=','<','>']
oprCheck = True

def isOpr(current, next):
    if current in opr and next in opr:
        if next == '=':
            current += next
            return current
        else:
            return current
    else:
        if current in opr:
            return current
        return False

txt = "=>"

for i in range(len(txt)-1):
    temp = isOpr(txt[i], txt[i+1])
    if temp:
        print(temp)
        print(type(temp))
    else:
        print("else ",temp)
        print(type(temp))
