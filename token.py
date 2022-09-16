
from pickle import TRUE


punct = ['{','}','[',']','(',')',',',':']
opr = ['=','<','>']
datatype = ['int', 'float', 'string', 'arr']
keywords = ['if', 'else', 'while', 'for']

def isPunct(ch):
    if ch in punct:
        return True
    return False

def nextOpr(next):
    if next in opr:
        return True
    return False
    
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

def isDatatype(ch):
    if ch in datatype:
        return True
    return False
    
def isKeyword(ch):
    if ch in keywords:
        return True
    return False

file = open('E:\\6thSem\\compiler\\myproject\\file.txt','r')
lineCount = 0
for f in file:
    if not f.strip():
        print("empty")
        lineCount += 1
        continue
    lineCount +=  1
    f = f.strip()
    temp = "" 
    oprCheck = False
    for i in range(len(f)):
        # means double operator occurs
        if oprCheck:
            oprCheck = False
            continue
        else:
            # if coming is space that means it's breakpoint
            # it can be multiple spaces 
            if not f[i] == " ":
                if i == len(f)-1:
                    if not temp:
                        temp += f[i]
                        if isPunct(temp):
                            print("last punctuator", temp)
                            continue
                        if isOpr(temp):
                            print("last operator", temp)
                            continue
                        print("empty temp (last): does not match to any function which means it is a identifier", temp)
                        continue
                    else:
                        temp += f[i]
                        if isKeyword(temp):
                            print("last keyword", temp)
                            temp = ""
                            continue
                        if isDatatype(temp):
                            print("last datatype", temp)
                            temp = ""
                            continue
                        print("(last) does not match to any function which means it is a identifier", temp)
                        continue
                    
                # if temp is empty
                if not temp:
                    temp += f[i]
                    # for coming 
                    if isPunct(temp):
                        print("punctuator", temp)
                        temp = ""
                        continue
                    isOp = isOpr(temp, f[i+1])
                    if isOp:
                        print("operator:", isOp)
                        if len(isOp) == 2:
                            oprCheck = True
                        temp = ""
                        continue

                    # for next 
                    if isPunct(f[i+1]):
                        print("next punctuator", temp)
                        temp = ""
                        continue
                    if nextOpr(f[i+1]):
                        print("next operator", temp)
                        temp = ""
                        continue
                # if temp is not empty
                else:
                    temp += f[i]
                    if isPunct(f[i+1]):
                        print("next2 punctuator", temp)
                        temp = ""
                        continue
                    if isOpr(f[i+1]):
                        print("next2 operator", temp)
                        temp = ""
                        continue
            else:
                if temp == "":
                    continue
                else:
                    if isDatatype(temp):
                        print("space", temp)
                        temp = ""
                        continue
                    if isKeyword(temp):
                        print("space keyword", temp)
                        temp = ""
                        continue
                    print("space, does not match to any function which means it is a identifier", temp)
                    temp = ""
                    continue

print("line count: ", lineCount)

            